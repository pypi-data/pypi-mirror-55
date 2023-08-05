#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import *
import os
import sys
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.widgets import RectangleSelector
from matplotlib.figure import Figure
import h5py
import numpy as np
np.seterr(divide='ignore')
from . import __init__ as xrdInit

class MplCanvas(FigureCanvas):
    """ Mpl container class"""

    def __init__(self, parent=None):
        self.fig = Figure()
        super().__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

        parent.layout().addWidget(self)

class XpadCanvas(MplCanvas):
    """ Upper Xpad canvas """

    def __init__(self, parent, ui, data):
        super().__init__(parent)
        self.logScale = ui.XpadLogScale
        self.frame = ui.ScanSlider
        self.roiMax = 1
        self.data = data
        self.update_plot_pane = None
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    def update_plot(self):
        xpadData = self.data.files[0].xpad[self.frame.value()]
        for region in self.data.regions:
            if region.Active():
                self.roiMax = np.amax(
                    xpadData[region.getSlice()])

        self.axes.cla()
        self.axes.axis('off')
        

        def scale_fnt(x):
            return x if self.logScale.isChecked() else np.log(x)

        self.axes.imshow(
            scale_fnt(xpadData), cmap='jet', vmin=0, vmax=self.roiMax)

        for region in self.data.regions:
            if region.Active():
                self.rSelector = RectangleSelector(self.axes, self.rectangle_callback,
                                                    drawtype='box', useblit=False, button=[1],
                                                    minspanx=5, minspany=5, spancoords='data',
                                                    interactive=True, rectprops=dict(facecolor='None', edgecolor='red', alpha=0.8, fill=False))
                self.rSelector.to_draw.set_visible(True)
                self.rSelector.extents = region.get()
            else:
                self.axes.add_patch(patches.Rectangle((region.X(),region.Y()),region.L(),region.W(),linewidth=1,edgecolor='black',facecolor='none'))

        self.draw()

    def rectangle_callback(self, eclick, erelease):
        """ rectangle selection in xpad pane  """

        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        for region in self.data.regions:
            if region.Active():
                region.set(int(min(x1, x2)), int(min(y1, y2)),
                        int(np.abs(x1-x2)), int(np.abs(y1-y2)))

        self.update_plot()
        self.update_plot_pane()

