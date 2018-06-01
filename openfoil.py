#!/usr/bin/python3

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMessageBox, QTextEdit)
from PyQt5 import uic

import vtk
print(vtk)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from foamreader import FoamFile

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.title = 'OpenFoil'
        self.ui = uic.loadUi("mainwindow.ui", self)

        # create a VTK render window within the ui.vtkFrame object
        self.vtkWidget = QVTKRenderWindowInteractor(self.ui.flowFrame)
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0.1, 0.2, 0.4)
        # self.vtkWidget.setGeometry(0,0,600,400)
        # geo = self.ui.flowFrame.geometry()
        # self.vtkWidget.setGeometry(geo)
        # TODO: the widget should scale filling the available space
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        
        # Define custom interaction.
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # this way the mouse doesn't move anything
        # self.iren.SetInteractorStyle(None)
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        # this way we just disable the left mouse button
        self.iren.RemoveObservers('LeftButtonPressEvent')
        # self.iren.AddObserver('LeftButtonPressEvent', DummyFunc1, 1.0)
        # self.iren.AddObserver('LeftButtonPressEvent', DummyFunc2, -1.0)
        
        # TODO: we want to assign exactly the function of the middle
        # mouse button (pan) to the left mouse button

        # read mesh data
        ff = FoamFile('run/alfa200/constant/polyMesh/points')
        point_data = ff.readPoints()
        print(len(point_data))
        print(point_data)
        ff = FoamFile('run/alfa200/constant/polyMesh/faces')
        face_data = ff.readFaces()
        print(len(face_data))
        print(face_data)
        
        # Create a wire frame from the mesh data
        vtkPoints = vtk.vtkPoints()
        vtkPoints.SetNumberOfPoints(len(point_data))
        # we switch coordinates y and z
        # the airfoils then lies in the x-y plane
        for i,p in enumerate(point_data):
            vtkPoints.SetPoint(i,p[0], p[2], p[1])
        lines = vtk.vtkCellArray()
        for i,face in enumerate(face_data):
            lines.InsertNextCell(5)
            for ind in face:
                lines.InsertCellPoint(ind)
            lines.InsertCellPoint(face[0])
        mesh = vtk.vtkPolyData()
        mesh.SetPoints(vtkPoints)
        mesh.SetLines(lines)
        
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        # mapper.SetInputConnection(source.GetOutputPort())
        mapper.SetInputData(mesh)

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        camera = vtk.vtkCamera ();
        camera.SetPosition(0, 0, 20);
        camera.SetFocalPoint(0, 0, 0);

        self.ren.AddActor(actor)
        # self.ren.ResetCamera();
        self.ren.SetActiveCamera(camera);
        
        self.show()
        self.iren.Initialize()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()
 
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
    

