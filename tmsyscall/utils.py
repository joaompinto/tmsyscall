"""Useful utility functions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import logging

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


__all__ = [
    'get_iterable',
    'parse_mask'
]
