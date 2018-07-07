#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BNTX Editor
# Version 0.1
# Copyright © 2018 AboodXD

# This file is part of BNTX Editor.

# BNTX Editor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# BNTX Editor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Python version: sanity check
minimum = 3.4
import sys

currentRunningVersion = sys.version_info.major + (.1 * sys.version_info.minor)
if currentRunningVersion < minimum:
    errormsg = 'Please update your copy of Python to ' + str(minimum) + \
               ' or greater. Currently running on: ' + sys.version[:5]

    raise Exception(errormsg)

import os.path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtWidgets
import time
import traceback

import bntx as BNTX
import globals


def _excepthook(*exc_info):
    """
    Custom unhandled exceptions handler
    """
    separator = '-' * 80
    logFile = "log.txt"
    notice = \
        """An unhandled exception occurred. This program will now exit. """\
        """Please report the problem to @MasterVermilli0n#7241 on Discord.\n"""\
        """A log will be written to "%s".\n\nError information:\n""" % logFile

    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    e = "".join(traceback.format_exception(*exc_info))
    sections = [separator, timeString, separator, e]
    msg = '\n'.join(sections)

    try:
        with open(logFile, "w") as f:
            f.write(msg)

    except IOError:
        pass

    errorbox = QtWidgets.QMessageBox()
    errorbox.setText(notice + msg)
    errorbox.exec_()

    sys.exit(1)


# Override the exception handler with ours
sys.excepthook = _excepthook


