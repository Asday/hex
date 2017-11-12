import os


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, '../version.txt'), 'r') as f:
    # <release.feature.commit>
    __version__ = f.read().strip()
