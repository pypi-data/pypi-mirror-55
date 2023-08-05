import base64
import docker
import pickle

from constellation.config_util import \
    config_build, \
    config_string, \
    read_yaml
from constellation.docker_util import \
    string_from_container, \
    string_into_container


class ConstellationMetaConfiguration:
    """Developer-written configuration for a configuration"""
    def __init__(self, name, basename, container, container_path=None,
                 default_container_prefix=None):
        self.name = name
        self.basename = basename
        self.container = container
        if not container_path:
            container_path = "/{}.yml".format(basename)
        self.container_path = container_path
        self.default_container_prefix = default_container_prefix


class ConstellationConfiguration:
    def __init__(self, path, meta):
        self.meta = meta
        self.path = path
        self.data = read_yaml("{}/{}.yml".format(path, meta.basename))
        self.container_prefix = container_prefix(self.data, meta)

    def build(self, extra=None, options=None):
        return config_build(self.path, self.data, extra, options)

    def fetch(self):
        cl = docker.client.from_env()
        try:
            container = cl.containers.get(self.name_persist())
        except docker.errors.NotFound:
            return None
        txt = string_from_container(container, self.meta.container_path)
        return pickle.loads(base64.b64decode(txt))

    def save(self, data):
        cl = docker.client.from_env()
        container = cl.containers.get(self.name_persist())
        txt = base64.b64encode(pickle.dumps(data)).decode("utf8")
        string_into_container(txt, container, self.meta.container_path)

    def name_persist(self):
        return "{}_{}".format(self.container_prefix, self.meta.container)


def container_prefix(data, meta):
    default = meta.default_container_prefix
    required = default is None
    given = config_string(data, ["docker", "container_prefix"], required)
    return given or meta.default_container_prefix