class MainWindow(QtWidgets.QWidget):
    class Separator(QtWidgets.QFrame):
        def __init__(self):
            super().__init__()

            self.setFrameShape(QtWidgets.QFrame.HLine)
            self.setFrameShadow(QtWidgets.QFrame.Sunken)

    def __init__(self):
        super().__init__()

        self.setupUi()
        self.loaded = False
        self.bntx = BNTX.File()

    def setupUi(self):
        self.setWindowTitle("BNTX Editor v%s - By AboodXD" % globals.Version)
        self.setMinimumSize(375, 0)

        Layout = QtWidgets.QGridLayout()

        self.openbtn = QtWidgets.QPushButton("Open")
        self.openbtn.clicked.connect(self.openFile)

        self.openLnEdt = QtWidgets.QLineEdit()
        self.openLnEdt.setEnabled(False)

        self.fnameLabel = QtWidgets.QLabel()
        self.fnameLabel.setText("File name:")

        self.fnameLnEdt = QtWidgets.QLineEdit()
        self.fnameLnEdt.setEnabled(False)

        self.targetLabel = QtWidgets.QLabel()
        self.targetLabel.setText("Target:")

        self.targetLnEdt = QtWidgets.QLineEdit()
        self.targetLnEdt.setEnabled(False)

        self.tileModeLabel = QtWidgets.QLabel()
        self.tileModeLabel.setText("Tiling mode:")

        self.tileModeLnEdt = QtWidgets.QLineEdit()
        self.tileModeLnEdt.setEnabled(False)

        self.dimLabel = QtWidgets.QLabel()
        self.dimLabel.setText("Image Storage Dimension:")

        self.dimLnEdt = QtWidgets.QLineEdit()
        self.dimLnEdt.setEnabled(False)

        self.sparseBindingLabel = QtWidgets.QLabel()
        self.sparseBindingLabel.setText("Sparse Binding:")

        self.sparseBindingLnEdt = QtWidgets.QLineEdit()
        self.sparseBindingLnEdt.setEnabled(False)

        self.sparseResidencyLabel = QtWidgets.QLabel()
        self.sparseResidencyLabel.setText("Sparse Residency:")

        self.sparseResidencyLnEdt = QtWidgets.QLineEdit()
        self.sparseResidencyLnEdt.setEnabled(False)

        self.swizzleLabel = QtWidgets.QLabel()
        self.swizzleLabel.setText("Swizzle:")

        self.swizzleSpinBox = QtWidgets.QSpinBox()
        self.swizzleSpinBox.setRange(0, 7)
        self.swizzleSpinBox.setEnabled(False)
        self.swizzleSpinBox.valueChanged.connect(self.swizzleChanged)

        self.numMipsLabel = QtWidgets.QLabel()
        self.numMipsLabel.setText("Number of Mipmaps:")

        self.numMipsLnEdt = QtWidgets.QLineEdit()
        self.numMipsLnEdt.setEnabled(False)

        self.numSamplesLabel = QtWidgets.QLabel()
        self.numSamplesLabel.setText("Number of Multi Samples:")

        self.numSamplesLnEdt = QtWidgets.QLineEdit()
        self.numSamplesLnEdt.setEnabled(False)

        self.formatLabel = QtWidgets.QLabel()
        self.formatLabel.setText("Format:")

        self.formatLnEdt = QtWidgets.QLineEdit()
        self.formatLnEdt.setEnabled(False)

        self.accessFlagsLabel = QtWidgets.QLabel()
        self.accessFlagsLabel.setText("GPU Access Flag:")

        self.accessFlagsComboBox = QtWidgets.QComboBox()
        self.accessFlagsComboBox.setEnabled(False)
        self.accessFlagsComboBox.currentIndexChanged.connect(self.accessFlagsChanged)

        self.widthLabel = QtWidgets.QLabel()
        self.widthLabel.setText("Width:")

        self.widthLnEdt = QtWidgets.QLineEdit()
        self.widthLnEdt.setEnabled(False)

        self.heightLabel = QtWidgets.QLabel()
        self.heightLabel.setText("Height:")

        self.heightLnEdt = QtWidgets.QLineEdit()
        self.heightLnEdt.setEnabled(False)

        self.arrayLengthLabel = QtWidgets.QLabel()
        self.arrayLengthLabel.setText("Array Length:")

        self.arrayLengthLnEdt = QtWidgets.QLineEdit()
        self.arrayLengthLnEdt.setEnabled(False)

        self.blockHeightLabel = QtWidgets.QLabel()
        self.blockHeightLabel.setText("Block Height:")

        self.blockHeightLnEdt = QtWidgets.QLineEdit()
        self.blockHeightLnEdt.setEnabled(False)

        self.imgSizeLabel = QtWidgets.QLabel()
        self.imgSizeLabel.setText("Image Size:")

        self.imgSizeLnEdt = QtWidgets.QLineEdit()
        self.imgSizeLnEdt.setEnabled(False)

        self.alignmentLabel = QtWidgets.QLabel()
        self.alignmentLabel.setText("Alignment:")

        self.alignmentLnEdt = QtWidgets.QLineEdit()
        self.alignmentLnEdt.setEnabled(False)

        self.chan1Label = QtWidgets.QLabel()
        self.chan1Label.setText("Channel 1:")

        self.chan1ComboBox = QtWidgets.QComboBox()
        self.chan1ComboBox.setEnabled(False)
        self.chan1ComboBox.currentIndexChanged.connect(self.chan1Changed)

        self.chan2Label = QtWidgets.QLabel()
        self.chan2Label.setText("Channel 2:")

        self.chan2ComboBox = QtWidgets.QComboBox()
        self.chan2ComboBox.setEnabled(False)
        self.chan2ComboBox.currentIndexChanged.connect(self.chan2Changed)

        self.chan3Label = QtWidgets.QLabel()
        self.chan3Label.setText("Channel 3:")

        self.chan3ComboBox = QtWidgets.QComboBox()
        self.chan3ComboBox.setEnabled(False)
        self.chan3ComboBox.currentIndexChanged.connect(self.chan3Changed)

        self.chan4Label = QtWidgets.QLabel()
        self.chan4Label.setText("Channel 4:")

        self.chan4ComboBox = QtWidgets.QComboBox()
        self.chan4ComboBox.setEnabled(False)
        self.chan4ComboBox.currentIndexChanged.connect(self.chan4Changed)

        self.imgDimLabel = QtWidgets.QLabel()
        self.imgDimLabel.setText("Image Dimension:")

        self.imgDimComboBox = QtWidgets.QComboBox()
        self.imgDimComboBox.setEnabled(False)
        self.imgDimComboBox.currentIndexChanged.connect(self.imgDimChanged)
        
        openLayout = QtWidgets.QHBoxLayout()
        openLayout.addWidget(self.openbtn)
        openLayout.addWidget(self.openLnEdt)
        
        fnameLayout = QtWidgets.QHBoxLayout()
        fnameLayout.addWidget(self.fnameLabel)
        fnameLayout.addWidget(self.fnameLnEdt)
        
        targetLayout = QtWidgets.QHBoxLayout()
        targetLayout.addWidget(self.targetLabel)
        targetLayout.addWidget(self.targetLnEdt)
        
        tileModeLayout = QtWidgets.QHBoxLayout()
        tileModeLayout.addWidget(self.tileModeLabel)
        tileModeLayout.addWidget(self.tileModeLnEdt)
        
        dimLayout = QtWidgets.QHBoxLayout()
        dimLayout.addWidget(self.dimLabel)
        dimLayout.addWidget(self.dimLnEdt)
        
        sparseBindingLayout = QtWidgets.QHBoxLayout()
        sparseBindingLayout.addWidget(self.sparseBindingLabel)
        sparseBindingLayout.addWidget(self.sparseBindingLnEdt)
        
        sparseResidencyLayout = QtWidgets.QHBoxLayout()
        sparseResidencyLayout.addWidget(self.sparseResidencyLabel)
        sparseResidencyLayout.addWidget(self.sparseResidencyLnEdt)
        
        swizzleLayout = QtWidgets.QHBoxLayout()
        swizzleLayout.addWidget(self.swizzleLabel)
        swizzleLayout.addWidget(self.swizzleSpinBox)
        
        numMipsLayout = QtWidgets.QHBoxLayout()
        numMipsLayout.addWidget(self.numMipsLabel)
        numMipsLayout.addWidget(self.numMipsLnEdt)
        
        numSamplesLayout = QtWidgets.QHBoxLayout()
        numSamplesLayout.addWidget(self.numSamplesLabel)
        numSamplesLayout.addWidget(self.numSamplesLnEdt)
        
        formatLayout = QtWidgets.QHBoxLayout()
        formatLayout.addWidget(self.formatLabel)
        formatLayout.addWidget(self.formatLnEdt)
        
        accessFlagsLayout = QtWidgets.QHBoxLayout()
        accessFlagsLayout.addWidget(self.accessFlagsLabel)
        accessFlagsLayout.addWidget(self.accessFlagsComboBox)
        
        widthLayout = QtWidgets.QHBoxLayout()
        widthLayout.addWidget(self.widthLabel)
        widthLayout.addWidget(self.widthLnEdt)
        
        heightLayout = QtWidgets.QHBoxLayout()
        heightLayout.addWidget(self.heightLabel)
        heightLayout.addWidget(self.heightLnEdt)
        
        arrayLengthLayout = QtWidgets.QHBoxLayout()
        arrayLengthLayout.addWidget(self.arrayLengthLabel)
        arrayLengthLayout.addWidget(self.arrayLengthLnEdt)
        
        blockHeightLayout = QtWidgets.QHBoxLayout()
        blockHeightLayout.addWidget(self.blockHeightLabel)
        blockHeightLayout.addWidget(self.blockHeightLnEdt)
        
        imgSizeLayout = QtWidgets.QHBoxLayout()
        imgSizeLayout.addWidget(self.imgSizeLabel)
        imgSizeLayout.addWidget(self.imgSizeLnEdt)
        
        alignmentLayout = QtWidgets.QHBoxLayout()
        alignmentLayout.addWidget(self.alignmentLabel)
        alignmentLayout.addWidget(self.alignmentLnEdt)
        
        chan1Layout = QtWidgets.QHBoxLayout()
        chan1Layout.addWidget(self.chan1Label)
        chan1Layout.addWidget(self.chan1ComboBox)
        
        chan2Layout = QtWidgets.QHBoxLayout()
        chan2Layout.addWidget(self.chan2Label)
        chan2Layout.addWidget(self.chan2ComboBox)
        
        chan3Layout = QtWidgets.QHBoxLayout()
        chan3Layout.addWidget(self.chan3Label)
        chan3Layout.addWidget(self.chan3ComboBox)
        
        chan4Layout = QtWidgets.QHBoxLayout()
        chan4Layout.addWidget(self.chan4Label)
        chan4Layout.addWidget(self.chan4ComboBox)
        
        imgDimLayout = QtWidgets.QHBoxLayout()
        imgDimLayout.addWidget(self.imgDimLabel)
        imgDimLayout.addWidget(self.imgDimComboBox)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.updateTexInfo)

        self.exportButton = QtWidgets.QPushButton()
        self.exportButton.setEnabled(False)
        self.exportButton.setText("Export")
        self.exportButton.clicked.connect(self.exportTex)

        self.exportAsButton = QtWidgets.QPushButton()
        self.exportAsButton.setEnabled(False)
        self.exportAsButton.setText("Export As")
        self.exportAsButton.clicked.connect(self.exportTexAs)

        self.exportAllButton = QtWidgets.QPushButton()
        self.exportAllButton.setEnabled(False)
        self.exportAllButton.setText("Export All")
        self.exportAllButton.clicked.connect(self.exportTexAll)
        
        exportLayout = QtWidgets.QHBoxLayout()
        exportLayout.addWidget(self.exportButton)
        exportLayout.addWidget(self.exportAsButton)
        exportLayout.addWidget(self.exportAllButton)

        self.replaceButton = QtWidgets.QPushButton()
        self.replaceButton.setEnabled(False)
        self.replaceButton.setText("Replace")
        self.replaceButton.clicked.connect(self.replaceTex)

        self.saveButton = QtWidgets.QPushButton()
        self.saveButton.setEnabled(False)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)

        self.saveAsButton = QtWidgets.QPushButton()
        self.saveAsButton.setEnabled(False)
        self.saveAsButton.setText("Save As")
        self.saveAsButton.clicked.connect(self.saveAs)

        saveLayout = QtWidgets.QHBoxLayout()
        saveLayout.addWidget(self.saveButton)
        saveLayout.addWidget(self.saveAsButton)

        fileLayout = QtWidgets.QVBoxLayout()
        fileLayout.addLayout(openLayout)
        fileLayout.addWidget(self.Separator())
        fileLayout.addLayout(saveLayout)
        fileLayout.addWidget(self.Separator())
        fileLayout.addLayout(fnameLayout)
        fileLayout.addLayout(targetLayout)
        fileLayout.addWidget(self.Separator())
        fileLayout.addLayout(tileModeLayout)
        fileLayout.addLayout(dimLayout)
        fileLayout.addLayout(sparseBindingLayout)
        fileLayout.addLayout(sparseResidencyLayout)
        fileLayout.addLayout(swizzleLayout)
        fileLayout.addLayout(numMipsLayout)
        fileLayout.addLayout(numSamplesLayout)
        fileLayout.addLayout(formatLayout)
        fileLayout.addLayout(accessFlagsLayout)
        fileLayout.addLayout(widthLayout)
        fileLayout.addLayout(heightLayout)
        fileLayout.addLayout(arrayLengthLayout)
        fileLayout.addLayout(blockHeightLayout)
        fileLayout.addLayout(imgSizeLayout)
        fileLayout.addLayout(alignmentLayout)
        fileLayout.addLayout(chan1Layout)
        fileLayout.addLayout(chan2Layout)
        fileLayout.addLayout(chan2Layout)
        fileLayout.addLayout(chan3Layout)
        fileLayout.addLayout(chan4Layout)
        fileLayout.addLayout(imgDimLayout)
        fileLayout.addWidget(self.Separator())
        fileLayout.addWidget(self.comboBox)
        fileLayout.addWidget(self.Separator())
        fileLayout.addLayout(exportLayout)
        fileLayout.addWidget(self.replaceButton)

        self.createPreviewer()

        Layout = QtWidgets.QGridLayout()
        Layout.addWidget(self.Viewer, 0, 1)
        Layout.addLayout(fileLayout, 0, 0)
        self.setLayout(Layout)

        self.setLayout(Layout)

    def createPreviewer(self):
        self.Viewer = QtWidgets.QGroupBox("Preview")

        self.preview = QtWidgets.QLabel()
        self.resetPreviewer()

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.preview, 0, 0)
        self.Viewer.setLayout(mainLayout)

    def resetPreviewer(self):
        pix = QPixmap(333, 333)
        pix.fill(Qt.transparent)
        self.preview.setPixmap(pix)

    def prepareOpenFile(self, file):
        self.BFRESPath = os.path.dirname(os.path.abspath(file))

        self.openLnEdt.setText(file)
        self.fnameLnEdt.setText('')
        self.targetLnEdt.setText('')
        self.tileModeLnEdt.setText('')
        self.dimLnEdt.setText('')
        self.sparseBindingLnEdt.setText('')
        self.sparseResidencyLnEdt.setText('')
        self.numMipsLnEdt.setText('')
        self.numSamplesLnEdt.setText('')
        self.formatLnEdt.setText('')
        self.widthLnEdt.setText('')
        self.heightLnEdt.setText('')
        self.arrayLengthLnEdt.setText('')
        self.blockHeightLnEdt.setText('')
        self.imgSizeLnEdt.setText('')
        self.alignmentLnEdt.setText('')

        self.accessFlagsComboBox.setEnabled(False)
        self.swizzleSpinBox.setEnabled(False)
        self.chan1ComboBox.setEnabled(False)
        self.chan2ComboBox.setEnabled(False)
        self.chan3ComboBox.setEnabled(False)
        self.chan4ComboBox.setEnabled(False)
        self.imgDimComboBox.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.exportButton.setEnabled(False)
        self.exportAsButton.setEnabled(False)
        self.exportAllButton.setEnabled(False)
        self.replaceButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.saveAsButton.setEnabled(False)

        self.accessFlagsComboBox.clear()
        self.swizzleSpinBox.setValue(0)
        self.chan1ComboBox.clear()
        self.chan2ComboBox.clear()
        self.chan3ComboBox.clear()
        self.chan4ComboBox.clear()
        self.imgDimComboBox.clear()
        self.comboBox.clear()

    def openFile(self):
        self.loaded = False

        file = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", "Binary Resources Texture (*.bntx)")[0]
        if not file:
            return False

        self.prepareOpenFile(file)
        if not self.bntx.readFromFile(file):
            self.fnameLnEdt.setText(self.bntx.name)
            self.targetLnEdt.setText(self.bntx.target)
            self.accessFlagsComboBox.addItems([flag for flag in globals.accessFlags])
            self.chan1ComboBox.addItems([compSel for compSel in globals.compSels])
            self.chan2ComboBox.addItems([compSel for compSel in globals.compSels])
            self.chan3ComboBox.addItems([compSel for compSel in globals.compSels])
            self.chan4ComboBox.addItems([compSel for compSel in globals.compSels])
            self.imgDimComboBox.addItems([dim for dim in globals.imgDims])
            self.comboBox.addItems([texture.name for texture in self.bntx.textures])

            self.accessFlagsComboBox.setEnabled(True)
            self.swizzleSpinBox.setEnabled(True)
            self.chan1ComboBox.setEnabled(True)
            self.chan2ComboBox.setEnabled(True)
            self.chan3ComboBox.setEnabled(True)
            self.chan4ComboBox.setEnabled(True)
            self.imgDimComboBox.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.exportButton.setEnabled(True)
            self.exportAsButton.setEnabled(True)
            self.exportAllButton.setEnabled(True)
            self.replaceButton.setEnabled(True)
            self.saveButton.setEnabled(True)
            self.saveAsButton.setEnabled(True)

            self.comboBox.setCurrentIndex(0)
            self.loaded = True

    def updateTexInfo(self, index):
        texture = self.bntx.textures[index]

        if texture.tileMode in globals.tileModes:
            self.tileModeLnEdt.setText(globals.tileModes[texture.tileMode])

        else:
            self.tileModeLnEdt.setText(str(texture.tileMode))

        self.dimLnEdt.setText(globals.dims[texture.dim])
        self.sparseBindingLnEdt.setText(str(bool(texture.sparseBinding)))
        self.sparseResidencyLnEdt.setText(str(bool(texture.sparseResidency)))
        self.swizzleSpinBox.setValue(texture.swizzle)
        self.numMipsLnEdt.setText(str(texture.numMips - 1))
        self.numSamplesLnEdt.setText(str(texture.numSamples))

        if texture.format_ in globals.formats:
            self.formatLnEdt.setText(globals.formats[texture.format_])

        else:
            self.formatLnEdt.setText(hex(texture.format_))

        self.accessFlagsComboBox.setCurrentIndex(len(bin(texture.accessFlags)[2:]) - 1)
        self.widthLnEdt.setText(str(texture.width))
        self.heightLnEdt.setText(str(texture.height))
        self.arrayLengthLnEdt.setText(str(texture.arrayLength))
        self.blockHeightLnEdt.setText(str(1 << texture.blockHeightLog2))
        self.imgSizeLnEdt.setText(str(texture.imageSize))
        self.alignmentLnEdt.setText(str(texture.alignment))
        self.chan1ComboBox.setCurrentIndex(texture.compSel[0])
        self.chan2ComboBox.setCurrentIndex(texture.compSel[1])
        self.chan3ComboBox.setCurrentIndex(texture.compSel[2])
        self.chan4ComboBox.setCurrentIndex(texture.compSel[3])
        self.imgDimComboBox.setCurrentIndex(texture.imgDim)

        self.updatePreview(texture)

    def accessFlagsChanged(self, index):
        if self.loaded:
            texture = self.bntx.textures[self.comboBox.currentIndex()]

            if index in [0, 1]:
                texture.accessFlags = index

            else:
                texture.accessFlags = 1 << index

    def swizzleChanged(self, value):
        if self.loaded:
            texture = self.bntx.textures[self.comboBox.currentIndex()]
            texture.swizzle = value

    def chan1Changed(self, index):
        if self.loaded:
            texture = self.bntx.textures[self.comboBox.currentIndex()]
            texture.compSel[0] = index

            self.updatePreview(texture)

    def chan2Changed(self, index):
        if self.loaded:
            texture = self.bntx.textures[self.comboBox.currentIndex()]
            texture.compSel[1] = index

            self.updatePreview(texture)

    def chan3Changed(self, index):
        if self.loaded:
            texture = self.bntx.textures[self.comboBox.currentIndex()]
            texture.compSel[2] = index

            self.updatePreview(texture)

    def chan4Changed(self, index):
        if self.loaded:
            texture = self.bntx.textures[self.comboBox.currentIndex()]
            texture.compSel[3] = index

            self.updatePreview(texture)

    def imgDimChanged(self, index):
        if self.loaded:
            texture = self.bntx.textures[self.comboBox.currentIndex()]
            texture.imgDim = index

    def updatePreview(self, texture):
        if texture.format_ in [0x101, 0x201, 0x301, 0x401, 0x501, 0x601, 0x701,
                               0x801, 0x901, 0xb01, 0xb06, 0xc01, 0xc06, 0xe01,
                               0x1a01, 0x1a06, 0x1b01, 0x1b06, 0x1c01, 0x1c06,
                               0x1d01, 0x1d02, 0x1e01, 0x1e02, 0x3b01] and texture.dim == 2:

            result, _, _ = self.bntx.rawData(texture)

            if texture.format_ == 0x101:
                data = result[0]

                format_ = 'la4'
                bpp = 1

            elif texture.format_ == 0x201:
                data = result[0]

                format_ = 'l8'
                bpp = 1

            elif texture.format_ == 0x301:
                data = result[0]

                format_ = 'rgba4'
                bpp = 2

            elif texture.format_ == 0x401:
                data = result[0]

                format_ = 'abgr4'
                bpp = 2

            elif texture.format_ == 0x501:
                data = result[0]

                format_ = 'rgb5a1'
                bpp = 2

            elif texture.format_ == 0x601:
                data = result[0]

                format_ = 'a1bgr5'
                bpp = 2

            elif texture.format_ == 0x701:
                data = result[0]

                format_ = 'rgb565'
                bpp = 2

            elif texture.format_ == 0x801:
                data = result[0]

                format_ = 'bgr565'
                bpp = 2

            elif texture.format_ == 0x901:
                data = result[0]

                format_ = 'la8'
                bpp = 2

            elif (texture.format_ >> 8) == 0xb:
                data = result[0]

                format_ = 'rgba8'
                bpp = 4

            elif (texture.format_ >> 8) == 0xc:
                data = result[0]

                format_ = 'bgra8'
                bpp = 4

            elif texture.format_ == 0xe01:
                data = result[0]

                format_ = 'bgr10a2'
                bpp = 4

            elif (texture.format_ >> 8) == 0x1a:
                data = BNTX.bcn.decompressDXT1(result[0], texture.width, texture.height)

                format_ = 'rgba8'
                bpp = 4

            elif (texture.format_ >> 8) == 0x1b:
                data = BNTX.bcn.decompressDXT3(result[0], texture.width, texture.height)

                format_ = 'rgba8'
                bpp = 4

            elif (texture.format_ >> 8) == 0x1c:
                data = BNTX.bcn.decompressDXT5(result[0], texture.width, texture.height)

                format_ = 'rgba8'
                bpp = 4

            elif (texture.format_ >> 8) == 0x1d:
                data = BNTX.bcn.decompressBC4(result[0], texture.width, texture.height, 0 if texture.format_ & 3 == 1 else 1)

                format_ = 'rgba8'
                bpp = 4

            elif (texture.format_ >> 8) == 0x1e:
                data = BNTX.bcn.decompressBC5(result[0], texture.width, texture.height, 0 if texture.format_ & 3 == 1 else 1)

                format_ = 'rgba8'
                bpp = 4

            elif texture.format_ == 0x3b01:
                data = result[0]

                format_ = 'bgr5a1'
                bpp = 2

            data = BNTX.dds.formConv.torgba8(texture.width, texture.height, bytearray(data), format_, bpp, texture.compSel)
            img = QImage(data, texture.width, texture.height, QImage.Format_RGBA8888)

            if texture.width >= texture.height:
                pix = QPixmap(img.scaledToWidth(333, Qt.SmoothTransformation))

            else:
                pix = QPixmap(img.scaledToHeight(333, Qt.SmoothTransformation))

            self.preview.setPixmap(pix)

        else:
            self.resetPreviewer()

    def exportTex(self):
        self.bntx.extract(self.comboBox.currentIndex(), self.BFRESPath, 0)

    def exportTexAs(self):
        self.bntx.extract(self.comboBox.currentIndex(), self.BFRESPath, 1)

    def exportTexAll(self):
        for i in range(self.bntx.texContainer.count):
            self.bntx.extract(i, self.BFRESPath, 0, True)

    def replaceTex(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", "DDS (*.dds)")[0]
        if not file:
            return False

        index = self.comboBox.currentIndex()
        texture = self.bntx.textures[index]

        optionsDialog = QtWidgets.QDialog(self)
        optionsDialog.setWindowTitle("Options")

        tileModeLabel = QtWidgets.QLabel()
        tileModeLabel.setText("Tiling mode:")

        tileModeComboBox = QtWidgets.QComboBox()
        tileModeComboBox.addItems(["Optimal", "Linear"])

        if texture.tileMode in globals.tileModes:
            tileModeComboBox.setCurrentIndex(texture.tileMode)
        
        tileModeLayout = QtWidgets.QHBoxLayout()
        tileModeLayout.addWidget(tileModeLabel)
        tileModeLayout.addWidget(tileModeComboBox)

        SRGBLabel = QtWidgets.QLabel()
        SRGBLabel.setText("Use SRGB when possible:")

        SRGBCheckBox = QtWidgets.QCheckBox()
        SRGBCheckBox.setChecked(texture.format_ & 0xFF == 6)
        
        SRGBLayout = QtWidgets.QHBoxLayout()
        SRGBLayout.addWidget(SRGBLabel)
        SRGBLayout.addWidget(SRGBCheckBox)

        sparseBindingLabel = QtWidgets.QLabel()
        sparseBindingLabel.setText("Sparse Binding:")

        sparseBindingCheckBox = QtWidgets.QCheckBox()
        sparseBindingCheckBox.setChecked(bool(texture.sparseBinding))
        
        sparseBindingLayout = QtWidgets.QHBoxLayout()
        sparseBindingLayout.addWidget(sparseBindingLabel)
        sparseBindingLayout.addWidget(sparseBindingCheckBox)

        sparseResidencyLabel = QtWidgets.QLabel()
        sparseResidencyLabel.setText("Sparse Residency:")

        sparseResidencyCheckBox = QtWidgets.QCheckBox()
        sparseResidencyCheckBox.setChecked(bool(texture.sparseResidency))
        
        sparseResidencyLayout = QtWidgets.QHBoxLayout()
        sparseResidencyLayout.addWidget(sparseResidencyLabel)
        sparseResidencyLayout.addWidget(sparseResidencyCheckBox)

        importMipsLabel = QtWidgets.QLabel()
        importMipsLabel.setText("Import mipmaps if possible:")

        importMipsCheckBox = QtWidgets.QCheckBox()
        importMipsCheckBox.setChecked(False)
        
        importMipsLayout = QtWidgets.QHBoxLayout()
        importMipsLayout.addWidget(importMipsLabel)
        importMipsLayout.addWidget(importMipsCheckBox)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(optionsDialog.accept)
        buttonBox.rejected.connect(optionsDialog.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(tileModeLayout)
        layout.addLayout(SRGBLayout)
        layout.addLayout(sparseBindingLayout)
        layout.addLayout(sparseResidencyLayout)
        layout.addLayout(importMipsLayout)
        layout.addWidget(buttonBox)

        optionsDialog.setLayout(layout)

        if optionsDialog.exec_() != QtWidgets.QDialog.Accepted:
            return False

        tileMode = tileModeComboBox.currentIndex()
        SRGB = SRGBCheckBox.isChecked()
        sparseBinding = 1 if sparseBindingCheckBox.isChecked() else 0
        sparseResidency = 1 if sparseResidencyCheckBox.isChecked() else 0
        importMips = importMipsCheckBox.isChecked()

        texture_ = self.bntx.replace(texture, tileMode, SRGB, sparseBinding, sparseResidency, importMips, file)
        if texture_:
            self.bntx.textures[index] = texture_
            self.updateTexInfo(index)

    def save(self):
        with open(self.openLnEdt.text(), "wb") as out:
            out.write(self.bntx.save())

    def saveAs(self):
        file = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "Binary Resources Texture (*.bntx)")[0]
        if not file:
            return False

        with open(file, "wb") as out:
            out.write(self.bntx.save())

        self.openLnEdt.setText(file)

def main():
    app = QtWidgets.QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
