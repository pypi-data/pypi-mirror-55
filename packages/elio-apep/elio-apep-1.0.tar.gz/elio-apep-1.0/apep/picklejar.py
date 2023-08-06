"""**Usage**::

    from apep.picklejar import PickleJar
    data = ['Mango'] # or {} or ''
    chutney_pj = PickleJar('projectpath/appfolder/optionalfolder', 'cucumber')
    chutney_pj.pickle(data)

    # Muck about with the current data.
    data = chutney_pj.open([])
    data += ['Clove', 'Cinnamon', 'Pepper']

    # Repickle it.
    chutney_pj.pickle(data)"""
# -*- coding: utf-8 -*-
import os
import pickle


class PickleJar:
    """A convenient wrapper for pickling data, handling os/read/write"""

    DEFAULT = {}

    def __init__(self, jarpath, jarname):
        """Set path names to the picklejar by name."""
        self.jarname = jarname
        self.jarpath = jarpath
        if not os.path.exists(self.jarpath):
            os.makedirs(self.jarpath, exist_ok=True)
        self.jarfile = f"{jarname}.pickle"
        self.picklejar = os.path.join(self.jarpath, self.jarfile)

    @property
    def ripe(self):
        """Check for picklejar."""
        return os.path.exists(self.picklejar)

    def wipe(self):
        """Wipe old."""
        if self.ripe:
            os.remove(self.picklejar)

    def pickle(self, data):
        """Store the data."""
        with open(self.picklejar, "wb") as fp:
            pickle.dump(data, fp)
        return data

    def open(self, default=DEFAULT):
        """Read the data."""
        if not self.ripe:
            return self.pickle(default)
        with open(self.picklejar, "rb") as fp:
            return pickle.load(fp)
