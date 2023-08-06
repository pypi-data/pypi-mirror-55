"""
    This software is a part of backupmystemusb2usb and its functionality is to
    backup one usb key to another usb with the same sapce disk
    Author: Stéphane Bressani <s.bressani@bluewin.ch>
"""
from subprocess import Popen, CalledProcessError
from datetime import datetime
from . import const

UUID = const.UUID
DEVICE = const.DEVICE


class e2label:
    def __init__(self, blkid, log):
        self.blkid = blkid
        self.log = log

    def write_time_stamp_label_to_master(self):
        """
        Write time stamp label to master
        """
        global DDOUTPUT
        now = datetime.now()
        dt_string = now.strftime('"%Y%m%d%H%M%S"')
        self.log.add_log(const.TTY_E2LABEL_WTSLTM % (self.blkid.master[DEVICE],
                                                     dt_string))
        x = 'sudo e2label %s1 "%s"'
        try:
            cmd_list = ['sudo', 'e2label', self.blkid.master[DEVICE],
                        dt_string]
            cmd = Popen(cmd_list)
            cmd.wait()
            DDOUTPUT = cmd.communicate()[0]
            self.log.add_log(DDOUTPUT)
        except CalledProcessError:
            self.log.add_log(const.ERR_E2LABEL_WTSLTM)
            xx = x % (self.blkid.master[DEVICE], dt_string)
            self.log.add_log(const.ERR_CMD % (xx))
