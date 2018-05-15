tmsyscall
=========

`tmsyscall` is a python library wrapper for some Linux kernel system calls.

It is based in the code from Morgan-Stanley's `threadmill project <https://github.com/Morgan-Stanley/treadmill>`_.

This library can help you:

 * List mounted filesystems
 * Mount/unmount filesystems
 * Unshare linux namespaces (man unshare)
 * Move the root filesystem of the current process  (man privot_root)

Sections
========
.. toctree::
   :maxdepth: 2

   mount_api
   unshare_api
   pivot_root_api
   Example
