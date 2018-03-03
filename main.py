from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from threading import Thread, currentThread, Event
from time import sleep 
 
class Textlogger(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.i = 0
        self.timestr = self.timestamp()
        self.createLogFile("", self.timestr)
        self.limitLogFiles()
 
    logResult = pyqtSignal(str, arguments=['log'])

    @pyqtSlot(str)
    def log(self, arg):
        if self.i == 2:
            self.createLogFile(arg, self.timestr)
            self.i = 0
        else:
            self.i = self.i + 1

    @pyqtSlot(str)
    def clean(self, arg):
        if arg == "":
            import os

            cwd = os.getcwd()
            path = cwd + "/logs/"

            os.remove(path + self.timestr + '.log')
        else:
            self.createLogFile(arg, self.timestr)

    def timestamp(self):
        import time

        timestr = time.strftime("%Y%m%d-%H%M%S")
        return timestr

    def createLogFile(self, arg, timestr):
        f = open('logs/' + timestr + '.log', 'w')
        f.write(arg)

    def limitLogFiles(self):
        import os

        cwd = os.getcwd()
        path = cwd + "/logs/"
        max_Files = 5
        
        def sorted_ls(path):
            mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
            return list(sorted(os.listdir(path), key=mtime))
        
        del_list = sorted_ls(path)[0:(len(sorted_ls(path))-max_Files)]
        
        for dfile in del_list:
            os.remove(path + dfile)
 
if __name__ == "__main__":
    import sys
 
    # Create an instance of the application
    app = QGuiApplication(sys.argv)
    # Set window icon
    app.setWindowIcon(QIcon("note.png"))
    # Create QML engine
    engine = QQmlApplicationEngine()
    # Create a textlogger object
    textlogger = Textlogger()
    # And register it in the context of QML
    engine.rootContext().setContextProperty("textlogger", textlogger)
    # Load the qml file into the engine
    engine.load("main.qml")
 
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
