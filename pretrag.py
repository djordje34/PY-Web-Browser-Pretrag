import os
import sys
import time

import psutil
import qdarktheme
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


# main window
class MainWindow(QMainWindow):
    
    def defineNavButton(self,icon,text,info,graphic=1):
            if graphic:
                btn = QAction(icon,text, self)
                btn.setStatusTip(info)
            else:
                btn = QAction(text, self)
                btn.setStatusTip(info)
            return btn
        
    # constructor
    def __init__(self, icons):
        
        
        self.start_time = time.time()
        
        super(MainWindow, self).__init__()
 
        # creating a tab widget
        self.tabs = QTabWidget()
        self.showMaximized()
        # making document mode true
        self.tabs.setDocumentMode(True)
 
        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
 
        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)
 
        # making tabs closeable
        self.tabs.setTabsClosable(True)
 
        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
 
        # making tabs as central widget
        self.setCentralWidget(self.tabs)
 
        # creating a status bar
        self.status = QStatusBar()
 
        # setting status bar to the main window
        self.setStatusBar(self.status)
 
        # creating a tool bar for navigation
        self.navtb = QToolBar("Navigation")
 
        # adding tool bar tot he main window
        self.addToolBar(self.navtb)
 
        # creating back action
        back_btn=self.defineNavButton(icons["back_dark"],"Back","Back to previous page")
 
        # setting status tip
 
        # adding action to back button
        # making current tab to go back
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
 
        # adding this to the navigation tool bar
        self.navtb.addAction(back_btn)
 
        # similarly adding next button
        next_btn=self.defineNavButton(icons["forward_dark"],"Forward","Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.navtb.addAction(next_btn)
 
        # similarly adding reload button
        reload_btn=self.defineNavButton(icons["reload"],"Reload","Reload page")

        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        self.navtb.addAction(reload_btn)
 
        # creating home action
        home_btn=self.defineNavButton(icons["home_dark"],"Home","Go home")

 
        # adding action to home button
        home_btn.triggered.connect(self.navigate_home)
        self.navtb.addAction(home_btn)
 
        # adding a separator
        self.navtb.addSeparator()
 
        # creating a line edit widget for URL
        self.urlbar = QLineEdit()
 
        # adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)
 
        # adding line edit to tool bar
        self.navtb.addWidget(self.urlbar)
        pctg = psutil.virtual_memory()[2]
        
        
        

        
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)
        
        ntime = time.gmtime(time.time() - self.start_time)
        self.vreme = self.defineNavButton("",f"Време: {time.strftime('%H:%M:%S',ntime)}",f"{ntime}",graphic=0)
        self.navtb.addAction(self.vreme) 
        
        
        self.ram = self.defineNavButton("",f"РАМ меморија: {pctg}%",f"{pctg}",graphic=0)
        self.navtb.addAction(self.ram)
        
        
        # similarly adding stop action
        self.stop_btn=self.defineNavButton(icons["stop"],"Stop","Stop loading current page")
        self.stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(self.stop_btn)
 
        # creating first tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')
 
        # showing all the components
        self.show()
 
        # setting window title
        self.setWindowTitle("ПРЕТРАГ")

    def updateTime(self):
        ntime = time.gmtime(time.time() - self.start_time)
        if self.vreme:
            self.navtb.removeAction(self.vreme)
        self.vreme = self.defineNavButton("",f"Време: {time.strftime('%H:%M:%S',ntime)}",f"{ntime}",graphic=0)
        self.navtb.addAction(self.vreme)    
        
        if self.ram:
            self.navtb.removeAction(self.ram)
        pctg = psutil.virtual_memory()[2]
        self.ram = self.defineNavButton("",f"РАМ меморија: {pctg}%",f"{pctg}",graphic=0)
        self.navtb.addAction(self.ram)
        
        if self.stop_btn:
            self.navtb.removeAction(self.stop_btn)
        self.stop_btn=self.defineNavButton(icons["stop"],"Stop","Stop loading current page")
        self.stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(self.stop_btn)
        
            
    # method for adding new tab
    def add_new_tab(self, qurl = None, label ="Blank"):
 
        # if url is blank
        if qurl is None:
            # creating a google url
            qurl = QUrl('http://www.google.com')
 
        # creating a QWebEngineView object
        browser = QWebEngineView()
 
        # setting url to browser
        browser.setUrl(qurl)
 
        # setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
 
        # adding action to the browser when url is changed
        # update the url
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
 
        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
 
        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_new_tab()
 
    # when tab is changed
    def current_tab_changed(self, i):
 
        # get the curl
        qurl = self.tabs.currentWidget().url()
 
        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())
 
        # update the title
        self.update_title(self.tabs.currentWidget())
 
    # when tab is closed
    def close_current_tab(self, i):
 
        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return
 
        # else remove the tab
        self.tabs.removeTab(i)
 
    # method for updating the title
    def update_title(self, browser):
 
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return
 
        # get the page title
        title = self.tabs.currentWidget().page().title()
 
        # set the window title
        self.setWindowTitle("% s - ПРЕТРАГ" % title)
 
    # action to go to home
    def navigate_home(self):
 
        # go to google
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))
 
    # method for navigate to url
    def navigate_to_url(self):
 
        # get the line edit text
        # convert it to QUrl object
        q = QUrl(self.urlbar.text())
 
        # if scheme is blank
        if q.scheme() == "":
            # set scheme
            q.setScheme("http")
 
        # set the url
        self.tabs.currentWidget().setUrl(q)
 
    # method to update the url
    def update_urlbar(self, q, browser = None):
 
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
 
            return
 
        # set text to the url bar
        self.urlbar.setText(q.toString())
 
        # set cursor position
        self.urlbar.setCursorPosition(0)
 
# creating a PyQt5 application
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
app.setStyleSheet(qdarktheme.load_stylesheet())

app.setApplicationName("ПРЕТРАГ")
app.setWindowIcon(icons["logo"])
# creating MainWindow object
window = MainWindow(icons)
 
# loop
app.exec_()