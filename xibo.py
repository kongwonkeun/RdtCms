#
#

import signal
import sys
import os
import argparse

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer

import ui
import config

#===============================
#
#
if __name__ == '__main__':

    config_file = 'config.json'
    parser = argparse.ArgumentParser(
        description = ""
    )
    parser.add_argument(
        '-c',
        '--config',
        default = config_file,
        help = 'configuration file, default is %s' % config_file
    )
    arg = parser.parse_args()
    app = QApplication(sys.argv)
    win = app.desktop().screenGeometry()
    cfg = config.XiboConfig(arg.config)

    signal.signal(signal.SIGINT, lambda s, f: app.quit())

    if  not os.path.isfile(arg.config):
        print('')
        print('the configuration file %s is not exists.' % arg.config)
        print('creating default configuration ...')
        cfg.save()
        print('please edit the "%s" file and then rerun xibopy again.' % arg.config)
        print('')
        sys.exit(0)

    r = -1
    with ui.XiboWindow(cfg) as w:
        t = QTimer()
        t.setSingleShot(True)
        t.timeout.connect(w.showFullScreen)
        t.start(1000)
        w.setGeometry(win)
        w.show()
        r = app.exec_()
        print('exiting, please wait ...')

    sys.exit(r)

#
# EOF