from __future__ import print_function
from tmsyscall.unshare import unshare, CLONE_NEWPID, CLONE_NEWNS
from tmsyscall.mount import mount, list_mounts
import os
from tempfile import mkdtemp

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
        _, _ = os.waitpid(child_pid, 0)
        mount_info = [x for x in list_mounts() if x.target == tmp_dir]
        assert not mount_info
