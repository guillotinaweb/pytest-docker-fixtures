from pprint import pformat
from pytest_docker_fixtures import images
from time import sleep

import docker
import os


class BaseImage:

    docker_version = '1.23'
    name = 'foobar'
    port = None
    host = ''
    base_image_options = dict(
        cap_add=['IPC_LOCK'],
        mem_limit='1g',
        environment={},
        privileged=True,
        detach=True,
        publish_all_ports=True)

    @property
    def image(self):
        return images.get_image(self.name)

    def get_image_options(self):
        image_options = self.base_image_options.copy()
        if 'environment' not in image_options:
            image_options['environment'] = {}
        for key, value in images.get_env(self.name).items():
            if value is None:
                if key in image_options['environment']:
                    del image_options['environment'][key]
            else:
                image_options['environment'][key] = value
        image_options.update(images.get_options(self.name))
        image_options['max_wait_s'] = images.get_max_wait_s(self.name)
        return image_options

    def get_port(self, port=None):
        if (os.environ.get('TESTING', '') == 'jenkins' or
                'TRAVIS' in os.environ):
            return port if port else self.port
        network = self.container_obj.attrs['NetworkSettings']
        service_port = '{0}/tcp'.format(port if port else self.port)
        for netport in network['Ports'].keys():
            if netport == '6543/tcp':
                continue

            if netport == service_port:
                return network['Ports'][service_port][0]['HostPort']

    def get_host(self):
        return self.container_obj.attrs['NetworkSettings']['IPAddress']

    def check(self):
        return True

    def run(self):
        docker_client = docker.from_env(version=self.docker_version)
        image_options = self.get_image_options()

        max_wait_s = image_options.pop('max_wait_s', None) or 30

        # Create a new one
        container = docker_client.containers.run(
            image=self.image,
            **image_options
        )
        ident = container.id
        count = 1

        self.container_obj = docker_client.containers.get(ident)

        opened = False

        print(f'starting {self.name}')
        while count < max_wait_s and not opened:
            if count > 0:
                sleep(1)
            count += 1
            try:
                self.container_obj = docker_client.containers.get(ident)
            except docker.errors.NotFound:
                print(f'Container not found for {self.name}')
                continue
            if self.container_obj.status == 'exited':
                logs = self.container_obj.logs()
                self.stop()
                raise Exception(f'Container failed to start {logs}')

            if self.container_obj.attrs['NetworkSettings']['IPAddress'] != '':
                if os.environ.get('TESTING', '') == 'jenkins':
                    network = self.container_obj.attrs['NetworkSettings']
                    self.host = network['IPAddress']
                else:
                    self.host = 'localhost'

            if self.host != '':
                opened = self.check()
        if not opened:
            logs = self.container_obj.logs().decode('utf-8')
            self.stop()
            raise Exception(
                f'Could not start {self.name}: {logs}\n'
                f'Image: {self.image}\n'
                f'Options:\n{pformat(image_options)}')
        print(f'{self.name} started')
        return self.host, self.get_port()

    def stop(self):
        if self.container_obj is not None:
            try:
                self.container_obj.kill()
            except docker.errors.APIError:
                pass
            try:
                self.container_obj.remove(v=True, force=True)
            except docker.errors.APIError:
                pass
