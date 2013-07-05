#!/usr/bin/env python

"""
editor.py - A Ravenskull level editor.

Copyright (C) 2013 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ravenskull import Ravenskull
import UEFfile

__version__ = "0.1"

class LevelWidget(QWidget):

    def __init__(self, game_info, parent = None):
    
        QWidget.__init__(self, parent)
        
        self.game_info = game_info
        
        self.tw = game_info.tile_width
        self.th = game_info.tile_height
        
        self.xs = 2
        self.ys = 1
        
        self.rows = 64
        self.columns = 64
        
        self.levels = []
        self.items = []
        self.level_number = 1
        self.currentTile = 0
        self.highlight = None
        
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        
        self.pen = QPen(Qt.white)
        self.pen.setWidth(2)
        self.pen.setJoinStyle(Qt.RoundJoin)
        self.pen.setCapStyle(Qt.RoundCap)
        
        self.setMouseTracking(True)
        
        self.loadImages()
        self.loadLevels()
    
    def loadImages(self):
    
        self.tile_images = {}
        
        palette = map(lambda x: qRgb(*x), self.game_info.palette(self.level_number))
        
        for number, sprite in self.game_info.read_sprites().items():
        
            image = QImage(sprite, self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.tile_images[number] = image
    
    def loadLevels(self):
    
        self.levels, self.items = self.game_info.read_levels()
    
    def setTileImages(self, tile_images):
    
        self.tile_images = tile_images
    
    def clearLevel(self):
    
        for row in range(self.rows):
            for column in range(self.columns):
                self.writeTile(column, row, self.currentTile)
    
    def setLevel(self, number):
    
        self.level_number = number
        self.loadImages()
        
        self.update()
    
    def mousePressEvent(self, event):
    
        r = self._row_from_y(event.y())
        c = self._column_from_x(event.x())
        
        if event.button() == Qt.LeftButton:
            self.writeTile(c, r, self.currentTile)
        elif event.button() == Qt.MiddleButton:
            self.writeTile(c, r, 0)
        else:
            event.ignore()
    
    def mouseMoveEvent(self, event):
    
        r = self._row_from_y(event.y())
        c = self._column_from_x(event.x())
        
        if event.buttons() & Qt.LeftButton:
            self.writeTile(c, r, self.currentTile)
        elif event.buttons() & Qt.MiddleButton:
            self.writeTile(c, r, 0)
        else:
            event.ignore()
    
    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(Qt.black))
        
        painter.setPen(self.pen)
        
        y1 = event.rect().top()
        y2 = event.rect().bottom()
        x1 = event.rect().left()
        x2 = event.rect().right()
        
        r1 = max(0, self._row_from_y(y1))
        r2 = max(0, self._row_from_y(y2))
        c1 = self._column_from_x(x1)
        c2 = self._column_from_x(x2)
        
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
            
                tile = self.levels[self.level_number - 1][r][c]
                tile_image = self.tile_images[tile]
                
                painter.drawImage(c * self.tw * self.xs, r * self.th * self.ys,
                                  tile_image)
                
                if (63 - r, c - 3) in self.items[self.level_number - 1]:
                    painter.drawLine(c * self.tw * self.xs, r * self.th * self.ys,
                                     (c + 1) * self.tw * self.xs - 1, (r + 1) * self.th * self.ys - 1)
                    painter.drawLine(c * self.tw * self.xs, (r + 1) * self.th * self.ys - 1,
                                     (c + 1) * self.tw * self.xs - 1, r * self.th * self.ys)
        
        painter.end()
    
    def sizeHint(self):
    
        return QSize(self.columns * self.tw * self.xs, self.rows * self.th * self.ys)
    
    def _row_from_y(self, y):
    
        return y/(self.th * self.ys)
    
    def _column_from_x(self, x):
    
        return x/(self.tw * self.xs)
    
    def _y_from_row(self, r):
    
        return r * self.th * self.ys
    
    def _x_from_column(self, c):
    
        return c * self.tw * self.xs
    
    def updateCell(self, c, r):
    
        self.update(QRect(self._x_from_column(c), self._y_from_row(r),
              self.tw * self.xs, self.th * self.ys))
    
    def writeTile(self, c, r, tile):
    
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return
        
        self.levels[self.level_number - 1][r][c] = tile
        self.updateCell(c, r)


class EditorWindow(QMainWindow):

    def __init__(self, game_info):
    
        QMainWindow.__init__(self)
        
        self.xs = 2
        self.ys = 1
        
        self.tw = game_info.tile_width
        self.th = game_info.tile_height
        
        self.game_info = game_info
        
        self.path = ""
        
        self.levelWidget = LevelWidget(game_info)
        
        self.createToolBars()
        self.createMenus()
        
        # Select the first tile in the tiles toolbar and the first level in the
        # levels menu.
        self.tileGroup.actions()[0].trigger()
        self.levelsGroup.actions()[0].trigger()
        
        area = QScrollArea()
        area.setWidget(self.levelWidget)
        self.setCentralWidget(area)
    
    def saveAs(self):
    
        path = QFileDialog.getSaveFileName(self, self.tr("Save As"),
                                           self.path, self.tr("UEF files (*.uef)"))
        if not path.isEmpty():
        
            if self.saveLevels(unicode(path)):
                self.path = path
                self.setWindowTitle(self.tr(path))
            else:
                QMessageBox.warning(self, self.tr("Save Levels"),
                    self.tr("Couldn't write the new executable to %1.\n").arg(path))
    
    def saveLevels(self, path):
    
        # Write the levels back to the UEF file.
        self.game_info.write_levels(self.levelWidget.levels)
        
        # Write the new UEF file.
        u = UEFfile.UEFfile(creator = 'Ravenskull Editor ' + __version__)
        u.minor = 6
        u.target_machine = "Electron"
        
        files = map(lambda x: (x["name"], x["load"], x["exec"], x["data"]),
                    self.game_info.uef.contents)
        
        u.import_files(0, files, gap = True)
        
        try:
            u.write(path, write_emulator_info = False)
            return True
        except UEFfile.UEFfile_error:
            return False
    
    def createToolBars(self):
    
        self.tileGroup = QActionGroup(self)
        
        collection = [range(0, 16)]
        toolbar_areas = [Qt.TopToolBarArea]
        titles = [self.tr("Tiles")]
        
        for symbols, area, title in zip(collection, toolbar_areas, titles):
        
            tilesToolBar = QToolBar(title)
            self.addToolBar(area, tilesToolBar)
            
            for symbol in symbols:
            
                icon = QIcon(QPixmap.fromImage(self.levelWidget.tile_images[symbol]))
                action = tilesToolBar.addAction(icon, str(symbol))
                action.setData(QVariant(symbol))
                action.setCheckable(True)
                self.tileGroup.addAction(action)
                action.triggered.connect(self.setCurrentTile)
    
    def createMenus(self):
    
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        
        newAction = fileMenu.addAction(self.tr("&New"))
        newAction.setShortcut(QKeySequence.New)
        
        saveAsAction = fileMenu.addAction(self.tr("Save &As..."))
        saveAsAction.setShortcut(QKeySequence.SaveAs)
        saveAsAction.triggered.connect(self.saveAs)
        
        quitAction = fileMenu.addAction(self.tr("E&xit"))
        quitAction.setShortcut(self.tr("Ctrl+Q"))
        quitAction.triggered.connect(self.close)
        
        editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        clearAction = editMenu.addAction(self.tr("&Clear"))
        clearAction.triggered.connect(self.clearLevel)
        
        levelsMenu = self.menuBar().addMenu(self.tr("&Levels"))
        self.levelsGroup = QActionGroup(self)
        
        for i in range(len(self.levelWidget.levels)):
            levelAction = levelsMenu.addAction(str(i + 1))
            levelAction.setData(QVariant(i + 1))
            levelAction.setCheckable(True)
            self.levelsGroup.addAction(levelAction)
        
        levelsMenu.triggered.connect(self.selectLevel)
    
    def setCurrentTile(self):
    
        self.levelWidget.currentTile = self.sender().data().toInt()[0]
    
    def selectLevel(self, action):
    
        number = action.data().toInt()[0]
        self.levelWidget.highlight = None
        self.setLevel(number)
    
    def setLevel(self, number):
    
        self.levelWidget.setLevel(number)
        
        # Also change the sprites in the toolbar.
        for action in self.tileGroup.actions():
        
            symbol = action.data().toInt()[0]
            icon = QIcon(QPixmap.fromImage(self.levelWidget.tile_images[symbol]))
            action.setIcon(icon)
    
    def clearLevel(self):
    
        answer = QMessageBox.question(self, self.tr("Clear Level"),
            self.tr("Clear the current level?"), QMessageBox.Yes | QMessageBox.No)
        
        if answer == QMessageBox.Yes:
            self.levelWidget.clearLevel()
    
    def sizeHint(self):
    
        levelSize = self.levelWidget.sizeHint()
        menuSize = self.menuBar().sizeHint()
        scrollBarSize = self.centralWidget().verticalScrollBar().size()
        
        return QSize(max(levelSize.width(), menuSize.width(), levelSize.width()),
                     levelSize.height() + menuSize.height() + scrollBarSize.height())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    if len(app.arguments()) < 2:
    
        sys.stderr.write("Usage: %s <UEF file>\n" % app.arguments()[0])
        app.quit()
        sys.exit(1)
    
    game_info = Ravenskull(app.arguments()[1])
    
    window = EditorWindow(game_info)
    window.show()
    sys.exit(app.exec_())
