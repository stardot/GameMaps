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

__version__ = "0.9"

class EditorWidget(QWidget):

    xs = 2
    ys = 1
    
    updated = pyqtSignal()
    
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
        
        if self.highlight:
            c1, r1, c2, r2 = self.highlight
            x1, x2 = map(lambda x: x * self.tw * self.xs, (c1, c2))
            y1, y2 = map(lambda y: y * self.th * self.ys, (r1, r2))
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        
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
    
    def __init__(self, levels, sprites, puzzle, character, parent = None):
    
        EditorWidget.__init__(self, parent)
        
        self.levels = levels
        self.sprites = sprites
        self.character = character
        
        self.setLevel(levels, puzzle, 1)
    
    def loadImages(self):
    
        self.tile_images = {}
        
        palette = map(lambda x: qRgb(*x), self.levels.palette(self.level_number - 1))
        
        for number in self.sprites.sprite_table.keys():
        
            sprite = self.sprites.read_sprite(number)
            
            image = QImage(sprite, self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.tile_images[number] = image
        
        self.loadPuzzleImages(update = False)
        
        # Read the character sprite from a separate Sprites instance.
        sprite = self.character.read_sprite(0xff)
        lines = map(lambda i: sprite[i:i+16], range(0, 512, 16))
        lines.reverse()
        image = QImage("".join(lines), self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
        image.setColorTable(palette)
        self.tile_images[0xff] = image
    
    def loadPuzzleImages(self, update = True):
    
        palette = map(lambda x: qRgb(*x), self.levels.palette(self.level_number - 1))
        
        for number in range(21):
        
            sprite = self.puzzle.read_sprite(self.level_number - 1, number)
            
            image = QImage(sprite, self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.tile_images[number + 0x10] = image
        
        if update:
            self.update()
    
    def setTileImages(self, tile_images):
    
        self.tile_images = tile_images
    
    def clearLevel(self):
    
        for row in range(self.rows):
            for column in range(self.columns):
                self.writeTile(column, row, self.currentTile)
    
    def setLevel(self, levels, puzzle, number):
    
        self.levels = levels
        self.puzzle = puzzle
        
        self.level_number = number
        self.loadImages()
        
        self.readTargetArea(update = False)
        self.update()
    
    def readTargetArea(self, update = True):
    
        c1, r1 = self.levels.get_target_position(self.level_number - 1, 0)
        c2, r2 = self.levels.get_target_position(self.level_number - 1, 20)
        self.highlight = c1, r1, c2 + 1, r2 + 1
        
        if update:
            self.update()
    
    def readTile(self, c, r):
    
        tile = self.levels.read_tile(self.level_number - 1, c, r)
        return self.tile_images[tile]
    
    def writeTile(self, c, r, tile):
    
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return
        
        self.levels.write_tile(self.level_number - 1, c, r, tile)
        self.updateCell(c, r)


class PuzzleEditor(EditorWidget):

    xs = 2
    ys = 1
    
    tw = Puzzle.block_width
    th = Puzzle.block_height
    
    rows = Puzzle.rows * 4
    columns = Puzzle.columns * 4
    
    palette = [(0,0,0), (255,0,0), (0,255,0), (0,0,255)]
    
    def __init__(self, puzzle, parent = None):
    
        EditorWidget.__init__(self, parent)
        
        self.setLevel(puzzle, 1)
        self.changed = False
    
    def loadImages(self):
    
        self.tile_images = {}
        
        palette = map(lambda x: qRgb(*x), self.palette)
        
        keys = Puzzle.blocks.keys()
        keys.sort()
        
        for key in keys:
        
            sprite = "".join(self.puzzle.read_block(Puzzle.blocks[key]))
            
            image = QImage(sprite, self.tw, self.th, QImage.Format_Indexed8).scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(palette)
            self.tile_images[key] = image
    
    def setLevel(self, puzzle, number):
    
        self.puzzle = puzzle
        
        self.level_number = number
        self.loadImages()
        
        self.update()
    
    def setCurrentTile(self, value):
    
        self.currentTile = value
    
    def readTile(self, c, r):
    
        piece = ((r/4) * 7) + (c/4)
        tile = self.puzzle.read_block_number(self.level_number - 1, piece, c % 4, r % 4)
        return self.tile_images[tile]
    
    def writeTile(self, c, r, tile):
    
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return
        
        piece = ((r/4) * 7) + (c/4)
        oldTile = self.puzzle.read_block_number(self.level_number - 1, piece, c % 4, r % 4)
        
        self.puzzle.write_block_number(self.level_number - 1, piece, c % 4, r % 4, tile)
        self.updateCell(c, r)
        
        if tile != oldTile:
            self.changed = True
    
    def mouseReleaseEvent(self, event):
    
        if self.changed:
            self.updated.emit()
            self.changed = False


class PuzzlePalette(PuzzleEditor):

    rows = 12
    columns = 1
    
    currentChanged = pyqtSignal(int)
    
    def __init__(self, puzzle, parent = None):
    
        PuzzleEditor.__init__(self, puzzle, parent)
        
        self.blocks = Puzzle.blocks.keys()
        self.blocks.sort()
    
    def readTile(self, c, r):
    
        tile = self.blocks[r]
        return self.tile_images[tile]
    
    def writeTile(self, c, r, tile):
    
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return
        
        tile = self.blocks[r]
        self.currentChanged.emit(tile)


class PuzzleWidget(QWidget):

    updated = pyqtSignal()
    
    def __init__(self, puzzle, parent = None):
    
        QWidget.__init__(self, parent)
        
        self.puzzleEditor = PuzzleEditor(puzzle)
        self.puzzlePalette = PuzzlePalette(puzzle)
        
        self.puzzleEditor.updated.connect(self.updated)
        self.puzzlePalette.currentChanged.connect(self.puzzleEditor.setCurrentTile)
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.puzzleEditor)
        layout.addWidget(self.puzzlePalette)
    
    def saveImage(self, path):
    
        return self.puzzleEditor.saveImage(path)
    
    def setLevel(self, puzzle, number):
    
        self.puzzleEditor.setLevel(puzzle, number)


class AreaWidget(QWidget):

    valueChanged = pyqtSignal()
    
    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setMaxLength(7)
        self.passwordEdit.setValidator(QRegExpValidator(QRegExp("[A-Z]+"), self))
        self.passwordEdit.textChanged.connect(self.updatePassword)
        
        self.columnEdit = QSpinBox()
        self.columnEdit.setMinimum(0)
        self.columnEdit.setMaximum(25)
        
        self.rowEdit = QSpinBox()
        self.rowEdit.setMinimum(0)
        self.rowEdit.setMaximum(25)
        
        self.columnEdit.valueChanged.connect(self.updateArea)
        self.rowEdit.valueChanged.connect(self.updateArea)
        
        layout = QFormLayout(self)
        layout.addRow(self.tr("&Password:"), self.passwordEdit)
        layout.addRow(self.tr("&Column:"), self.columnEdit)
        layout.addRow(self.tr("&Row:"), self.rowEdit)
    
    def setLevel(self, levels, number):
    
        self.levels = levels
        self.level_number = number
        
        self.passwordEdit.setText(levels.get_password(number - 1))
        self.passwordEdit.setEnabled(number != 1)
        
        c1, r1 = levels.get_target_position(number - 1, 0)
        self.columnEdit.setValue(c1)
        self.rowEdit.setValue(r1)
    
    def updatePassword(self, text):
    
        self.levels.set_password(self.level_number - 1, str(text))
    
    def updateArea(self):
    
        c1, r1 = self.columnEdit.value(), self.rowEdit.value()
        
        for i in range(21):
            x = c1 + (i % 7)
            y = r1 + (i / 7)
            self.levels.set_target_position(self.level_number - 1, i, x, y)
        
        self.valueChanged.emit()


class EditorWindow(QMainWindow):

    def __init__(self, uef_file):
    
        QMainWindow.__init__(self)
        
        self.xs = 2
        self.ys = 1
        
        self.set = ""
        self.sets = {}
        
        self.openUEF(uef_file)
        
        self.levelWidget = LevelWidget(self.levels, self.sprites, self.puzzle,
                                       self.character)
        self.puzzleWidget = PuzzleWidget(self.puzzle)
        
        # Ensure that changes to the puzzle are reflected in the images used
        # for the puzzle pieces.
        self.puzzleWidget.updated.connect(self.updatePuzzleImages)
        
        self.createToolBars()
        self.createMenus()
        
        # Select the first tile in the tiles toolbar and the first level in the
        # levels menu.
        self.tileGroup.actions()[0].trigger()
        self.levelsGroup.actions()[0].trigger()
        
        area = QScrollArea()
        area.setWidget(self.levelWidget)
        self.setCentralWidget(area)
    
    def openFile(self):
    
        path = QFileDialog.getOpenFileName(self, self.tr("Open File"),
                                           self.uef_file, self.tr("UEF files (*.uef)"))
        if not path.isEmpty():
            self.openUEF(unicode(path))
            self.setLevel(self.set, 1)
    
    def openUEF(self, uef_file):
    
        self.uef_file = uef_file
        
        self.uef = UEFfile.UEFfile(uef_file)
        
        for details in self.uef.contents:
            name = details["name"]
            if name in Levels.sets:
                self.sets[name] = list(details["data"])
            elif name == "SPTDATA":
                self.character = Sprites(details["data"])
        
        self.openSet(Levels.sets[0])
        self.setWindowTitle(self.tr(uef_file))
    
    def openSet(self, name):
    
        data = self.sets[name]
        
        self.set = name
        self.levels = Levels(data)
        self.sprites = Sprites(data[0xabd:])
        self.puzzle = Puzzle(data)
    
    def saveAs(self):
    
        path = QFileDialog.getSaveFileName(self, self.tr("Save As"),
                                           self.uef_file, self.tr("UEF files (*.uef)"))
        if not path.isEmpty():
        
            if self.saveLevels(unicode(path)):
                self.uef_file = path
                self.setWindowTitle(self.tr(path))
            else:
                QMessageBox.warning(self, self.tr("Save Levels"),
                    self.tr("Couldn't write the new executable to %1.\n").arg(path))
    
    def saveLevels(self, path):
    
        # Write the levels back to the UEF file.
        self.writeLevels()
        
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
        
        tilesToolBar = QToolBar(self.tr("Tiles"))
        collection = self.sprites.sprite_table.keys()
        collection.sort()
        self.addToolBar(Qt.TopToolBarArea, tilesToolBar)
        
        for symbol in collection:
        
            image = self.levelWidget.tile_images[symbol]
            icon = QIcon(QPixmap.fromImage(image))
            action = tilesToolBar.addAction(icon, str(symbol))
            action.setData(QVariant(symbol))
            action.setCheckable(True)
            self.tileGroup.addAction(action)
            action.triggered.connect(self.setCurrentTile)
        
        piecesToolBar = QToolBar(self.tr("Puzzle pieces"))
        puzzle_collection = range(0x10, 0x10 + 21)
        self.addToolBar(Qt.TopToolBarArea, piecesToolBar)
        
        for symbol in puzzle_collection:
        
            image = self.levelWidget.tile_images[symbol]
            icon = QIcon(QPixmap.fromImage(image))
            action = piecesToolBar.addAction(icon, str(symbol))
            action.setData(QVariant(symbol))
            action.setCheckable(True)
            self.tileGroup.addAction(action)
            action.triggered.connect(self.setCurrentTile)
        
        puzzleBar = QToolBar(self.tr("Puzzle"))
        puzzleBar.addWidget(self.puzzleWidget)
        self.addToolBar(Qt.BottomToolBarArea, puzzleBar)
        
        # Add a level toolbar with password and target area widgets.
        levelToolBar = QToolBar(self.tr("Levels"))
        self.addToolBar(Qt.BottomToolBarArea, levelToolBar)
        
        self.areaWidget = AreaWidget()
        self.areaWidget.valueChanged.connect(self.levelWidget.readTargetArea)
        levelToolBar.addWidget(self.areaWidget)
    
    def updatePuzzleImages(self):
    
        self.levelWidget.loadPuzzleImages()
        
        puzzle_collection = range(0x10, 0x10 + 21)
        
        for action in self.tileGroup.actions():
        
            symbol, valid = action.data().toInt()
            
            if valid and 0x10 <= symbol < 0x10 + 21:
                image = self.levelWidget.tile_images[symbol]
                icon = QIcon(QPixmap.fromImage(image))
                action.setIcon(icon)
    
    def createMenus(self):
    
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        
        #newAction = fileMenu.addAction(self.tr("&New"))
        #newAction.setShortcut(QKeySequence.New)
        
        openAction = fileMenu.addAction(self.tr("&Open..."))
        openAction.setShortcut(QKeySequence.Open)
        openAction.triggered.connect(self.openFile)
        
        saveAsAction = fileMenu.addAction(self.tr("Save &As..."))
        saveAsAction.setShortcut(QKeySequence.SaveAs)
        saveAsAction.triggered.connect(self.saveAs)
        
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
        
        helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        
        aboutAction = helpMenu.addAction(self.tr("&About..."))
        
        image = self.levelWidget.tile_images[0xff]
        icon = QIcon(QPixmap.fromImage(image))
        self.setWindowIcon(icon)
        
        self.aboutBox = QMessageBox(QMessageBox.NoIcon, self.tr("About This Application"),
            self.tr("<qt>A level/puzzle editor for the Acorn Electron version "
                    "of Impact Software's Clogger.<p><b>Version:</b> %1</qt>").arg(__version__),
            QMessageBox.Close, self)
        
        self.aboutBox.setDetailedText(__doc__.strip())
        self.aboutBox.setWindowIcon(icon)
        aboutAction.triggered.connect(self.aboutBox.exec_)
        
        aboutQtAction = helpMenu.addAction(self.tr("&About Qt..."))
        aboutQtAction.triggered.connect(qApp.aboutQt)
    
    def setCurrentTile(self):
    
        self.levelWidget.currentTile = self.sender().data().toInt()[0]
    
    def selectLevel(self, action):
    
        name, number = action.data().toPyObject()
        self.setLevel(name, number)
    
    def setLevel(self, name, number):
    
        self.openSet(name)
        
        self.levelWidget.setLevel(self.levels, self.puzzle, number)
        self.puzzleWidget.setLevel(self.puzzle, number)
        self.areaWidget.setLevel(self.levels, number)
        
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
    
        for details in self.uef.contents:
            name = details["name"]
            if name in Levels.sets:
                details["data"] = "".join(self.sets[name])
    
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
