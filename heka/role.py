from .apkbuild import APKBuildalike


class Role(APKBuildalike):
    """An object representing a role.  Roles can contain references to other roles,
    package lists, and provide a policy object containing settings.

    The role-level policy object is authoritative for that role, and role-specific
    config derivations will eventually override other configuration packages using
    the APK replaces field (not implemented yet)."""

    def __init__(self, rolename: str, roles: set=set(), packages: set=set(), policy: dict=dict()):
        self.rolename = rolename
        self.roles = roles
        self.packages = packages
        self.policy = policy

    @property
    def packagename(self) -> str:
        return 'role-' + self.rolename

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
    r = Role('desktop',
             roles={'x11', 'display-manager', 'gnome'},
             packages={'!kdm'})
    print(r.render())