class PlotCanvas(MplCanvas):
    """ lower plot canvas """

    def __init__(self, parent, ui, data):
        super().__init__(parent)
        self.logScale = ui.PlotLogScale
        self.frame = ui.ScanSlider
        self.offset = ui.PlotOffset
        self.xBox = ui.xBox
        self.yBox = ui.yBox
        self.data = data
        self.clicked = None
        self.showCursor = True

    def update_plot(self):
        """ Update function for lower plot pane """

        self.axes.cla()
        size = self.fig.get_size_inches()*self.fig.dpi
        offset = int(self.offset.text())

        for file in self.data.files:
            file.plot_x = []
            file.plot_y = []

            if self.xBox.currentText() == "xpad_image" or self.yBox.currentText() == "xpad_image":
                summe = []
                for region in self.data.regions:
                    # first region is background region (type = 0)
                    sss = np.empty(file.xpad.shape[0])
                    for i in range(file.xpad.shape[0]):
                        sss[i] = np.sum(file.xpad[i][region.getSlice()])
                    sss /= region.L()*region.W()

                    if region.type == 0:           
                        background = sss
                    else:
                        summe.append(sss-background)

            if self.xBox.currentText() == "xpad_image":
                for s in summe:
                    file.plot_x.append(s[offset:])
                file.plot_xlabel = "I (a.u.)"
            elif self.xBox.currentText() == "slices":
                file.plot_x.append(range(file.xpad.shape[0]-offset))
                file.plot_xlabel = "Slices"
            else:
                file.plot_x.append(file.nxs[self.xBox.currentText()][offset:])
                file.plot_xlabel = self.xBox.currentText()

            if self.yBox.currentText() == "xpad_image":
                for s in summe:
                    file.plot_y.append(s[offset:])
                file.plot_ylabel = "I (a.u.)"
            elif self.yBox.currentText() == "slices":
                file.plot_y.append(range(file.ypad.shape[0]-offset))
                file.plot_ylabel = "Slices"
            else:
                file.plot_y.append(file.nxs[self.yBox.currentText()][offset:])
                file.plot_ylabel = self.yBox.currentText()

            if self.logScale.isChecked():
                for x in file.plot_x:
                    for y in file.plot_y:
                        self.axes.semilogy(x,y)
                # self.axes.semilogy(file.plot_x, file.plot_y)
            else:
                for x in file.plot_x:
                    for y in file.plot_y:
                        self.axes.plot(x,y)
                # self.axes.plot(file.plot_x, file.plot_y)

            # print("update_plot")
            # print(len(file.plot_x))

        self.axes.set_xlabel(self.data.files[0].plot_xlabel)
        self.axes.set_ylabel(self.data.files[0].plot_ylabel)

        # TODO
        if self.showCursor:
            i = -1 # start by -1, so background regions sets it to 0
            for region in self.data.regions[1:]:
                i += 1
                if region.Active():
                    break
            else:
                i = 0

            x, y = self.data.files[0].plot_x[0][max(0,self.frame.value()-offset)], self.data.files[0].plot_y[i][max(0,self.frame.value()-offset)]
            self.axes.axhline(y, color='k')
            self.axes.axvline(x, color='k')
            self.axes.text((size[0]-10)/size[0], (size[1]-10)/size[1], 
                '{:f}'.format(x) + ', ' + '{:f}'.format(y), 
                horizontalalignment='right', verticalalignment='top', transform=self.axes.transAxes)

        self.mpl_connect(
            'button_press_event', self.plot_pane_clicked)
        self.mpl_connect(
            'button_release_event', self.plot_pane_released)
        self.mpl_connect(
            'motion_notify_event', self.plot_pane_on_move)

        self.fig.subplots_adjust(left=(75/size[0]), bottom=(50/size[1]), right=0.999, top=0.995, wspace=None, hspace=None)
        self.draw()

    def plot_pane_clicked(self, event):
        """ Connect function for lower plot pane """
        if not event.inaxes:
            return
        self.clicked = True
        self.plot_pane_on_move(event)

    def plot_pane_released(self, event):
        """ Connect function for lower plot pane """
        self.clicked = None

    def plot_pane_on_move(self, event):
        """ Connect function for lower plot pane """
        if not event.inaxes:
            return
        if not self.clicked:
            return
        
        self.frame.setFocus()

        offset = int(self.offset.text())
        ascending_factor = 1 if self.data.files[0].plot_x[0][0] < self.data.files[0].plot_x[0][-1] else -1

        plot_x = [*self.data.files[0].plot_x[0]] * ascending_factor
        x = event.xdata * ascending_factor
        indx = min(np.searchsorted(plot_x, [x])[
                   0], len(plot_x) - 1)

        if indx != self.frame.value():
            self.frame.setValue(indx + offset)
            # also calls ScanSlider.valueChanged automatically

class Data():
    """ shared data class """

    def __init__(self):
        """ fill in some initial data """

        self.regions = [Region(0, 170, 40, 50, 50),Region(1, 280, 0, 50, 239)]
        self.regions[1].active = True

        self.files = [Files()]

        self.mask_file = ""
        self.mask = np.ones(np.shape(self.files[0].xpad[0]))
        self.mask_border_factor = 0

class Files():
    def __init__(self):
        self.filename = ""
        self.nxs = {"omega": [0]}
        self.xpad = np.load(os.path.abspath(os.path.dirname(__file__)+"/assets/logo.npy"))

class Region():
    """ Region class for Region of Interest and Background Region """

    def __init__(self, type = 1, x = 10, y = 10, l = 10, w = 10):
        self.active = False
        self.type = type  # 1 for roi or 0 for background
        self.x, self.y, self.l, self.w = x, y, l, w
        self.uiX, self.uiY, self.uiL, self.uiW = None, None, None, None
        self.uiActive = None

    def set(self, x = None, y = None, l = None, w = None):
        if x is None:
            self.X(self.x)
        else:
            self.X(x)
        if y is None:
            self.Y(self.y)
        else:
            self.Y(y)
        if l is None:
            self.L(self.l)
        else:
            self.L(l)
        if w is None:
            self.W(self.w)
        else:
            self.W(w)

    def X(self,x = None):
        """ unified get and set fn """
        if x is None:
            if self.uiX is not None:
                self.x = int(self.uiX.text())
            return self.x
        else:
            self.x = x
            if self.uiX is not None:
                self.uiX.setText(str(x))

    def Y(self,y = None):
        """ unified get and set fn """
        if y is None:
            if self.uiY is not None:
                self.y = int(self.uiY.text())
            return self.y
        else:
            self.y = y
            if self.uiY is not None:
                self.uiY.setText(str(y))

    def L(self,l = None):
        """ unified get and set fn """
        if l is None:
            if self.uiL is not None:
                self.l = int(self.uiL.text())
            return self.l
        else:
            self.l = l
            if self.uiL is not None:
                self.uiL.setText(str(l))

    def W(self,w = None):
        """ unified get and set fn """
        if w is None:
            if self.uiW is not None:
                self.w = int(self.uiW.text())
            return self.w
        else:
            self.w = w
            if self.uiW is not None:
                self.uiW.setText(str(w))

    def get(self):
        x = self.X()
        y = self.Y()
        l = self.L()
        w = self.W()
        return (x, x + l, y, y + w)

    def getSlice(self):
        x = self.X()
        y = self.Y()
        l = self.L()
        w = self.W()
        return (slice(y, y + w), slice(x, x + l))

    def Active(self):
        if self.uiActive is not None:
            self.active = self.uiActive.isChecked()
        return self.active

