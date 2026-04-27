import importlib as _importlib
import sys as _sys


def _register(alias, package_name):
    try:
        mod = _importlib.import_module(package_name)
        _sys.modules[f"imap.{alias}"] = mod
        setattr(_sys.modules[__name__], alias, mod)
    except ImportError:
        raise 


_register("imap_processing", "imap_processing")
_register("imap_l3_processing", "imap_l3_processing")
_register("imap_data_access", "imap_data_access")
_register("sds_data_manager", "sds_data_manager")
