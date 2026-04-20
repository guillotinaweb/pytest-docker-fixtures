from pprint import pformat
from pytest_docker_fixtures import images
from time import sleep

import docker
import os
import re
import socket

DOCKER_HOST_TCP_FORMAT = re.compile(r'^tcp://(\d+\.\d+\.\d+\.\d+)(?::\d+)?$')


def _network_settings(container_attrs):
    return container_attrs.get('NetworkSettings') or {}


def _container_ipv4_from_inspect(container_attrs, default_network='bridge'):
    """
    Return the container's IPv4 from docker inspect if present.

    Docker Engine versions differ: some expose NetworkSettings.IPAddress,
    newer ones only Networks[<net>].IPAddress (and the bridge name may vary).
    """
    ns = _network_settings(container_attrs)
    legacy = (ns.get('IPAddress') or '').strip()
    if legacy:
        return legacy
    networks = ns.get('Networks') or {}
    if default_network in networks:
        ip = (networks[default_network].get('IPAddress') or '').strip()
        if ip:
            return ip
    for _name, net in networks.items():
        ip = (net.get('IPAddress') or '').strip()
        if ip:
            return ip
    return ''


def _published_ports(container_attrs):
    ns = _network_settings(container_attrs)
    return ns.get('Ports') or {}


def _client_host_from_env():
    """
    Return the host a client on this machine should use to reach the container.

    Honours ``DOCKER_HOST=tcp://<ip>[:port]`` for remote Docker instances,
    falling back to ``localhost`` otherwise.
    """
    match = DOCKER_HOST_TCP_FORMAT.match(os.environ.get('DOCKER_HOST', ''))
    return match.group(1) if match else 'localhost'


class BaseImage:

    docker_version = 'auto'
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
    default_network = 'bridge'

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
        network = _network_settings(self.container_obj.attrs)
        ports = network.get('Ports') or {}
        service_port = '{0}/tcp'.format(port if port else self.port)
        for netport in ports.keys():
            if netport == '6543/tcp':
                continue

            if netport == service_port:
                return ports[service_port][0]['HostPort']

    def get_host(self):
        if self.host:
            return self.host
        attrs = getattr(self.container_obj, 'attrs', {}) or {}
        return (_container_ipv4_from_inspect(attrs, self.default_network)
                or 'localhost')

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

            attrs = self.container_obj.attrs
            container_ip = _container_ipv4_from_inspect(attrs, self.default_network)
            ports = _published_ports(attrs)
            has_ports = bool(ports)

            self.host = ''
            if container_ip:
                if os.environ.get('TESTING', '') == 'jenkins':
                    self.host = container_ip
                else:
                    self.host = _client_host_from_env()
            elif has_ports:
                # No legacy / bridge IP in inspect (common on recent Docker
                # Desktop / user-defined networks) but ports are published —
                # service is reachable on the host.
                self.host = _client_host_from_env()

            if self.host:
                try:
                    self.host = socket.gethostbyname(self.host)
                except socket.gaierror:
                    pass

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
            self.container_obj = None