class XrdWindow(QtWidgets.QMainWindow):
    """ main window class """

    def __init__(self):
        super(XrdWindow, self).__init__()
        # self.ui = uic.loadUi(sys.path[0]+"/assets/xrd.ui", self)
        # self.ui = uic.loadUi("./assets/xrd.ui", self)
        self.ui = uic.loadUi(os.path.abspath(os.path.dirname(__file__)+"/assets/xrd.ui"), self)
        self.data = Data()

        self.xpad_widget = XpadCanvas(self.ui.XpadWidget, self.ui, self.data)
        self.plot_widget = PlotCanvas(self.ui.PlotWidget, self.ui, self.data)
        self.xpad_widget.update_plot_pane = self.plot_widget.update_plot

        # connect signals from ui to functions
        self.ui.actionOpen.triggered.connect(self.open_folder)
        self.ui.actionLoad_Mask.triggered.connect(self.load_mask)
        self.ui.actionSave_Graph.triggered.connect(self.save_graph)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.open_about)
        self.ui.listWidget.clicked.connect(self.list_change)
        self.ui.ScanSlider.valueChanged.connect(self.change_slider)
        self.ui.XpadLogScale.stateChanged.connect(self.xpad_widget.update_plot)
        self.ui.PlotLogScale.stateChanged.connect(self.plot_widget.update_plot)
        self.ui.xBox.currentIndexChanged.connect(self.plot_widget.update_plot)
        self.ui.yBox.currentIndexChanged.connect(self.plot_widget.update_plot)
        self.ui.PlotOffset.editingFinished.connect(self.update_plots)
        self.ui.regionButton.clicked.connect(self.open_region_editor)

        self.ui.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.listWidget.setStyleSheet(""" QListWidget:item:selected:active {
                                     background: blue;
                                }
                                QListWidget:item:selected:!active {
                                     background: gray;
                                }
                                QListWidget:item:selected:disabled {
                                     background: gray;
                                }
                                QListWidget:item:selected:!disabled {
                                     background: blue;
                                }
                                """
                                      )
        self.ui.listWidget.setEnabled(True)

    #    self.update_plots()
    
    def resizeEvent(self,event):
        self.update_plots()
        return super(XrdWindow, self).resizeEvent(event)

    def update_plots(self):
        self.xpad_widget.update_plot()
        self.plot_widget.update_plot()

    def open_folder(self):
        """ User input: folder selection and loading of .nxs """

        self.ui.listWidget.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Pick a folder")

        if directory:
            for file_name in os.listdir(directory):
                if file_name[-4:] == ".nxs":
                    item = QtWidgets.QListWidgetItem(
                        file_name[-9:-4], self.ui.listWidget)
                    # item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                    #               QtCore.Qt.ItemIsEnabled)
                    # item.setCheckState(QtCore.Qt.Unchecked)
                    item.setData(QtCore.Qt.StatusTipRole,
                                 directory+"/"+file_name)
            self.ui.listWidget.sortItems()

    def load_mask(self):
        """ User input: load mask """

        borderMask = np.zeros(np.shape(self.data.files[0].xpad[0]))
        borderMask[119:121, :] = 1
        for i in range(1, 7):
            borderMask[:, i*80-1:i*80+1] = 1
        self.data.mask_border_factor = 0.4
        
        mask_file = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select the mask file")

        if mask_file:
            self.data.mask_file = mask_file[0]
            self.data.mask = (1-np.load(self.data.mask_file)) + borderMask * self.data.mask_border_factor
            self.xpad_widget.axes.imshow(self.data.mask, cmap='jet')
            self.xpad_widget.draw()

    def list_change(self):
        """ User input: selection of item in list """

        self.data.files.clear()
        for item in self.ui.listWidget.selectedItems():
            self.data.files.append(Files())
            self.data.files[-1].filename = item.data(QtCore.Qt.StatusTipRole)

            nxsf = h5py.File(self.data.files[-1].filename,"r")
            self.data.files[-1].nxs = nxsf[list(nxsf)[0]]["scan_data"]
            self.data.files[-1].xpad = np.array(
                [x * self.data.mask for x in self.data.files[-1].nxs["xpad_image"]])

        filename = self.data.files[0].filename.split(os.sep)[-1]
        self.setWindowTitle(filename + " - XRD Viewer")

        # temporary disconnect signal to avoid update_plot while renewing the content of xBox and yBox
        self.ui.xBox.currentIndexChanged.disconnect(self.plot_widget.update_plot)
        self.ui.yBox.currentIndexChanged.disconnect(self.plot_widget.update_plot)

        xBoxOld = self.ui.xBox.currentText()
        yBoxOld = self.ui.yBox.currentText()
        self.ui.xBox.clear()
        self.ui.yBox.clear()

        for x in list(self.data.files[0].nxs) + ["slices"]:
            self.ui.xBox.addItem(x)
            self.ui.yBox.addItem(x)

        if xBoxOld in list(self.data.files[0].nxs):
            self.ui.xBox.setCurrentText(xBoxOld)
        if yBoxOld in list(self.data.files[0].nxs):
            self.ui.yBox.setCurrentText(yBoxOld)

        self.ui.xBox.currentIndexChanged.connect(self.plot_widget.update_plot)
        self.ui.yBox.currentIndexChanged.connect(self.plot_widget.update_plot)

        val = self.ui.ScanSlider.value()
        self.ui.ScanSlider.setMaximum(self.data.files[0].xpad.shape[0]-1)
        self.ui.ScanSlider.setValue(min(val, self.ui.ScanSlider.maximum()))

        self.xpad_widget.update_plot()
        self.plot_widget.update_plot()

        self.ui.actionSave_Graph.setEnabled(True)

    def change_slider(self):
        """ User input: change of the slider """
        self.xpad_widget.update_plot()
        self.plot_widget.update_plot()

    def save_graph(self):
        """ save the plot as file """

        while True:
            dialog = QFileDialog(caption="Save File...") # SaveDialog doesn't check, if file with appended extension already exists...
            dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
            dialog.setDefaultSuffix("txt")
            dialog.setOption(QFileDialog.DontConfirmOverwrite) 
            dialog.setAcceptMode(QFileDialog.AcceptSave)
            # dialog.setNameFilters(["Plain Text (*.txt)","Image (*.png *.jpg *.tif *.pdf)"])
            dialog.setMimeTypeFilters(["application/octet-stream","text/plain","image/jpeg","image/png","application/pdf"])
            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.selectedFiles()[0]
                if filename[-4:] not in [".txt",".png",".jpg",".pdf"]: # testing supported extension
                    msg = QMessageBox()
                    msg.setWindowTitle("Save File...")
                    msg.setIcon(QMessageBox.Warning)

                    msg.setText("The specified filename has an unsupported extension:\n"+filename+"\n\nSupported extensions are: .txt, .png, .jpg, .pdf\n\nOk to select a new file name, Cancel to abort")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    if(msg.exec_() == QMessageBox.Ok):
                        continue
                    else:
                        filename = None
                        break

                if os.path.isfile(filename): # testing existence and overwrite ok
                    msg = QMessageBox()
                    msg.setWindowTitle("Save File...")
                    msg.setIcon(QMessageBox.Warning)

                    msg.setText("The specified filename already exists:\n"+filename+"\n\nOk to overwrite, Cancel to select a new name")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    if(msg.exec_() == QMessageBox.Ok):
                        break
                else:
                    # file doesn't exist
                    break
            else:
                # dialog aborted
                filename = False
                break

        if filename:
            if filename[-4:] == ".txt":
                f = open(filename, "w")
                f.write("# xrd-viewer plot\n")
                for file in self.data.files:
                    f.write("# analysed file: "+file.filename+"\n")
                f.write("# used mask: "+self.data.mask_file+"\n")
                if self.data.mask_border_factor != 0:
                    f.write("# with border factor of " + str(self.data.mask_border_factor) + " for detector grid\n")
                for region in self.data.regions:
                    if region.type == 1:
                        f.write("# selected region: "+str(region.X())+" "+str(region.Y())+" "+str(region.L())+" "+str(region.W())+"\n")
                    else:
                        f.write("# selected background region: "+str(region.X())+" "+str(region.Y())+" "+str(region.L())+" "+str(region.W())+"\n")  
                f.write("# \n")
                f.write("# " + self.data.files[0].plot_xlabel+"\t"+self.data.files[0].plot_ylabel+"\n")
                for file in self.data.files:
                    for xx in file.plot_x:
                        for yy in file.plot_y:
                            for x,y in zip(xx,yy):
                                f.write(str(x)+"\t"+str(y)+"\n")
                            f.write("\n")
                f.close()

            elif filename[-4:] == ".png" or filename[-4:] == ".jpg" or filename[-4:] == ".pdf" :
                self.plot_widget.showCursor = False
                self.plot_widget.update_plot()
                self.plot_widget.fig.savefig(filename)
                self.plot_widget.showCursor = True
                self.plot_widget.update_plot()

            else:
                pass
                # print("invalid extension")


    def open_region_editor(self):
        """ Editor for regions of interest or background """
        try:
            self.regionWidget.show()
            self.regionWidget.activateWindow()
        except:
            self.regionWidget = RegionWidget(
                self.data.regions, self.update_plots)
            self.regionWidget.show()

    def open_about(self):
        """ open About window """
        try:
            self.aboutWidget.show()
            self.aboutWidget.activateWindow()
        except:
            self.aboutWidget = AboutWidget()
            self.aboutWidget.show()

    def closeEvent(self, event):
        try:
            self.regionWidget.close()
        except:
            pass
        try:
            self.aboutWidget.close()
        except:
            pass


