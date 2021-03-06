import os
import vtk
import numpy as np
from numpy import random
from astropy.io import fits

TRAVIS = os.environ.get('TRAVIS', 'false') == 'true'

# TODO: follow http://public.kitware.com/pipermail/paraview/2012-February/023989.html for setting color with column data
# Plot points as vertices of the Poly Object
class VtkPointCloud:

    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        # mapper = vtk.vtkPolyDataMapper()
        mapper = vtk.vtkOpenGLPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point, size=5):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
            self.vtkActor.GetProperty().SetPointSize(size)
            self.vtkActor.GetProperty().SetRenderPointsAsSpheres(True)
            self.vtkActor.GetProperty().SetOpacity(0.2)
            
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

pointCloud = VtkPointCloud()

# Test with astronomy catalog
inputFile='cloud_catalog_july14_2015.fits'
# data = numpy.genfromtxt(inputFile, delimiter=' ')
tbdata=fits.open(inputFile)[1].data
xyz=np.zeros((tbdata.shape[0], 3))
xyz[:, 0] = tbdata['x_gal']
xyz[:, 1] = tbdata['y_gal']
xyz[:, 2] = tbdata['z_gal']*10

# Test performance with fake data
# i=500000
# xyz = np.random.rand(i, 3)*i
# numberOfPoints = i

numberOfPoints = tbdata.shape[0]

for i in range(numberOfPoints):
    print('point pos', xyz[i][:3])
    pointCloud.addPoint(xyz[i][:3])

# Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(pointCloud.vtkActor)
renderer.SetBackground(.2, .3, .4)
renderer.ResetCamera()

# Render Window
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# Interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Begin Interaction
renderWindow.Render()

if not TRAVIS:
    renderWindowInteractor.Start()
