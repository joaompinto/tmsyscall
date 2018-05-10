from tmsyscall.mount import mount, unmount
from tempfile import mkdtemp

def test_mount_umount():
    tmp_dir = mkdtemp()
    mount("/proc", tmp_dir, "proc")
    with open("/proc/self/mountinfo") as mount_file:
        mount_info = mount_file.read().splitlines()
    # Search for target
    mount_record = [x for x in mount_info if x.split()[4] == tmp_dir]
    assert len(mount_record) == 1
    mount_record = mount_record[0].split()
    # parent
    assert mount_record[3] == '/'
    # options
    assert mount_record[5] == 'rw,relatime'
    # fstype
    assert mount_record[8] == 'proc'
    # source
    assert mount_record[9] == '/proc'
    unmount(tmp_dir)
    with open("/proc/self/mountinfo") as mount_file:
        mount_info = mount_file.read().splitlines()
    mount_record = [x for x in mount_info if x.split()[4] == tmp_dir]
    assert not mount_record
