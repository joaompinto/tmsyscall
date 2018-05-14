from __future__ import print_function
from tmsyscall.unshare import unshare, CLONE_NEWPID, CLONE_NEWNS
from tmsyscall.mount import  mount, mount_procfs, unmount
from tmsyscall.mount import MS_SLAVE, MS_REC, MS_BIND, MS_PRIVATE, MNT_DETACH
from tmsyscall.pivot_root import pivot_root
from os.path import exists
import os

def test_unshare():

    container_root = '/home/janito/containers/'

    # Detach from the system-wide mount table
    # cleanup_mounts([container_root + '*'], ignore_exc=True)

    # We unshare (change) the pid namespace here, and other namespaces after
    # the exec, because if we exec'd in the new mount namespace, it would open
    # files in the new namespace's root, and prevent us from umounting the old
    # root after pivot_root. Note that changing the pid namespace affects only
    # the children (namely, which namespace they will be put in). It is thread
    # safe because unshare() affects the calling thread only.
    unshare(CLONE_NEWPID|CLONE_NEWNS)
    oldroot = os.path.join(container_root, 'host')
    if not exists(oldroot):
        os.makedirs(oldroot)
    mount('none', "/", None, MS_REC | MS_PRIVATE)
    mount(container_root, container_root, None, MS_BIND | MS_REC)
    os.chdir(container_root)
    pivot_root('.', 'mnt')
    unmount('mnt', MNT_DETACH)
    os.chroot('.')
    mount_procfs("/proc")
    os.execl('/bin/bash', 'ls')
    unmount(container_root)

    print("We are ok nout")
