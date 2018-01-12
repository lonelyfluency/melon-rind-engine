#coding=utf8
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from graph_reco import *

class MyBrowser(QWidget):

    def __init__(self, parent = None):
        super(MyBrowser, self).__init__(parent)
        self.createLayout()
        self.createConnection()

    def search(self):
        address = str(self.addressBar.text())
        if address:
            if address.find('://') == -1:
                address = 'http://' + address
            url = QUrl(address)
            self.webView.load(url)

    def record(self):
        os.system('python record1.py')

    def record2(self):
        os.system('python record2.py')

    def graphReco(self):
        absolute_path = QFileDialog.getOpenFileName(self,'Open file')
        print str(absolute_path)
        pred_list = graph_reco(str(absolute_path))
        print pred_list

        oout = open('graph_result.txt','w')
        oout.write(pred_list[0].encode('utf8'))
        oout.close()
        self.addressBar.setText(pred_list[0])

    def createLayout(self):
        self.setWindowTitle("dada's browser")

        self.addressBar = QLineEdit()
        self.goButton = QPushButton("&GO")
        self.voiceButton = QPushButton("&REGISTER")
        self.logButton = QPushButton("&LOGIN")
        self.graphButton = QPushButton("&GRAPH")

        bl = QHBoxLayout()
        bl.addWidget(self.addressBar)
        bl.addWidget(self.voiceButton)
        bl.addWidget(self.logButton)
        bl.addWidget(self.goButton)
        bl.addWidget(self.graphButton)

        self.webView = QWebView()

        layout = QVBoxLayout()
        layout.addLayout(bl)
        layout.addWidget(self.webView)

        self.setLayout(layout)

    def createConnection(self):
        self.connect(self.addressBar, SIGNAL('returnPressed()'), self.search)
        self.connect(self.addressBar, SIGNAL('returnPressed()'), self.addressBar, SLOT('selectAll()'))
        self.connect(self.goButton, SIGNAL('clicked()'), self.search)
        self.connect(self.goButton, SIGNAL('clicked()'), self.addressBar, SLOT('selectAll()'))
        self.connect(self.voiceButton, SIGNAL('clicked()'), self.record)
        self.connect(self.logButton, SIGNAL('clicked()'), self.record2)
        self.connect(self.graphButton, SIGNAL('clicked()'), self.graphReco)

app = QApplication(sys.argv)

browser = MyBrowser()
browser.show()

sys.exit(app.exec_())