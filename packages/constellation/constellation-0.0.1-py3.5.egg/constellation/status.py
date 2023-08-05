import docker

class ConstellationStatus:
    def __init__(self, path, meta):
        self.path = path
        self.meta = meta
        self.reload()

    def __str__(self):
        if self.cannot_read_status:
        if self.cannot_read_status:
            return ("Cannot read status from {} because it has not " +
                    "started successfully or is in an error state.").format(
                        self.meta.name)
        if not self.is_running:
            return "<not running>"
        st_c = dict_map(self.containers, format_container)
        st_v = dict_map(self.volumes, format_volume)
        st_n = "Network: {}".format(self.network)
        ret = ["{} status:".format(self.meta.name)]
        if st_c:
            ret += ["Containers:"] + st_c
        if st_v:
            ret += ["Volumes:"] + st_v
        ret += [st_n]
        return "\n".join(ret)

    def __repr__(self):
        return self.__str__()

    def reload(self):
        cfg_base = read_config(self.path)
        try:
            cfg = cfg_base.fetch()
            self.cannot_read_status = False
        except docker.errors.NotFound:
            cfg = None
            self.cannot_read_status = True

        self.is_running = bool(cfg)
        if self.is_running:
            cl = docker.client.from_env()
            self.containers = {k: container_status(cl, v)
                               for k, v in cfg.containers.items()}
            self.volumes = cfg.volumes
            self.network = cfg.network
        else:
            self.containers = {}
            self.volumes = {}
            self.network = None


def format_container(role, status):
    return "  {}: {} ({})".format(role, status["status"], status["name"])


def format_volume(role, name):
    return "  {}: {}".format(role, name)


def container_status(client, name):
    try:
        status = client.containers.get(name).status
    except docker.errors.NotFound:
        status = "missing"
    return {"name": name, "status": status}


def dict_map(x, f):
    return [f(k, x[k]) for k in sorted(x.keys())]
