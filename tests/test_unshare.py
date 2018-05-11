from tmsyscall.unshare import *
from tmsyscall.mount import *
import os

def test_unshare():

    container_root = '/tmp/x'

    # Detach from the system-wide mount table
    # cleanup_mounts([container_root + '*'], ignore_exc=True)

    # We unshare (change) the pid namespace here, and other namespaces after
    # the exec, because if we exec'd in the new mount namespace, it would open
    # files in the new namespace's root, and prevent us from umounting the old
    # root after pivot_root. Note that changing the pid namespace affects only
    # the children (namely, which namespace they will be put in). It is thread
    # safe because unshare() affects the calling thread only.
    unshare(CLONE_NEWPID)
    #mount_procfs(container_root)
    os.execl('/bin/bash', 'bash')

    print("We are ok nout")
