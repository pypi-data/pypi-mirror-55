"""
A process that manages tracking and running update commands for the AL services.

TODO:
    - docker build updates
    - kubernetes interfaces

"""
import os
import sched
import shutil
import tempfile
import random
import string
import json
import time
from contextlib import contextmanager
from threading import Thread
from typing import Dict

import docker
from passlib.hash import bcrypt

from assemblyline_core.server_base import ServerBase
from assemblyline.common import forge
from assemblyline.common.isotime import now_as_iso
from assemblyline.datastore.helper import AssemblylineDatastore
from assemblyline.odm.models.user import User
from assemblyline.odm.models.user_settings import UserSettings
from assemblyline.remote.datatypes import get_client
from assemblyline.remote.datatypes.hash import Hash
from assemblyline.odm.models.service import DockerConfig
from assemblyline.common.security import get_random_password, get_password_hash

SERVICE_SYNC_INTERVAL = 30  # How many seconds between checking for new services, or changes in service status
UPDATE_CHECK_INTERVAL = 5   # How many seconds per check for outstanding updates

# How to identify the update volume as a whole, in a way that the underlying container system recognizes.
FILE_UPDATE_VOLUME = os.environ.get('FILE_UPDATE_VOLUME', None)
# Where to find the update directory inside this container.
FILE_UPDATE_DIRECTORY = os.environ.get('FILE_UPDATE_DIRECTORY', None)

# How many past updates to keep for file based updates
UPDATE_FOLDER_LIMIT = 5


@contextmanager
def temporary_api_key(ds: AssemblylineDatastore, user_name: str, permissions=('R', 'W')):
    """Creates a context where a temporary API key is available."""

    name = ''.join(random.choices(string.ascii_letters, k=20))
    random_pass = get_random_password(length=48)
    ds.user.update(user_name, [
        (ds.user.UPDATE_SET, f'apikeys.{name}', {"password": bcrypt.encrypt(random_pass), "acl": permissions})
    ])

    try:
        yield f"{name}:{random_pass}"
    finally:
        ds.user.update(user_name, [(ds.user.UPDATE_DELETE, 'apikeys', name)])


class DockerUpdateInterface:
    """Wrap docker interface for the commands used in the update process.

    Volumes used for file updating on the docker interface are simply a host directory that gets
    mounted at different depths and locations in each container.

    FILE_UPDATE_VOLUME gives us the path of the directory on the host, so that we can mount
    it properly on new containers we launch. FILE_UPDATE_DIRECTORY gives us the path
    that it is mounted at in the update manager container.
    """
    def __init__(self):
        self.client = docker.from_env()

    def launch(self, name, docker_config: DockerConfig, mounts, env, namespace: str, blocking: bool = True):
        """Run a container to completion."""
        self.client.containers.run(
            image=docker_config.image,
            name='update_' + name,
            # cpu_period=100000,
            # cpu_quota=int(100000*prof.cpu),
            # mem_limit=f'{prof.ram}m',
            restart_policy={'Name': 'never'},
            command=docker_config.command,
            volumes={os.path.join(row['volume'], row['source_path']): {'bind': row['dest_path'], 'mode': 'rw'}
                     for row in mounts},
            environment=[f'{_e.name}={_e.value}' for _e in docker_config.environment]
                        + [f'{_e.name}={_e.value}' for _e in env],
            detach=not blocking,
        )

    def restart(self, service_name, namespace):
        for container in self.client.containers.list(filters={'label': f'component={service_name}'}):
            container.kill()


class KubernetesUpdateInterface:
    def launch(self, name, docker_config: DockerConfig, mounts, env, namespace: str, blocking: bool = True):
        raise NotImplementedError()

    def restart(self, service_name, namespace):
        raise NotImplementedError()


