from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QHBoxLayout, QVBoxLayout, QApplication, QAbstractItemView, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt
from pathlib import Path
import sys
import os

def getGameName(gameid,path):
    with open(os.path.join(path,"appmanifest_" + gameid + ".acf")) as f:
        content = f.readlines()
        for line in content:
            if line.find('"name"') != -1:
                l = line.split("\t")
                name = l[3].replace("\n","")[1:-1]
    return name

def searchProtonGames(path):
    for v in os.listdir(os.path.join(path,"compatdata")):
        if (os.path.isfile(os.path.join(path,"compatdata",v,"pfx","system.reg")) and os.path.isfile(os.path.join(path,"compatdata",v,"version"))):
            tmp = {}
            tmp["name"] = getGameName(v,path)
            tmp["gamepath"] = os.path.join(path,"compatdata",v,"pfx")
            filehandle = open(os.path.join(path,"compatdata",v,"version"),"r")
            version,_ = filehandle.read().split("-")
            filehandle.close()
            tmp["protonpath"] = os.path.join(path,"common","Proton " + version,"dist","bin","wine")
            gamelist.append(tmp)

class MainWindow(QWidget):
    def setup(self):
        self.gameTable = QTableWidget(0, 1)
        self.openWinecfgButton = QPushButton("Open winecfg")
        self.openRegeditButton = QPushButton("Open regedit")

        self.openWinecfgButton.clicked.connect(self.openWinecfgClicked)
        self.openRegeditButton.clicked.connect(self.openRegeditClicked)

        self.gameTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.gameTable.setHorizontalHeaderLabels(("Proton Games",""))
        self.gameTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.gameTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.gameTable.verticalHeader().hide()
        self.gameTable.setShowGrid(False)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.openWinecfgButton)
        self.buttonLayout.addWidget(self.openRegeditButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.gameTable)
        self.mainLayout.addLayout(self.buttonLayout)

        self.addGames()
        self.setLayout(self.mainLayout)
        self.setWindowTitle("jdProtonHelper")
        self.show()

    def addGames(self):
        count = 0
        for item in gamelist:
            gameItem = QTableWidgetItem(item["name"])
            gameItem.setFlags(gameItem.flags() ^ Qt.ItemIsEditable)
            self.gameTable.insertRow(count)
            self.gameTable.setItem(count, 0, gameItem) 
            count += 1

    def disableAll(self):
        self.gameTable.setEnabled(False)
        self.openWinecfgButton.setEnabled(False)
        self.openRegeditButton.setEnabled(False)

    def enableAll(self):
        self.gameTable.setEnabled(True)
        self.openWinecfgButton.setEnabled(True)
        self.openRegeditButton.setEnabled(True)

    def openWinecfgClicked(self):
        prog = gamelist[self.gameTable.currentRow()]
        self.disableAll()
        os.system('WINEPREFIX="' + prog["gamepath"] + '" "'+ prog["protonpath"] + '" winecfg')
        self.enableAll()

    def openRegeditClicked(self):
        prog = gamelist[self.gameTable.currentRow()]
        self.disableAll()
        os.system('WINEPREFIX="' + prog["gamepath"] + '" "'+ prog["protonpath"] + '" regedit')
        self.enableAll()

def main():
    global gamelist
    gamelist = []
    searchProtonGames(os.path.join(str(Path.home()),".steam","steam","steamapps"))
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setup()
    sys.exit(app.exec_())
