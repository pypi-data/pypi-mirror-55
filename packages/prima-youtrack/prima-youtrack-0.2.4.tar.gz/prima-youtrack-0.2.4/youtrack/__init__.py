from youtrack.config import __version__

version = str(__version__).split('.')
if len(version) < 4:
    version = __version__
else:
    if version[3].lower().startswith('dev'):
        version = __version__
    else:
        version = '{} build {}'.format('.'.join(version[:3]), version[3])

from youtrack.youtrack import *  # noqa
