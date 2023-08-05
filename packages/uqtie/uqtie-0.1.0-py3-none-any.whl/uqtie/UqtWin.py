#!/usr/bin/python
#
# PyQt5 Application Main Window base class that does basic things that most of my GUI apps need.
#

from __future__      import print_function
import sys, os, argparse

from PyQt5.QtCore    import Qt, QSettings
from PyQt5.QtWidgets import QWidget, QApplication, QAction, QMainWindow

class MainWindow(QMainWindow):

    def __init__(self, parsedArgs, **kwargs ):
        super(MainWindow, self).__init__()

        # Save the app so we can change its stylesheet
        if 'app' in kwargs:
            self.app = kwargs['app']

        # Create a QSettings. Qt stores this using your organization name and your application name
        # to determine the correct place for your user and their operating system
        # (linux: ~/.config/Craton/SomeApp)
        if 'organizationName' in kwargs and 'appName' in kwargs:
            self.settings = QSettings(kwargs['organizationName'], kwargs['appName'])
            
            dirname = os.path.dirname(self.settings.fileName())
            
            #self.styleFile='big-dark-orange.stylesheet'
            self.styleFile = dirname + '/' + kwargs['appName'] + '.qss'
            try:
                with open(self.styleFile,'r') as fh:
                    self.app.setStyleSheet(fh.read())
            except:
                pass

        appName = ''
        title = ''
        if 'appName' in kwargs:
            appName = kwargs['appName']
        if 'title' in kwargs:
            title = kwargs['title']

        if title == '':
            title = appName

        self.setupBaseUi( title )

    def setupBaseMenus(self):
        # Create Menu Bar
        self.menuBar = self.menuBar()

        # Create Root Menus
        self.fileMenu = self.menuBar.addMenu('File')   

        # Set up our handling of file menu
        self.fileMenu.triggered.connect(self.fileMenuSelected)

        # Create Actions for menus
        self.quitAction = QAction('Quit', self)
        self.quitAction.setShortcut('Ctrl+Q')

        # Add actions to Menus
        self.fileMenu.addAction(self.quitAction)
        self.quitAction.triggered.connect(self.onQuit)

        # Events
        #self.fileMenu.triggered.connect(self.selected)


    def setupBaseUi(self, title ):
        self.setupBaseMenus()
        centralWindow = QWidget()
        self.setCentralWidget(centralWindow)

        # Restore the geometry from settings, default to an empty string
        geometry = self.settings.value('geometry', '')
        if geometry:
            self.restoreGeometry(geometry)

        self.setWindowTitle(title)
        
    def saveGeometryOnQuit(self):
        # Get and save the geometry
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)

    def onQuit(self):
        self.saveGeometryOnQuit()
        #self.app.quit()

    def closeEvent(self, event):
        # This is called whenever a window is closed when you hit the upper right X on the window,
        # call the same function we call for handling CTRL-Q or File Menu->Quit
        self.saveGeometryOnQuit()

        # Pass the event to the class we inherit from
        super(MainWindow, self).closeEvent(event)

    def fileMenuSelected(self, q):
        #print(q.text() + ' selected')
        if q.text() == 'Save':
            if self.currentFileName:
                # just perform the save
                self.saveFileDialog()
            else:
                # put up the Save file dialog
                self.saveFileDialog()
                pass
        elif q.text() == 'New':
            # What does New mean?
            pass
        elif q.text() == 'Save As':
            # Similar to New I guess
            pass
        elif q.text() == 'Open':
            # Put up the Open File Dialog
            pass

## Test Code:
# Class that demonstrates deriving a class from MainWindow
class TestAppMainWindow(MainWindow):

    def __init__(self, parsedArgs, **kwargs ):
        #print ( 'TestAppMainWindow.init() : parsedArgs: {a}'.format(a=parsedArgs) )
        #print ( 'TestAppMainWindow.init() : parsedArgs.test: {a}'.format(a=parsedArgs.test) )
        super(TestAppMainWindow, self).__init__(parsedArgs, **kwargs)
        self.show()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--test', help='Test Argument placeholder', default='Test')
    parsedArgs,unparsedArgs = parser.parse_known_args()

    # Pass unparsed args to Qt, might have some X Windows args, like --display
    qtArgs = sys.argv[:1] + unparsedArgs
    app = QApplication(qtArgs)

    mainw = TestAppMainWindow(parsedArgs, app=app, organizationName='Craton', appName='honker', title='Hoonker' )

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
