"""
Classes inherited from Matplotlib's PatchCollection and LineCollection classes. The set of patches/lines to draw are
often dynamically changing, and so these derived classes allow for automatic updating.
"""
from matplotlib import collections


class UpdatablePatchCollection(collections.PatchCollection):
    def __init__(self, patches, *args, **kwargs):
        self.patches = patches
        collections.PatchCollection.__init__(self, patches, *args, **kwargs)

    def get_paths(self):
        self.set_paths(self.patches)
        return self._paths


class UpdatableLineCollection(collections.LineCollection):
    def __init__(self, lines, *args, **kwargs):
        self.lines = lines
        collections.LineCollection.__init__(self, lines, *args, **kwargs)

    def get_paths(self):
        self.set_paths(self.lines)
        return self._paths
