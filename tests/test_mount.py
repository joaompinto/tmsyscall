from tmsyscall.mount import mount, unmount, list_mounts
from tempfile import mkdtemp
from shutil import rmtree

def test_list_mounts():
    mount_info = [x for x in list_mounts() if x.target == '/proc']
    assert len(mount_info) == 1
    mount_info = mount_info[0]
    assert mount_info.fs_type == 'proc'


def test_mount():
    tmp_dir = mkdtemp()
    mount("/proc", tmp_dir, "proc")

    # Search for target
    mount_info = [x for x in list_mounts() if x.target == tmp_dir]
    assert len(mount_info) == 1
    mount_info = mount_info[0]

    assert mount_info.source == '/proc'
    assert mount_info.mnt_opts == set(['relatime', 'rw'])
    assert mount_info.fs_type == 'proc'

    unmount(tmp_dir)
    mount_info = [x for x in list_mounts() if x.target == tmp_dir]
    mount_record = [x for x in list_mounts() if x.target == tmp_dir]
    assert not mount_record
    rmtree(tmp_dir)
