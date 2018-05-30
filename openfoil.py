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
        self.vtkWidget = QVTKRenderWindowInteractor(self.ui.vtkFrame)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

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
    
    
"""
	# Generate lines in between
	lines = vtk.vtkCellArray()
	lines.InsertNextCell(len(pts)+int(closed))
	for i,p in enumerate(pts):
		lines.InsertCellPoint(i)
	if closed:
		lines.InsertCellPoint(0)
	
	polygon = vtk.vtkPolyData()
	polygon.SetPoints(points)
	polygon.SetLines(lines)
"""

