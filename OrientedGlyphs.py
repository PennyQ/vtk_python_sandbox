import vtk

# TODO: assign each data point to glyph3d position
sphereSource = vtk.vtkSphereSource()
sphereSource.Update()

input_data = vtk.vtkPolyData()
input_data.ShallowCopy(sphereSource.GetOutput())

arrowSource = vtk.vtkArrowSource() # The arrow shpae: Appends a cylinder to a cone to form an arrow.

glyph3D = vtk.vtkGlyph3D()
glyph3D.SetSourceConnection(arrowSource.GetOutputPort())
glyph3D.SetVectorModeToUseNormal()
print('input data', input_data) # ploydata
glyph3D.SetInputData(input_data)
glyph3D.SetScaleFactor(.2)
glyph3D.Update()

# Visualize
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(glyph3D.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)
renderer.SetBackground(.3, .6, .3) # Background color green

renderWindow.Render()
renderWindowInteractor.Start()