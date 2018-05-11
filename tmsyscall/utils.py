"""Useful utility functions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import logging
import os.path
import errno
import six

_LOGGER = logging.getLogger(__name__)

def get_iterable(obj):
    """Gets an iterable from either a list or a single value.
    """
    if obj is None:
        return ()

    if (isinstance(obj, collections.Iterable) and
            not isinstance(obj, six.string_types)):
        return obj

    return (obj,)


def parse_mask(value, mask_enum):
    """Parse a mask into indivitual mask values from enum.

    :params ``int`` value:
        (Combined) mask value.
    :params ``enum.IntEnum`` mask_enum:
        Enum of all possible mask values.
    :returns:
        ``list`` - List of enum values and optional remainder.
    """
    masks = []
    for mask in mask_enum:
        if value & mask:
            masks.append(mask.name)
            value ^= mask
    if value:
        masks.append(hex(value))

    return masks

def norm_safe(path):
    """Returns normalized path, aborts if path is not absolute.
    """
    if not os.path.isabs(path):
        raise Exception(path, 'Not absolute path: %r' % path)

    return os.path.normpath(path)

def mkdir_safe(path, mode=0o777):
    """Creates directory, if there is any error, aborts the process.

    :param ``str`` path:
        Path to the directory to create. All intermediary folders will be
        created.
    :return ``Bool``:
        ``True`` - if the directory was created.
        ``False`` - if the directory already existed.
    """
    try:
        os.makedirs(path, mode=mode)
        return True
    except OSError as err:
        # If dir already exists, no problem. Otherwise raise
        if err.errno == errno.EEXIST and os.path.isdir(path):
            return False
        else:
            raise


__all__ = [
    'get_iterable',
    'norm_safe',
    'parse_mask',
    'mkdir_safe'
]
