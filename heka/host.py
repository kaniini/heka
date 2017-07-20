from .apkbuild import APKBuildalike


class Host(APKBuildalike):
    """An object representing a host.  Hosts can contain references to roles,
    package lists, and provide a policy object containing settings.

    The host-level policy object is authoritative for that host, and host-specific
    config derivations will eventually override other configuration packages using
    the APK replaces field (not implemented yet)."""

    def __init__(self, hostname: str, roles: set=set(), packages: set=set(), policy: dict=dict()):
        self.hostname = hostname
        self.roles = roles
        self.packages = packages
        self.policy = policy

    @property
    def packagename(self) -> str:
        return 'host-' + self.hostname

    def get_role_packages(self) -> set:
        role_packages = set()
        for i in self.roles:
            if i[0] != '!':
                role_packages.add('role-' + i)
            else:
                role_packages.add('!role-' + i[1:])
        return role_packages

    def get_depends(self) -> set:
        return self.get_role_packages() | {x for x in self.packages}


if __name__ == '__main__':
    h = Host('petrie',
             roles={'desktop', 'openssh-server', '!server'}, 
             packages={'mate-desktop-environment', '!systemd'})
    print(h.render())
