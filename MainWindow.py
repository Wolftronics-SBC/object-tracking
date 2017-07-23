#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:05:43 2017

@author: ali
"""

from PyQt5 import QtWidgets
import sys
from DrawableMovieLabel import DrawableMovieLabel
import pandas as pd

sys.path.append('forms')
from ui_MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.movie = DrawableMovieLabel()
        self.ui.horizontalLayout_2.addWidget(self.movie)
        self.ui.pushButton_browse.clicked.connect(self.openFile)
        self.ui.pushButton_start.clicked.connect(self.start_stop)
        self.ui.pushButton_remove.clicked.connect(self.removeTrack)
        self.ui.pushButton_save_annotation.clicked.connect(
                self.save_annotations)
        self.ui.pushButton_browse_annotaion.clicked.connect(
                self.open_annotations)
        self.ui.listView.setModel(self.movie.model)
        self.ui.listView.setEditTriggers(
                QtWidgets.QAbstractItemView.DoubleClicked)
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.valueChanged.connect(self.movie.seekToPercent)
        self.movie.progress.connect(self.ui.horizontalSlider.setValue)

    def open_annotations(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            'Annotation File')
        self.movie.annotations = pd.read_csv(fileName)
        self.movie.globalId = self.movie.annotations['id'].max()+1
        self.ui.lineEdit_annotaion.setText(fileName)

    def save_annotations(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            'Annotation File',
                                                            'annotation.csv')
        if(fileName):
            self.movie.annotations.to_csv(fileName)

    def removeTrack(self):
        row = self.ui.listView.currentIndex().row()
        self.movie.model.removeRow(row)

    def start_stop(self):
        if(self.ui.pushButton_start.text() == 'Start'):
            self.movie.start()
            self.ui.pushButton_start.setText('Stop')
        else:
            self.movie.stop()
            self.ui.pushButton_start.setText('Start')

    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'open video')
        if(fileName):
            self.ui.lineEdit.setText(fileName)
            self.movie.openVideo(fileName)