class RegionWidget(QWidget):
    """ class for region editor gui """

    def __init__(self, regions, update_fn):
        super().__init__()
        self.regions = regions
        self.update_fn = update_fn

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Region Editor')

        self.tab = QVBoxLayout()
        self.tableRows = []

        self.textLayout = QHBoxLayout()
        for text in ["Active", "X Pos", "Y Pos", "Length", "Width"]:
            label = QLabel(text)
            label.setFixedWidth(35 if text == "Active" else 60)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.textLayout.addWidget(label)

        self.selectionGroup = QtWidgets.QButtonGroup(self)
        for region in self.regions:
            self.addRow(region)
        # for row in self.tableRows:
        #     self.tab.addLayout(row.layout)

        self.buttonLayout = QHBoxLayout()
        self.new_button = QPushButton("New Region")
        self.new_button.clicked.connect(self.addRow)
        self.buttonLayout.addWidget(self.new_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.buttonLayout.addWidget(self.close_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.textLayout)
        self.layout.addLayout(self.tab)
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)

    def closeEvent(self, event):
        # release all ui assignments
        pass

    def addRow(self,region=False):
        if region is False:
            region = Region(1,20,0,20,300)
            self.regions.append(region)
        # print(region)
        self.tableRows.append(tableRow(region, self.update_fn, self.selectionGroup))
        self.tab.addLayout(self.tableRows[-1].layout)


class tableRow():
    """ item class for region editor """

    def __init__(self, region, update_fn,radioGrp):
        self.selected = False

        self.layout = QHBoxLayout()
        region.uiActive = QtWidgets.QRadioButton()
        radioGrp.addButton(region.uiActive)
        if region.active:
            region.uiActive.setChecked(True)
        region.uiActive.toggled.connect(update_fn)
        self.layout.addWidget(region.uiActive)

        region.uiX, region.uiY, region.uiL, region.uiW = \
            QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        for ui in [region.uiX, region.uiY, region.uiL, region.uiW]:
            ui.setFixedWidth(60)
            ui.editingFinished.connect(update_fn)
            self.layout.addWidget(ui)

        region.set()

    def __del__(self):
        pass

class AboutWidget(QWidget):
    """ class for about Widget """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('About') 

        self.button = QPushButton("Close")
        self.button.clicked.connect(self.close)

        self.text = QLabel("\nXRD-Viewer\nVersion: "+xrdInit.__version__+"\n\ncreated by\n\nSebastian Schenk (sebastian.schenk@physik.uni-halle.de)\n")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
