"""Module that manages and loads modules"""
import pkg_resources

MODULE_ENTRYPOINT_KEY = 'skytemple.module'


class Modules:
    _modules = {}

    @classmethod
    def load(cls):
        # Look up package entrypoints for modules
        cls._modules = {
            entry_point.name:
                entry_point.load() for entry_point in pkg_resources.iter_entry_points(MODULE_ENTRYPOINT_KEY)
        }
        dependencies = {}
        for k, module in cls._modules.items():
            dependencies[k] = module.depends_on()
        resolved_deps = dep(dependencies)
        cls._modules = dict(sorted(cls._modules.items(), key=lambda x: resolved_deps.index(x[0])))

    @classmethod
    def all(cls):
        """Returns a list of all loaded modules, ordered by dependencies"""
        return cls._modules


def dep(arg):
    """
    Dependency resolver

    "arg" is a dependency dictionary in which
    the values are the dependencies of their respective keys.

    Source: http://code.activestate.com/recipes/576570-dependency-resolver/

    Copyright: Louis RIVIERE
    Original license: MIT
    """
    d = dict((k, set(arg[k])) for k in arg)
    r = []
    while d:
        # values not in keys (items without dep)
        t = set(i for v in d.values() for i in v)-set(d.keys())
        # and keys without value (items without dep)
        t.update(k for k, v in d.items() if not v)
        # can be done right away
        r.append(t)
        # and cleaned up
        d = dict(((k, v-t) for k, v in d.items() if v))
    return [item for s in r for item in s]
