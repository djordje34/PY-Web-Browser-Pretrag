
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

# creating main window class



class MainWindow(QMainWindow):  #QIcon(os.path.join('icons','arrow-circle-315.png'))
 
 
 
    def defineNavButton(self,icon,text,info,graphic=1):
        if graphic:
            btn = QAction(icon,text, self)
            btn.setStatusTip(info)
        else:
            btn = QAction(icon, self)
            btn.setStatusTip(info)
        return btn
    
    
    def addNavButtonAction(self,btn,functions,hasF=1):
        if hasF:
            btn.triggered.connect(functions)

            
        self.navtb.addAction(btn)
        
        
    def setURLBar(self):
        urlbar = QLineEdit()
        urlbar.returnPressed.connect(self.navigateToURL)
        return urlbar
    
    
    
    def updateTitle(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - ПРЕТРАГ" % title)
 
 
    # method called by the home action
    def navigateHome(self):
 
        # open the google
        self.browser.setUrl(QUrl("https://www.google.com"))
 
    # method called by the line edit when return key is pressed
    def navigateToURL(self):
 
        # getting url and converting it to QUrl object
        q = QUrl(self.urlbar.text())
 
        # if url is scheme is blank
        if q.scheme() == "":
            # set url scheme to html
            q.setScheme("https")
 
        # set the url to the browser
        self.browser.setUrl(q)
 
    # method for updating url
    # this method is called by the QWebEngineView object
    def updateURLBar(self, q):
 
        # setting text to the url bar
        self.urlbar.setText(q.toString())
 
        # setting cursor position of the url bar
        self.urlbar.setCursorPosition(0)
        
    def setHomePage(self,link):
        self.browser.setUrl(QUrl(link))
        self.browser.urlChanged.connect(self.updateURLBar)
        # adding action when loading is finished
        self.browser.loadFinished.connect(self.updateTitle)
        self.setCentralWidget(self.browser)
        
    def setTabNavBar(self):
        tabs = QTabWidget()
 
        # making document mode true
        tabs.setDocumentMode(True)
 
        # adding action when double clicked
        tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
 
        # adding action when tab is changed
        tabs.currentChanged.connect(self.current_tab_changed)
 
        # making tabs closeable
        tabs.setTabsClosable(True)
 
        # adding action when tab close is requested
        tabs.tabCloseRequested.connect(self.close_current_tab)
        
        
        self.setCentralWidget(self.tabs)
        
        return tabs
    # constructor
    def __init__(self, icons):
        super(MainWindow, self).__init__()
        
 
        # creating a QWebEngineView
        self.browser = QWebEngineView()
 
        self.setCentralWidget(self.browser)
        self.showMaximized()
        
        # setting default browser url as google
        self.setHomePage(QUrl("https://google.com"))
        # adding action when url get changed
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        # creating QToolBar for navigation
        self.navtb = QToolBar("Navigation")
        self.navtb.addSeparator()
        # adding this tool bar tot he main window
        self.addToolBar(self.navtb)
 
        # adding actions to the tool bar
        # creating a action for back
        
        back_btn=self.defineNavButton(icons["back_dark"],"Back","Back to previous page")
        self.addNavButtonAction(back_btn,self.browser.back)

        next_btn=self.defineNavButton(icons["forward_dark"],"Forward","Forward to next page")
        self.addNavButtonAction(next_btn,self.browser.forward)

        reload_btn=self.defineNavButton(icons["reload"],"Reload","Reload page")
        self.addNavButtonAction(reload_btn,self.browser.reload)
        
        home_btn=self.defineNavButton(icons["home_dark"],"Home","Go home")
        self.addNavButtonAction(home_btn,self.navigateHome)
 
        # adding a separator in the tool bar
        self.navtb.addSeparator()
 
        # creating a line edit for the url
        self.urlbar = self.setURLBar()
        # adding this to the tool bar
        self.navtb.addWidget(self.urlbar)
 
         
        stop_btn=self.defineNavButton(icons["stop"],"Stop","Stop loading current page")#stop btn
        self.addNavButtonAction(stop_btn,self.browser.stop)
        
 
        # showing all the components
        self.show()
 
 
    # method for updating the title of the window
    def updateTitle(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - ПРЕТРАГ" % title)
 
 
    # method called by the home action
    def navigateHome(self):
 
        # open the google
        self.browser.setUrl(QUrl("https://www.google.com"))
 
    # method called by the line edit when return key is pressed
    def navigateToURL(self):
 
        # getting url and converting it to QUrl object
        q = QUrl(self.urlbar.text())
 
        # if url is scheme is blank
        if q.scheme() == "":
            # set url scheme to html
            q.setScheme("https")
 
        # set the url to the browser
        self.browser.setUrl(q)
 
    # method for updating url
    # this method is called by the QWebEngineView object
    def updateURLBar(self, q):
 
        # setting text to the url bar
        self.urlbar.setText(q.toString())
 
        # setting cursor position of the url bar
        self.urlbar.setCursorPosition(0)
 
def main():
# creating a pyQt5 application
    app = QApplication(sys.argv)
    
    icons={
        "back_light":QIcon(os.path.join('icons','back_light.png')),
        "back_dark":QIcon(os.path.join('icons','back_dark.png')),
        "forward_light":QIcon(os.path.join('icons','forward_light.png')),
        "forward_dark":QIcon(os.path.join('icons','forward_dark.png')),
        "reload":QIcon(os.path.join('icons','refresh.png')),
        "home_light":QIcon(os.path.join('icons','home_light.png')),
        "home_dark":QIcon(os.path.join('icons','home_dark.png')),
        "stop":QIcon(os.path.join('icons','stop.png')),
        "logo":QIcon(os.path.join('icons','pretragnobg.png')),
            }
    
    # setting name to the application
    app.setApplicationName("ПРЕТРАГ")
    app.setWindowIcon(icons["logo"])
    # creating a main window object
    window = MainWindow(icons)
    
    # loop
    app.exec_()
    
if __name__=="__main__":
    main()