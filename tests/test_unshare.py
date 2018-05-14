from __future__ import print_function
from tmsyscall.unshare import unshare, CLONE_NEWPID, CLONE_NEWNS
from tmsyscall.mount import  mount, mount_procfs, unmount, list_mounts
from tmsyscall.mount import MS_SLAVE, MS_REC, MS_BIND, MS_PRIVATE, MNT_DETACH
from tmsyscall.pivot_root import pivot_root
from os.path import exists
import os
from glob import glob
from tempfile import mkdtemp
from pprint import pprint

def test_unshare():

    unshare(CLONE_NEWPID)
    child_pid = os.fork()
    tmp_dir = mkdtemp()
    if child_pid == 0:
        assert os.getpid() == 1
        unshare(CLONE_NEWNS)
        mount("tmpfs", tmp_dir, "tmpfs", 0, "size=16m")
        mount_info = [x for x in list_mounts() if x.target == tmp_dir]
        assert mount_info
    else:
        pid, status = os.waitpid(child_pid, 0)
        mount_info = [x for x in list_mounts() if x.target == tmp_dir]
        assert not mount_info
