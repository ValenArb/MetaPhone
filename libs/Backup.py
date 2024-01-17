import os
import shutil
import subprocess
import pyudev

source_dir = '/home/peima/FTP/test'
recordings_dir = '/home/peima/FTP/test/recordings'

context = pyudev.Context()

monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')

for device in iter(monitor.poll, None):
    if device.action == 'add' and device.get('ID_FS_TYPE') == 'vfat':
        target_dir = device.get('DEVNAME')
        shutil.copy(recordings_dir, target_dir)
        files = os.listdir(target_dir)
        if "variables.py" in files:
            source_files = os.listdir(source_dir)
            if "variables.py" in source_files:
                file = os.join(source_dir, "variables.py")
                os.remove(file)
            path = os.join(target_dir, "variables.py")
            shutil.move(path, source_dir)