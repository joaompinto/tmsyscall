# Syscall
Provide a python library for some "advanced" Linux syscalls, based on https://github.com/Morgan-Stanley/treadmill/tree/master/lib/python/treadmill/syscall .

The following requirements motivate a fork:
- Provide an independent python package for the syscall features
- Add Python2.7 support
- Add documentation and examples
- Add tests

## Credits

#
Upsteam project: https://github.com/Morgan-Stanley/treadmill

# Initial setup
Inital code base was setup with:

```
git clone https://github.com/joaompinto/python-package-skeleton
mv python-package-skeleton tmsyscall
cd tmsyscall/ && rm -rf .git && git init

RELEASE_ID="3.7/2018.05.04-1.tar.gz"
TMPFILE=/tmp/release.tar.gz
wget https://github.com/Morgan-Stanley/treadmill/archive/$RELEASE_ID -O $TMPFILE
tar -C /tmp -xvf $TMPFILE
cp -avp /tmp/treadmill-*/lib/python/treadmill/syscall tmsyscall
cp -avp /tmp/treadmill-*/LICENSE* .
echo "0.0.0" > tmsyscall/version
git add .
git commit -a -m "Initial commit"
```