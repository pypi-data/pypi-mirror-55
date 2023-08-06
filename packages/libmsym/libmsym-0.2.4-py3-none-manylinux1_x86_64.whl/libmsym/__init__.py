__all__ = []

_libmsym_install_location = None

__version__ = '0.2.4'


def export(defn):
    globals()[defn.__name__] = defn
    __all__.append(defn.__name__)
    return defn

from . import main as libmsym

def get_version():
    return __version__
