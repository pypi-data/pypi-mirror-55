"""
    This software is a part of backupmystemusb2usb and its functionality is to
    backup one usb key to another usb with the same space disk
    Author: Stéphane Bressani <s.bressani@bluewin.ch>
"""
from subprocess import Popen, CalledProcessError
from . import const

DEVICE = const.DEVICE


class umount:
    def __init__(self, blkid, log):
        self.blkid = blkid
        self.log = log
        self.__umount()

    def __umount(self):
        """
        Umount disks
        """
        self.log.add_log(const.TTY_UMOUNT % (self.blkid.master[DEVICE],
                                        self.blkid.slave[DEVICE]))
        x = 'sudo umount %s'
        try:
            xx = x % (self.blkid.master[DEVICE])
            cmd_list = ['sudo', 'umount', self.blkid.master[DEVICE]]
            cmd = Popen(cmd_list)
            cmd.wait()
            xx = x % (self.blkid.slave[DEVICE])
            cmd_list = ['sudo', 'umount', self.blkid.slave[DEVICE]]
            cmd = Popen(cmd_list)
            cmd.wait()
        except CalledProcessError:
            self.log.add_log(const.ERR_UMOUNT)
            self.log.add_log(const.ERR_CMD % (xx))