class ServiceUpdater(ServerBase):
    def __init__(self, persistent_redis=None, logger=None, datastore=None):
        super().__init__('assemblyline.service.updater', logger=logger)

        if not FILE_UPDATE_DIRECTORY:
            raise RuntimeError("The updater process must be run within the orchestration environment, "
                               "the update volume must be mounted, and the path to the volume must be "
                               "set in the environment variable FILE_UPDATE_DIRECTORY. Setting "
                               "FILE_UPDATE_DIRECTORY directly may be done for testing.")

        # The directory where we want working temporary directories to be created.
        # Building our temporary directories in the persistent update volume may
        # have some performance down sides, but may help us run into fewer docker FS overlay
        # cleanup issues. Try to flush it out every time we start. This service should
        # be a singleton anyway.
        self.temporary_directory = os.path.join(FILE_UPDATE_DIRECTORY, '.tmp')
        shutil.rmtree(self.temporary_directory, ignore_errors=True)
        os.mkdir(self.temporary_directory)

        self.config = forge.get_config()
        self.datastore = datastore or forge.get_datastore()
        self.persistent_redis = persistent_redis or get_client(
            host=self.config.core.redis.persistent.host,
            port=self.config.core.redis.persistent.port,
            private=False,
        )

        self.services = Hash('service-updates', self.persistent_redis)
        self.running_updates: Dict[str, Thread] = {}

        # Prepare a single threaded scheduler
        self.scheduler = sched.scheduler()

        #
        if 'KUBERNETES_SERVICE_HOST' in os.environ:
            self.controller = KubernetesUpdateInterface()
        else:
            self.controller = DockerUpdateInterface()

    def sync_services(self):
        """Download the service list and make sure our settings are up to date"""
        self.scheduler.enter(SERVICE_SYNC_INTERVAL, 0, self.sync_services)

        # Get all the service data
        for service in self.datastore.list_all_services(full=True):

            # Ensure that any disabled services are not being updated
            if not service.enabled and self.services.exists(service.name):
                self.log.info(f"Service updates disabled for {service.name}")
                self.services.pop(service.name)

            # Ensure that any enabled services with an update config are being updated
            if service.enabled and service.update_config and not self.services.exists(service.name):
                self.log.info(f"Service updates enabled for {service.name}")
                self.services.add(
                    service.name,
                    dict(
                        next_update=now_as_iso(),
                        previous_update=now_as_iso(-10**10),
                        sha256='',
                    )
                )

    def try_run(self):
        """Run the scheduler loop until told to stop."""
        # Do an initial call to the main methods, who will then be registered with the scheduler
        self.sync_services()
        self.update_services()

        # Run as long as we need to
        while self.running:
            delay = self.scheduler.run(False)
            time.sleep(min(delay, 0.1))

    def update_services(self):
        """Check if we need to update any services.

        Spin off a thread to actually perform any updates. Don't allow multiple threads per service.
        """
        self.scheduler.enter(UPDATE_CHECK_INTERVAL, 0, self.update_services)

        # Check for finished update threads
        self.running_updates = {name: thread for name, thread in self.running_updates.items() if thread.is_alive()}

        # Check if its time to try to update the service
        for service_name, data in self.services.items():
            if data['next_update'] <= now_as_iso() and service_name not in self.running_updates:
                self.running_updates[service_name] = Thread(
                    target=self.run_update,
                    kwargs=dict(service_name=service_name)
                )
                self.running_updates[service_name].start()

    def run_update(self, service_name):
        """Common setup and tear down for all update types."""
        # noinspection PyBroadException
        try:
            # Check for new update with service specified update method
            service = self.datastore.get_service_with_delta(service_name)
            update_method = service.update_config.method
            update_data = self.services.get(service_name)
            update_hash = None

            try:
                # Actually run the update method
                if update_method == 'run':
                    update_hash = self.do_file_update(
                        service=service,
                        previous_hash=update_data['sha256'],
                        previous_update=update_data['previous_update']
                    )
                elif update_method == 'build':
                    update_hash = self.do_build_update()

                # If we have performed an update, write that data
                if update_hash is not None and update_hash != update_data['sha256']:
                    update_data['sha256'] = update_hash
                    update_data['previous_update'] = now_as_iso()
                else:
                    update_hash = None

            finally:
                # Update the next service update check time
                update_data['next_update'] = now_as_iso(service.update_config.update_interval_seconds)
                self.services.set(service_name, update_data)

            if update_hash:
                self.controller.restart(service_name=service_name, namespace=self.config.core.scaler.service_namespace)

        except BaseException:
            self.log.exception("An error occurred while running an update for: " + service_name)

    def do_build_update(self):
        """Update a service by building a new container to run."""
        raise NotImplementedError()

    def do_file_update(self, service, previous_hash, previous_update):
        """Update a service by running a container to get new files."""
        input_directory = tempfile.mkdtemp(dir=self.temporary_directory)
        output_directory = tempfile.mkdtemp(dir=self.temporary_directory)
        service_dir = os.path.join(FILE_UPDATE_DIRECTORY, service.name)

        try:
            username = self.ensure_service_account()

            with temporary_api_key(self.datastore, username) as api_key:

                # Write out the parameters we want to pass to the update container
                with open(os.path.join(input_directory, 'config.yaml'), 'w') as update_config:
                    json.dump(update_config, {
                        'previous_update': previous_update,
                        'previous_hash': previous_hash,
                        'sources': service.update_config.sources.as_primitives(),
                        'api_user': username,
                        'api_key': api_key,
                    })

                # Run the update container
                self.controller.launch(
                    name=service.name,
                    docker_config=service.update_config.run_options,
                    mounts=[
                        {
                            'volume': FILE_UPDATE_VOLUME,
                            'source_path': os.path.relpath(input_directory, FILE_UPDATE_DIRECTORY),
                            'dest_path': '/mount/input_directory'
                        },
                        {
                            'volume': FILE_UPDATE_VOLUME,
                            'source_path': os.path.relpath(output_directory, FILE_UPDATE_DIRECTORY),
                            'dest_path': '/mount/output_directory'
                        },
                    ],
                    env={
                        'UPDATE_CONFIGURATION_PATH': '/mount/input_directory/config.yaml',
                        'UPDATE_OUTPUT_PATH': '/mount/output_directory/'
                    },
                    blocking=True,
                    namespace=self.config.core.scaler.core_namespace,
                )

                # Read out the results from the output container
                results_meta_file = os.path.join(output_directory, 'response.yaml')

                if not os.path.exists(results_meta_file) or not os.path.isfile(results_meta_file):
                    return None

                with open(results_meta_file) as rf:
                    results_meta = json.load(rf)
                update_hash = results_meta.get('hash', None)

                # Erase the results meta file
                os.unlink(results_meta_file)

                # FILE_UPDATE_DIRECTORY/{service_name} is the directory mounted to the service,
                # the service sees multiple directories in that directory, each with a timestamp
                destination_dir = os.path.join(service_dir, service.name + '_' + now_as_iso())
                shutil.move(output_directory, destination_dir)

                # Remove older update files, due to the naming scheme, older ones will sort first lexically
                existing_folders = []
                for folder_name in os.listdir(service_dir):
                    if os.path.isdir(folder_name) and folder_name.startswith(service.name):
                        existing_folders.append(folder_name)
                existing_folders.sort()
                for extra_folder in existing_folders[:UPDATE_FOLDER_LIMIT]:
                    shutil.rmtree(os.path.join(service_dir, extra_folder), ignore_errors=True)

                return update_hash
        finally:
            # If the working directory is still there for any reason erase it
            shutil.rmtree(input_directory, ignore_errors=True)
            shutil.rmtree(output_directory, ignore_errors=True)

    def ensure_service_account(self):
        """Check that the update service account exists, if it doesn't, create it."""
        uname = 'update_service_account'

        if self.datastore.user.get_if_exists(uname):
            return uname

        user_data = User({
            "agrees_with_tos": "NOW",
            "classification": "RESTRICTED",
            "name": "Update Account",
            "password": get_password_hash(''.join(random.choices(string.ascii_letters, k=20))),
            "uname": uname,
            "type": ["signature_importer"]
        })
        self.datastore.user.save(uname, user_data)
        self.datastore.user_settings.save(uname, UserSettings())
        return uname


if __name__ == '__main__':
    ServiceUpdater().serve_forever()
