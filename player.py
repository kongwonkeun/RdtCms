#
#
#
import sys

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtWidgets import QToolBar, QMenu, QSlider, QAction, QStyle
from PySide2.QtWidgets import QDialog, QFileDialog
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtCore import SLOT, QStandardPaths, Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        toolBar = QToolBar()
        self.addToolBar(toolBar)
        playIcon = self.style().standardIcon(QStyle.SP_MediaPlay)
        previousIcon = self.style().standardIcon(QStyle.SP_MediaSkipBackward)
        nextIcon = self.style().standardIcon(QStyle.SP_MediaSkipForward)
        pauseIcon = self.style().standardIcon(QStyle.SP_MediaPause)
        stopIcon = self.style().standardIcon(QStyle.SP_MediaStop)

        self.playAction = toolBar.addAction(playIcon, "Play")
        self.previousAction = toolBar.addAction(previousIcon, "Previous")
        self.nextAction = toolBar.addAction(nextIcon, "Next")
        self.pauseAction = toolBar.addAction(pauseIcon, "Pause")
        self.stopAction = toolBar.addAction(stopIcon, "Stop")
        self.playAction.triggered.connect(self.player.play)
        self.previousAction.triggered.connect(self.previousClicked)
        self.nextAction.triggered.connect(self.playlist.next)
        self.pauseAction.triggered.connect(self.player.pause)
        self.stopAction.triggered.connect(self.player.stop)

        self.volSlider = QSlider()
        self.volSlider.setOrientation(Qt.Horizontal)
        self.volSlider.setMinimum(0)
        self.volSlider.setMaximum(100)
        self.volSlider.setFixedWidth(120)
        self.volSlider.setValue(self.player.volume())
        self.volSlider.setTickInterval(10)
        self.volSlider.setTickPosition(QSlider.TicksBelow)
        self.volSlider.setToolTip("Volume")
        self.volSlider.valueChanged.connect(self.player.setVolume)
        toolBar.addWidget(self.volSlider)

        openAction = QAction(QIcon.fromTheme("document-open"), "&Open...", self, shortcut=QKeySequence.Open, triggered=self.open)
        exitAction = QAction(QIcon.fromTheme("application-exit"), "E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        playMenu = self.menuBar().addMenu("&Play")
        playMenu.addAction(self.playAction)
        playMenu.addAction(self.previousAction)
        playMenu.addAction(self.nextAction)
        playMenu.addAction(self.pauseAction)
        playMenu.addAction(self.stopAction)
        aboutMenu = self.menuBar().addMenu("&About")
        aboutMenu.addAction(aboutQtAct)

        self.videoWidget = QVideoWidget()
        self.setCentralWidget(self.videoWidget)

        self.player.setPlaylist(self.playlist);
        self.player.stateChanged.connect(self.updateButtons)
        self.player.setVideoOutput(self.videoWidget);
        self.updateButtons(self.player.state())

    def open(self):
        fileDialog = QFileDialog(self)
        supportedMimeTypes = ["video/mp4", "*.*"]
        fileDialog.setMimeTypeFilters(supportedMimeTypes)
        moviesLocation = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        fileDialog.setDirectory(moviesLocation)
        if fileDialog.exec_() == QDialog.Accepted:
            self.playlist.addMedia(fileDialog.selectedUrls()[0])
            self.player.play()

    def previousClicked(self):
        if self.player.position() <= 5000:
            self.playlist.previous();
        else:
            player.setPosition(0);

    def updateButtons(self, state):
        mediaCount = self.playlist.mediaCount()
        self.playAction.setEnabled(mediaCount > 0
            and state != QMediaPlayer.PlayingState)
        self.pauseAction.setEnabled(state == QMediaPlayer.PlayingState)
        self.stopAction.setEnabled(state != QMediaPlayer.StoppedState)
        self.previousAction.setEnabled(self.player.position() > 0)
        self.nextAction.setEnabled(mediaCount > 1)

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())

#
#
#
