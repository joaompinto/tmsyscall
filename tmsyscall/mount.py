"""
Linux mount(2) API wrapper module.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
import logging
import os
import errno
import fnmatch

import ctypes
from ctypes import (
    c_int,
    c_char_p,
    c_ulong,
    c_void_p,
)
from ctypes.util import find_library

import enum
import six

from tmsyscall import utils

_LOGGER = logging.getLogger(__name__)

###############################################################################
# Map the C interface

_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)

if (not getattr(_LIBC, 'mount', None) or
        not getattr(_LIBC, 'umount', None) or
        not getattr(_LIBC, 'umount2', None)):
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)


# int mount(const char *source, const char *target,
#           const char *filesystemtype, unsigned long mountflags,
#           const void *data);
_MOUNT_DECL = ctypes.CFUNCTYPE(
    c_int,
    c_char_p,  # source
    c_char_p,  # target
    c_char_p,  # filesystem type
    c_ulong,   # mount flags
    c_void_p,  # data
    use_errno=True
)
_MOUNT = _MOUNT_DECL(('mount', _LIBC))


def _mount(source, target, fs_type, mnt_flags, data):
    res = _MOUNT(source, target, fs_type, mnt_flags, data)
    if res < 0:
        errno = ctypes.get_errno()
        raise OSError(
            errno, os.strerror(errno),
            'mount(%r, %r, %r, 0x%x, %r)' % (
                source,
                target,
                fs_type,
                mnt_flags,
                data
            )
        )

    return res


# int umount(const char *target);
_UMOUNT_DECL = ctypes.CFUNCTYPE(
    c_int,
    c_char_p,  # target
    use_errno=True
)
_UMOUNT = _UMOUNT_DECL(('umount', _LIBC))

# int umount2(const char *target, int flags);
_UMOUNT2_DECL = ctypes.CFUNCTYPE(
    c_int,
    c_char_p,  # target
    c_int,     # flags
    use_errno=True
)
_UMOUNT2 = _UMOUNT2_DECL(('umount2', _LIBC))


def _umount(target):
    """Umount ``target``.
    """
    res = _UMOUNT(target)
    if res < 0:
        errno = ctypes.get_errno()
        raise OSError(
            errno, os.strerror(errno),
            'umount(%r)' % (target, )
        )


def _umount2(target, flags=None):
    res = _UMOUNT2(target, flags)
    if res < 0:
        errno = ctypes.get_errno()
        raise OSError(
            errno, os.strerror(errno),
            'umount2(%r, %r)' % (target, flags)
        )


###############################################################################
# NOTE: below values taken from mount kernel interface sys/mount.h

class MSFlags(enum.IntEnum):
    """All mount flags.
    """
    #: MS_MGC_VAL is a flag marker, needs to be included in all calls.
    MGC_VAL = 0xC0ED0000

    #: Mount read-only.
    RDONLY = 0x000001
    #: Ignore suid and sgid bits.
    NOSUID = 0x000002
    #: Disallow access to device special files.
    NODEV = 0x000004
    #: Disallow program execution.
    NOEXEC = 0x000008
    #: Writes are synced at once.
    SYNCHRONOUS = 0x000010
    #: Alter flags of a mounted FS.
    REMOUNT = 0x000020
    #: Allow mandatory locks on an FS.
    MANDLOCK = 0x000040
    #: Directory modifications are synchronous.
    DIRSYNC = 0x000080
    #: Update atime relative to mtime/ctime
    RELATIME = 0x200000
    #: Do not update access times.
    NOATIME = 0x000400
    #: Do not update directory access times.
    NODIRATIME = 0x000800
    #: Bind a mount point to a different place .
    BIND = 0x001000
    #: Move a mount point to a different place .
    MOVE = 0x002000
    #: Recursively apply the UNBINDABLE, PRIVATE, SLAVE, or SHARED flags.
    REC = 0x004000

    # See https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt
    #
    #: unbindable mount
    UNBINDABLE = 0x020000
    #: private mount
    PRIVATE = 0x040000
    #: slave mount
    SLAVE = 0x080000
    #: shared mount
    SHARED = 0x100000


#: Mount flag marker.
MS_MGC_VAL = MSFlags.MGC_VAL

#: Mount read-only.
MS_RDONLY = MSFlags.RDONLY
#: Ignore suid and sgid bits.
MS_NOSUID = MSFlags.NOSUID
#: Disallow access to device special files.
MS_NODEV = MSFlags.NODEV
#: Disallow program execution.
MS_NOEXEC = MSFlags.NOEXEC
#: Writes are synced at once.
MS_SYNCHRONOUS = MSFlags.SYNCHRONOUS
#: Alter flags of a mounted FS.
MS_REMOUNT = MSFlags.REMOUNT
#: Allow mandatory locks on an FS.
MS_MANDLOCK = MSFlags.MANDLOCK
#: Directory modifications are synchronous.
MS_DIRSYNC = MSFlags.DIRSYNC
#: Update atime relative to mtime/ctime
MS_RELATIME = MSFlags.RELATIME
#: Do not update access times.
MS_NOATIME = MSFlags.NOATIME
#: Do not update directory access times.
MS_NODIRATIME = MSFlags.NODIRATIME
#: Bind a mount point to a different place .
MS_BIND = MSFlags.BIND
#: Move a mount point to a different place .
MS_MOVE = MSFlags.MOVE
#: Recursively apply the UNBINDABLE, PRIVATE, SLAVE, or SHARED flags.
MS_REC = MSFlags.REC

# See https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt
#: unbindable mount
MS_UNBINDABLE = MSFlags.UNBINDABLE
#: private mount
MS_PRIVATE = MSFlags.PRIVATE
#: slave mount
MS_SLAVE = MSFlags.SLAVE
#: shared mount
MS_SHARED = MSFlags.SHARED


class MNTFlags(enum.IntEnum):
    """All umount2 operations flags.
    """
    #: Force unmounting
    FORCE = 0x1
    #: Just detach from the tree
    DETACH = 0x2
    #: Mark for expiry
    EXPIRE = 0x4


#: Force unmounting
MNT_FORCE = MNTFlags.FORCE
#: Just detach from the tree
MNT_DETACH = MNTFlags.DETACH
#: Mark for expiry
MNT_EXPIRE = MNTFlags.EXPIRE


###############################################################################
# Main mount/umount functions

def mount(source, target, fs_type, mnt_flags=0, *mnt_opts_args, # pylint: disable=W1113
          **mnt_opts_kwargs):
    """Mount ``source`` on ``target`` using filesystem type ``fs_type`` and
    mount flags ``mnt_flags``.

    NOTE: Mount data argument is not supported.

    :params `str` source:
        What to mount
    :params `str` target:
        Where to mount it
    """
    if source is not None:
        source = source.encode()
    if target is not None:
        target = target.encode()
    else:
        target = source
    if fs_type is not None:
        fs_type = fs_type.encode()

    # Fix up mount options
    options = ','.join(
        itertools.chain(
            mnt_opts_args,
            (
                '%s=%s' % (key, value)
                for (key, value) in six.iteritems(mnt_opts_kwargs)
            )
        )
    )
    if options:
        options = options.encode()
    else:
        options = None

    _LOGGER.debug('mount(%r, %r, %r, %r, %r)',
                  source, target, fs_type,
                  utils.parse_mask(mnt_flags, MSFlags), options)


    return _mount(source, target, fs_type, mnt_flags, options)


def unmount(target, mnt_flags=0):
    """Umount ``target``.
    """
    target = target.encode()

    _LOGGER.debug('umount(%r, %r)',
                  target, utils.parse_mask(mnt_flags, MNTFlags))

    if not mnt_flags:
        return _umount(target)
    return _umount2(target, mnt_flags)

def mount_move(target, source):
    """Move a mount from one to a point to another.
    """
    return mount(source=source, target=target, fs_type=None, mnt_flags=[MS_MOVE])


def mount_bind(newroot, target, source=None, recursive=True, read_only=True):
    """Bind mounts `source` to `newroot/target` so that `source` is accessed
    when reaching `newroot/target`.

    If a directory, the source will be mounted using --rbind.
    """
    # Ensure root directory exists
    if not os.path.exists(newroot):
        raise Exception('Path %r does not exist' % newroot)

    if source is None:
        source = target

    target = utils.norm_safe(target)
    source = utils.norm_safe(source)

    # Make sure target directory exists.
    if not os.path.exists(source):
        raise Exception('Source path %r does not exist' % source)

    mnt_flags = [MS_BIND]

    # Use --rbind for directories and --bind for files.
    if recursive and os.path.isdir(source):
        mnt_flags.append(MS_REC)

    # Strip leading /, ensure that mount is relative path.
    while target.startswith('/'):
        target = target[1:]

    # Create mount directory, make sure it does not exists.
    target_fp = os.path.join(newroot, target)
    if os.path.isdir(source):
        utils.mkdir_safe(target_fp)
    else:
        utils.mkfile_safe(target_fp)

    res = mount(source=source, target=target_fp, fs_type=None, mnt_flags=mnt_flags)

    if res == 0 and read_only:
        res = mount(
            source=None, target=target_fp,
            fs_type=None, mnt_flags=MS_BIND | MS_RDONLY | MS_REMOUNT
        )

    return res


def mount_procfs(newroot, target='/proc'):
    """Mounts procfs on directory.
    """
    while target.startswith('/'):
        target = target[1:]

    mnt_flags = MS_NODEV | MS_NOEXEC | MS_NOSUID |MS_RELATIME

    return mount(
        source='proc',
        target=os.path.join(newroot, target),
        fs_type='proc',
        mnt_flags=mnt_flags,
    )


def mount_sysfs(newroot, target='/sys'):
    """Mounts mount_sysfs on directory.
    """
    while target.startswith('/'):
        target = target[1:]

    mnt_flags = MS_RDONLY | MS_NODEV | MS_NOEXEC | MS_NOSUID |MS_RELATIME

    return mount(
        source='sysfs',
        target=os.path.join(newroot, target),
        fs_type='sysfs',
        mnt_flags=mnt_flags,
    )


def mount_tmpfs(newroot, target, **mnt_opts):
    """Mounts directory on tmpfs.
    """
    while target.startswith('/'):
        target = target[1:]

    mnt_flags = MS_NODEV | MS_NOEXEC | MS_NOSUID, MS_RELATIME

    return mount(
        source='tmpfs',
        target=os.path.join(newroot, target),
        fs_type='tmpfs',
        mnt_flags=mnt_flags,
        **mnt_opts
    )

class MountEntry(object):
    """Mount table entry data.
    """

    __slots__ = (
        'source',
        'target',
        'fs_type',
        'mnt_opts',
        'mount_id',
        'parent_id'
    )

    def __init__(self, source, target, fs_type, mnt_opts, mount_id, parent_id):
        self.source = source
        self.target = target
        self.fs_type = fs_type
        self.mnt_opts = mnt_opts
        self.mount_id = int(mount_id)
        self.parent_id = int(parent_id)

    def __repr__(self):
        return (
            '{name}(source={src!r}, target={target!r}, '
            'fs_type={fs_type!r}, mnt_opts={mnt_opts!r})'
        ).format(
            name=self.__class__.__name__,
            src=self.source,
            target=self.target,
            fs_type=self.fs_type,
            mnt_opts=self.mnt_opts
        )

    def __lt__(self, other):
        """Ordering is based on mount target.
        """
        return self.target < other.target

    def __eq__(self, other):
        """Equality is defined as the equality of the mount entry's attributes.
        """
        res = (
            (self.mount_id == other.mount_id) and
            (self.parent_id == other.parent_id) and
            (self.source == other.source) and
            (self.target == other.target) and
            (self.fs_type == other.fs_type) and
            (self.mnt_opts == other.mnt_opts)
        )
        return res

    @classmethod
    def mount_entry_parse(cls, mount_entry_line):
        """
        Create a :class:`MountEntry` from a mountinfo data line.

        The file contains lines of the form:

            36 35 98:0 /mnt1 /mnt2 rw,noatime master:1
                                            - ext3 /dev/root rw,errors=continue
            (1)(2)(3)   (4)   (5)      (6)      (7)
                                           (8) (9)   (10)         (11)

        The numbers in parentheses are labels for the descriptions
        below:

            (1)  mount ID: a unique ID for the mount (may be reused after
                 umount(2)).

            (2)  parent ID: the ID of the parent mount (or of self for the
                 root of this mount namespace's mount tree).

                 If the parent mount point lies outside the process's root
                 directory (see chroot(2)), the ID shown here won't have a
                 corresponding record in mountinfo whose mount ID (field
                 1) matches this parent mount ID (because mount points
                 that lie outside the process's root directory are not
                 shown in mountinfo).  As a special case of this point,
                 the process's root mount point may have a parent mount
                 (for the initramfs filesystem) that lies outside the
                 process's root directory, and an entry for that mount
                 point will not appear in mountinfo.

            (3)  major:minor: the value of st_dev for files on this
                 filesystem (see stat(2)).

            (4)  root: the pathname of the directory in the filesystem
                 which forms the root of this mount.

            (5)  mount point: the pathname of the mount point relative to
                 the process's root directory.

            (6)  mount options: per-mount options.

            (7)  optional fields: zero or more fields of the form
                 "tag[:value]"; see below.

            (8)  separator: the end of the optional fields is marked by a
                 single hyphen.

            (9)  filesystem type: the filesystem type in the form
                 "type[.subtype]".

            (10) mount source: filesystem-specific information or "none".

            (11) super options: per-superblock options.

        """
        mount_entry_line = mount_entry_line.strip().split(' ')

        (
            mount_id,
            parent_id,
            _major_minor,
            _parent_path,
            target,
            mnt_opts
        ), data = mount_entry_line[:6], mount_entry_line[6:]

        fields = []
        while data[0] != '-':
            fields.append(data.pop(0))

        (
            _,
            fs_type,
            source,
            mnt_opts2
        ) = data

        mnt_opts = set(mnt_opts.split(',') + mnt_opts2.split(','))

        return cls(source, target, fs_type, mnt_opts, mount_id, parent_id)

def list_mounts():
    """Read the current process' mounts.
    """
    mounts = []

    try:
        with open('/proc/self/mountinfo', 'r') as mf:
            mounts_lines = mf.readlines()

    except EnvironmentError as err:
        if err.errno == errno.ENOENT:
            _LOGGER.warning('Unable to read "/proc/self/mounts": %s', err)
            return mounts
        else:
            raise

    for mounts_line in mounts_lines:
        mounts.append(MountEntry.mount_entry_parse(mounts_line))

    return mounts

###############################################################################
def cleanup_mounts(whitelist_patterns, ignore_exc=False):
    """Prune all mount points except whitelisted ones.

    :param ``bool`` ignore_exc:
        If True, proceed in a best effort, only logging when unmount fails.
    """
    _LOGGER.info('Removing all mounts except %r', whitelist_patterns)
    current_mounts = [mount_entry for mount_entry in list_mounts()]

    # We need to iterate over mounts in "layering" order.
    mount_parents = {}
    for mount_entry in current_mounts:
        mount_parents_item = mount_parents.get(mount_entry.parent_id, [])
        mount_parents_item.append(mount_entry.mount_id)
        mount_parents[mount_entry.mount_id] = mount_parents_item

    sorted_mounts = sorted(
        [
            (len(mount_parents.get(mount_entry.mount_id, [])), mount_entry)
            for mount_entry in current_mounts
        ],
        reverse=True
    )

    for _, mount_entry in sorted_mounts:
        is_valid = any(
            [
                mount_entry for whitelist_pat in whitelist_patterns
                if fnmatch.fnmatchcase(mount_entry.target, whitelist_pat)
            ]
        )
        if is_valid:
            _LOGGER.info('Mount preserved: %r', mount_entry)
        elif ignore_exc:
            try:
                unmount(mount_entry.target)
            except OSError as err:
                _LOGGER.warning('Failed to umount %r: %s',
                                mount_entry.target, err)
        else:
            unmount(mount_entry.target)



__all__ = [
    'MNT_DETACH',
    'MNT_EXPIRE',
    'MNT_FORCE',
    'MS_BIND',
    'MS_DIRSYNC',
    'MS_MANDLOCK',
    'MS_MGC_VAL',
    'MS_MOVE',
    'MS_NOATIME',
    'MS_NODEV',
    'MS_NODIRATIME',
    'MS_NOEXEC',
    'MS_NOSUID',
    'MS_PRIVATE',
    'MS_RDONLY',
    'MS_REC',
    'MS_REMOUNT',
    'MS_SHARED',
    'MS_SLAVE',
    'MS_SYNCHRONOUS',
    'MS_UNBINDABLE',
    'MountEntry',
    'cleanup_mounts',
    'mount',
    'mount_procfs',
    'unmount'
]
