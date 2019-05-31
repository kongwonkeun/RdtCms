#
#
#
import platform
import sys
import os
import signal
import socket

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QLabel
from PySide2.QtCore import QTimer
from PySide2.QtCore import Qt

#===============================
#
#
def handler():
    app.quit()

#===============================
#
#
app = QApplication(sys.argv)
wind = app.desktop().screenGeometry()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('gmail.com', 80))
ip = s.getsockname()[0]
s.close()

signal.signal(signal.SIGINT, handler)

t = QTimer()
t.setSingleShot(True)
t.timeout.connect(handler)
t.start(10000)

url = QLabel()
url.setWindowFlags(Qt.FramelessWindowHint)
url.setGeometry(wind)
url.setAttribute(Qt.WA_DeleteOnClose, False)
url.setFocusPolicy(Qt.NoFocus)
url.setContextMenuPolicy(Qt.NoContextMenu)
url.setStyleSheet('background-color: black;')
url.setText('<font size=10 color=white>http://%s:8080</font>' % ip)
url.setAlignment(Qt.AlignCenter)
url.show()

sys.exit(app.exec_())

#
#
#