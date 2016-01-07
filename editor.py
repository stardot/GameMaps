#!/usr/bin/env python

"""
editor.py - A Clogger level editor.

Copyright (C) 2015 David Boddie <david@boddie.org.uk>

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

import UEFfile

from Clogger.levels import Levels
from Clogger.sprites import Sprites, Puzzle

__version__ = "0.2"

class EditorWidget(QWidget):

    xs = 2
    ys = 1
    
    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
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
    
        self.paint(self, event.rect())
    
    def paint(self, device, rect):
    
        painter = QPainter()
        painter.begin(device)
        painter.fillRect(rect, QBrush(Qt.black))
        
        painter.setPen(self.pen)
        
        y1 = rect.top()
        y2 = rect.bottom()
        x1 = rect.left()
        x2 = rect.right()
        
        r1 = max(0, self._row_from_y(y1))
        r2 = max(0, self._row_from_y(y2))
        c1 = self._column_from_x(x1)
        c2 = self._column_from_x(x2)
        
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
            
                tile_image = self.readTile(c, r)
                
                if tile_image:
                    painter.drawImage(c * self.tw * self.xs, r * self.th * self.ys,
                                      tile_image)
        
        painter.end()
    
    def saveImage(self, path):
    
        image = QImage(self.sizeHint(), QImage.Format_RGB16)
        self.paint(image, QRect(QPoint(0, 0), image.size()))
        return image.save(path)
    
    def updateCell(self, c, r):
    
        self.update(QRect(self._x_from_column(c), self._y_from_row(r),
              self.tw * self.xs, self.th * self.ys))
    
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


class LevelWidget(EditorWidget):

    tw = Sprites.tile_width
    th = Sprites.tile_height
        
    rows = Levels.width
    columns = Levels.height
    
    def __init__(self, levels, sprites, puzzle, parent = None):
    
        EditorWidget.__init__(self, parent)
        
        self.sprites = sprites
        self.levels = []
        
        self.setLevel(levels, puzzle, 1)
    
    def loadImages(self):
    
        self.tile_images = {}
        
        palette = map(lambda x: qRgb(*x), self.levels_obj.palette(self.level_number - 1))
        
        for number in self.sprites.sprite_table.keys():
        
            sprite = self.sprites.read_sprite(number)
            
            image = QImage(sprite, self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.tile_images[number] = image
        
        for number in range(21):
        
            sprite = self.puzzle.read_sprite(self.level_number - 1, number)
            
            image = QImage(sprite, self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.tile_images[number + 0x10] = image
    
    def loadLevels(self):
    
        self.levels = map(self.levels_obj.read, range(5))
    
    def setTileImages(self, tile_images):
    
        self.tile_images = tile_images
    
    def clearLevel(self):
    
        for row in range(self.rows):
            for column in range(self.columns):
                self.writeTile(column, row, self.currentTile)
    
    def setLevel(self, levels, puzzle, number):
    
        self.levels_obj = levels
        self.puzzle = puzzle
        
        self.level_number = number
        self.loadLevels()
        self.loadImages()
        
        self.update()
    
    def readTile(self, c, r):
    
        tile = self.levels[self.level_number - 1][r][c]
        if tile != 255:
            return self.tile_images[tile]
        else:
            return None
    
    def writeTile(self, c, r, tile):
    
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return
        
        self.levels[self.level_number - 1][r][c] = tile
        self.updateCell(c, r)


class PuzzleWidget(EditorWidget):

    xs = 2
    ys = 1
    
    tw = Sprites.tile_width
    th = Sprites.tile_height
    
    rows = Puzzle.rows
    columns = Puzzle.columns
    
    bw = Puzzle.block_width
    bh = Puzzle.block_height
    
    palette = [(0,0,0), (255,0,0), (0,255,0), (0,0,255)]
    
    def __init__(self, puzzle, parent = None):
    
        EditorWidget.__init__(self, parent)
        self.blocks = []
        
        self.setLevel(puzzle, 1)
        self.loadBlocks()
    
    def loadBlocks(self):
    
        self.block_images = {}
        
        palette = map(lambda x: qRgb(*x), self.palette)
        
        keys = Puzzle.blocks.keys()
        keys.sort()
        
        for key in keys:
        
            sprite = "".join(self.puzzle.read_block(Puzzle.blocks[key]))
            
            image = QImage(sprite, self.bw, self.bh, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.block_images[key] = image
    
    def loadImages(self):
    
        self.tile_images = {}
        
        palette = map(lambda x: qRgb(*x), self.palette)
        
        for number in range(21):
        
            sprite = self.puzzle.read_sprite(self.level_number - 1, number)
            
            image = QImage(sprite, self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.tile_images[number + 0x10] = image
    
    def setLevel(self, puzzle, number):
    
        self.puzzle = puzzle
        
        self.level_number = number
        self.loadImages()
        
        self.update()
    
    def readTile(self, c, r):
    
        tile = 0x10 + (r * 7) + c
        if tile != 255:
            return self.tile_images[tile]
        else:
            return None
    
    def writeTile(self, c, r, tile):
    
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return
        
        self.levels[self.level_number - 1][r][c] = tile
        self.updateCell(c, r)


class EditorWindow(QMainWindow):

    def __init__(self, uef_file):
    
        QMainWindow.__init__(self)
        
        self.openUEF(uef_file)
        
        self.xs = 2
        self.ys = 1
        
        self.path = ""
        self.set = ""
        
        self.levelWidget = LevelWidget(self.levels, self.sprites, self.puzzle)
        self.puzzleWidget = PuzzleWidget(self.puzzle)
        
        self.createToolBars()
        self.createMenus()
        
        # Select the first tile in the tiles toolbar and the first level in the
        # levels menu.
        self.tileGroup.actions()[0].trigger()
        self.levelsGroup.actions()[0].trigger()
        
        area = QScrollArea()
        area.setWidget(self.levelWidget)
        self.setCentralWidget(area)
    
    def openUEF(self, uef_file):
    
        self.uef_file = uef_file
        
        self.uef = UEFfile.UEFfile(uef_file)
        self.openSet(Levels.sets[0])
    
    def openSet(self, name):
    
        for details in self.uef.contents:
            if details["name"] == name:
                break
        
        self.set = name
        self.levels = Levels(details["data"])
        self.sprites = Sprites(details["data"][0xabd:])
        self.puzzle = Puzzle(details["data"])
    
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
        self.writeLevels(self.levelWidget.levels)
        
        # Write the new UEF file.
        u = UEFfile.UEFfile(creator = 'Clogger Editor ' + __version__)
        u.minor = 6
        u.target_machine = "Electron"
        
        files = map(lambda x: (x["name"], x["load"], x["exec"], x["data"]),
                    self.uef.contents)
        
        u.import_files(0, files, gap = True)
        
        try:
            u.write(path, write_emulator_info = False)
            return True
        except UEFfile.UEFfile_error:
            return False
    
    def saveLevelImageAs(self):
    
        path = QFileDialog.getSaveFileName(self, self.tr("Save Level Image As"),
            "%s-%i.png" % (self.set, self.levelWidget.level_number), self.tr("PNG files (*.png)"))
        if not path.isEmpty():
        
            if not self.levelWidget.saveImage(unicode(path)):
                QMessageBox.warning(self, self.tr("Save Level Image"),
                    self.tr("Couldn't save the image '%1'.\n").arg(path))
    
    def savePuzzleImageAs(self):
    
        path = QFileDialog.getSaveFileName(self, self.tr("Save Puzzle Image As"),
            "%s-%i.png" % (self.set, self.levelWidget.level_number), self.tr("PNG files (*.png)"))
        if not path.isEmpty():
        
            if not self.puzzleWidget.saveImage(unicode(path)):
                QMessageBox.warning(self, self.tr("Save Puzzle Image"),
                    self.tr("Couldn't save the image '%1'.\n").arg(path))
    
    def createToolBars(self):
    
        self.tileGroup = QActionGroup(self)
        
        collection = self.sprites.sprite_table.keys()
        collection.sort()
        puzzle_collection = range(0x10, 0x10 + 21)
        toolbar_areas = [Qt.TopToolBarArea, Qt.TopToolBarArea]
        titles = [self.tr("Tiles"), self.tr("Puzzle pieces")]
        
        collections = [collection, puzzle_collection]
        
        for symbols, area, title in zip(collections, toolbar_areas, titles):
        
            tilesToolBar = QToolBar(title)
            self.addToolBar(area, tilesToolBar)
            
            for symbol in symbols:
            
                image = self.levelWidget.tile_images[symbol]
                icon = QIcon(QPixmap.fromImage(image))
                action = tilesToolBar.addAction(icon, str(symbol))
                action.setData(QVariant(symbol))
                action.setCheckable(True)
                self.tileGroup.addAction(action)
                action.triggered.connect(self.setCurrentTile)
        
        puzzleBar = QToolBar(self.tr("Puzzle"))
        puzzleBar.addWidget(self.puzzleWidget)
        self.addToolBar(Qt.BottomToolBarArea, puzzleBar)
    
    def createMenus(self):
    
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        
        newAction = fileMenu.addAction(self.tr("&New"))
        newAction.setShortcut(QKeySequence.New)
        
        saveAsAction = fileMenu.addAction(self.tr("Save &As..."))
        saveAsAction.setShortcut(QKeySequence.SaveAs)
        saveAsAction.triggered.connect(self.saveAs)
        saveAsAction.setEnabled(False)
        
        self.saveLevelImageAsAction = fileMenu.addAction(self.tr("Save Level Image &As..."))
        self.saveLevelImageAsAction.triggered.connect(self.saveLevelImageAs)
        self.saveLevelImageAsAction.setEnabled(False)
        
        self.savePuzzleImageAsAction = fileMenu.addAction(self.tr("Save Puzzle Image &As..."))
        self.savePuzzleImageAsAction.triggered.connect(self.savePuzzleImageAs)
        self.savePuzzleImageAsAction.setEnabled(False)
        
        quitAction = fileMenu.addAction(self.tr("E&xit"))
        quitAction.setShortcut(self.tr("Ctrl+Q"))
        quitAction.triggered.connect(self.close)
        
        editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        clearAction = editMenu.addAction(self.tr("&Clear"))
        clearAction.triggered.connect(self.clearLevel)
        
        levelsMenu = self.menuBar().addMenu(self.tr("&Levels"))
        self.levelsGroup = QActionGroup(self)
        
        for name in self.levels.sets:
        
            setMenu = levelsMenu.addMenu(name)
            
            for i in range(5):
                levelAction = setMenu.addAction(str(i + 1))
                levelAction.setData(QVariant((name, i + 1)))
                levelAction.setCheckable(True)
                self.levelsGroup.addAction(levelAction)
        
        levelsMenu.triggered.connect(self.selectLevel)
    
    def setCurrentTile(self):
    
        self.levelWidget.currentTile = self.sender().data().toInt()[0]
    
    def selectLevel(self, action):
    
        name, number = action.data().toPyObject()
        self.levelWidget.highlight = None
        self.setLevel(name, number)
    
    def setLevel(self, name, number):
    
        self.openSet(name)
        
        self.levelWidget.setLevel(self.levels, self.puzzle, number)
        self.puzzleWidget.setLevel(self.puzzle, number)
        
        # Also change the sprites in the toolbar.
        for action in self.tileGroup.actions():
        
            symbol = action.data().toInt()[0]
            icon = QIcon(QPixmap.fromImage(self.levelWidget.tile_images[symbol]))
            action.setIcon(icon)
        
        self.saveLevelImageAsAction.setEnabled(True)
        self.savePuzzleImageAsAction.setEnabled(True)
    
    def clearLevel(self):
    
        answer = QMessageBox.question(self, self.tr("Clear Level"),
            self.tr("Clear the current level?"), QMessageBox.Yes | QMessageBox.No)
        
        if answer == QMessageBox.Yes:
            self.levelWidget.clearLevel()
    
    def writeLevels(self):
    
        pass
    
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
    
    window = EditorWindow(unicode(app.arguments()[1]))
    window.show()
    sys.exit(app.exec_())
