#! env python
#
import sys
import os.path

import imp

class LSSTImporter:
    """An importer to go on sys.meta_path that enables you to
    find a sub-module anywhere on sys.path, regardless of where its parent
    module was loaded from (requires python 2.5; cf PEP 302).

    More precisely, this importer is not restricted to loading a sub-module
    from a subdirectory of the directory where its parent module was loaded
    from.  Thus, if your sys.path contains multiple directories that contain
    an "lsst" module, then a submodule "lsst.foo" can appear below any of 
    those directories.
    """

    def __init__(self):
        self.isLSSTImporter = True 
        pass

    def find_module(self, fullname, path = None):
        """Find a module in the search path"""

        name = fullname.split(".")[-1]

        for d in sys.path:
            dirname = os.path.join(d, apply(os.path.join, fullname.split(".")))
                                            
            if os.path.isabs(dirname) and os.path.isdir(dirname):
                (fd, filename, desc) = \
                           imp.find_module(name, [os.path.dirname(dirname)])
                return LSSTLoader(fd, filename, desc)

        return None

class LSSTLoader:

    def __init__(self, fd, filename, desc):
        self._fd = fd
        self._filename = filename
        self._desc = desc

    def load_module(self, fullname):
        """Load a module, using the information from an importer's
        find_module"""
        fd = self._fd;             self._fd = None
        filename = self._filename; self._filename = None
        desc = self._desc;         self._desc = None

        return imp.load_module(fullname, fd, filename, desc)

# Ensure that duplicate allocations--particularly those related to RTTI--are
# resolved by setting dynamical library loading flags.
RTLD_GLOBAL = -1
RTLD_NOW = -1
try:
    import dl
    if hasattr(dl, 'RTLD_GLOBAL'):  RTLD_GLOBAL = dl.RTLD_GLOBAL
    if hasattr(dl, 'RTLD_NOW'):     RTLD_NOW    = dl.RTLD_NOW
except ImportError:
    # 64bit linux does not have a dl module...
    pass
except SystemError:
    # ...if it does it should throw a SystemError
    pass

if RTLD_GLOBAL < 0:
    import lsst64defs
    RTLD_GLOBAL = lsst64defs.RTLD_GLOBAL   # usually 0x00100
if RTLD_NOW < 0:
    import lsst64defs
    RTLD_NOW = lsst64defs.RTLD_NOW         # usually 0x00002

dlflags = RTLD_GLOBAL|RTLD_NOW
if dlflags != 0:
    sys.setdlopenflags(dlflags)


# we update the meta_path last to guard agaist failures in the above code
# (like failing to import the lsst64defs module)
#
sys.meta_path += [LSSTImporter()]

