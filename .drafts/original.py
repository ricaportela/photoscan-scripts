# INIT ENVIRONMENT
# import stuff
import os
import glob
import PhotoScan
import math
import platform

# Python script for automated PhotoScan processing
# PhotoScan version 1.0.0

# DEFINE PROCESSING SETTINGS
print("---Defining processing settings...")
print(os.name)
if platform.system() == "Windows":
    # Define: Home directory (later this is referred as ".")
    HomeDirectory = "C:\\Users\\ricardo\\Desktop\\clientes\\tenis"
else:
    # Define: Home directory (later this is referred as ".")
    HomeDirectory = "/home/ricardo/temp/"

# Define: Camera calib file
CalibFile = HomeDirectory + "AgisoftLensCameraCalib.xml"
# Define: PhotoScan Project File
PhotoScanProjectFile = HomeDirectory + "PhotoScan_Project.psz"
# Define: Source images
AerialImagesPattern = HomeDirectory + "photos/*.jpg"
# Define: Orientation file
OrientationFile = HomeDirectory + "CameraOrientations_IMU.txt"
# Define: Cameras output file
CamerasOPKFile = HomeDirectory + "CameraOrientations_PhotoScan.opk"
# Define: Coordinate system
CoordinateSystemEPSG = "EPSG::32632"

# Define: DSMResolutions (in meters),
# 0 == GSD resolution
DSMResolutions = [1.00, 0]

# Define: OrthoImageResolutions (in meters)
# 0 == GSD resolution
OrthoImageResolutions = [1.00, 0]

# Define: AlignPhotosAccuracy ["high", "medium", "low"]
AlignPhotosAccuracy = "medium"

# Define: BuildGeometryQuality ["lowest", "low", "medium", "high", "ultra"]
BuildGeometryQuality = "medium"

# Define: BuildGeometryFaces [’low’, ‘medium’, ‘high’] or exact number.
BuildGeometryFaces = "medium"

# START ACTUAL SCRIPT (DO NOT EDIT ANYTHING BELOW THIS!)
# Set home folder
os.chdir(HomeDirectory)
print("Home directory: " + HomeDirectory)

# get main app objects
doc = PhotoScan.app.document
app = PhotoScan.Application()
doc.open("testes.psz")
chunk = doc.addChunk()
for chunk in doc.chunks:
    R = chunk.region.rot		# Bounding box rotation matrix
    C = chunk.region.center		# Bounding box center vector
    if chunk.transform:
        T = chunk.transform.matrix
        # scaling
        s = math.sqrt(T[0, 0]*T[0, 0] + T[0, 1]*T[0, 1] + T[0, 2]*T[0, 2])
        # scale matrix
        S = PhotoScan.Matrix([[s, 0, 0, 0], [0, s, 0, 0], [0, 0, s, 0], [0, 0, 0, 1]])
    else:
        S = PhotoScan.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        T = PhotoScan.Matrix([[R[0, 0], R[0, 1], R[0, 2], C[0]], [R[1, 0], R[1, 1], R[1, 2], C[1]], [R[2, 0], R[2, 1], R[2, 2], C[2]], [0, 0, 0, 1]])
        chunk.transform.matrix = S * T.inv()		# resulting chunk transformation matrix


# SET COORDINATE SYSTEM
print("---Settings coordinate system...")
# init coordinate system object
chunk.crs = PhotoScan.CoordinateSystem(CoordinateSystemEPSG)
CoordinateSystem = PhotoScan.CoordinateSystem()
if not(CoordinateSystem.init(CoordinateSystemEPSG)):
    app.messageBox("Coordinate system EPSG code not recognized!")
# define coordinate system in chunk
chunk.crs = CoordinateSystem
chunk.projection = CoordinateSystem

# FIND ALL PHOTOS IN PATH
AerialImageFiles = glob.glob(AerialImagesPattern)

# LOAD CAMERA CALIBRATION
print("---Loading camera calibration...")
print(AerialImageFiles)
# we need to open first image to define image size
chunk.addPhotos(AerialImageFiles)
cam = chunk.cameras[0]
cam.open(AerialImageFiles[0])
# Load sensor calib
user_calib = PhotoScan.Calibration()
if not(user_calib.load(CalibFile)):
    app.messageBox("Loading of calibration file failed!")
# build sensor object
sensor = chunk.addSensor()
sensor.label = "MyCamera"
sensor.width = sensor.width
sensor.height = sensor.height
sensor.fixed = False
sensor.user_calib = user_calib
chunk.addSensor()

# LOAD AERIAL IMAGES
print("---Loading images...")
# load each image
for FileName in AerialImageFiles:
    print("File: " + FileName)
    cam = chunk.cameras[0]
    if not(cam.open(FileName)):
        app.messageBox("Loading of image failed: " + FileName)
    cam.label = cam.path.rsplit("/", 1)[1]
    cam.sensor = sensor
    chunk.cameras.add(cam)

# LOAD CAMERA ORIENTATIONS
print("---Loading initial photo orientations...")
print("File: " + OrientationFile)
# build ground control
chunk.ground_control.projection = CoordinateSystem
chunk.ground_control.crs = CoordinateSystem
if not(chunk.ground_control.load(OrientationFile, "csv")):
    app.messageBox("Loading of orientation file failed!")
chunk.ground_control.apply()

# SAVE PROJECT
print("---Saving project...")
print("File: " + PhotoScanProjectFile)
if not(doc.save(PhotoScanProjectFile)):
    app.messageBox("Saving project failed!")

# All init done! Ready to start processing.

# ALIGN PHOTOS
print("---Aligning photos ...")
print("Accuracy: " + AlignPhotosAccuracy)
chunk.matchPhotos(accuracy=AlignPhotosAccuracy, preselection="ground control")
chunk.alignPhotos()

# SAVE PROJECT
print("---Saving project...")
print("File: " + PhotoScanProjectFile)
if not(doc.save(PhotoScanProjectFile)):
    app.messageBox("Saving project failed!")

# If ground control markers are used, code should stop here and user should click them in now

# BUILD GEOMETRY
print("---Building Geometry...")
print("Quality: " + BuildGeometryQuality)
print("Faces: " + str(BuildGeometryFaces))
# THESE ROWS WERE ALTERED IN v1.0.0 UPDATE
# chunk.buildDepth(quality=BuildGeometryQuality)
# chunk.buildModel(object="height field", geometry="smooth", faces=BuildGeometryFaces)
if not(chunk.buildDenseCloud(quality=BuildGeometryQuality)):
    app.messageBox("Builde Dense Cloud failed!")

if not(chunk.buildModel(surface="height field", source="dense", interpolation="enabled", faces=BuildGeometryFaces)):
    app.messageBox("Build mesh model failed!")

# SAVE PROJECT
print("---Saving project...")
print("File: " + PhotoScanProjectFile)
if not(doc.save(PhotoScanProjectFile)):
    app.messageBox("Saving project failed!")

# Actual processing done
# EXPORT DATA:

# EXPORT CAMERAS
print("---Exporting camera positions...")
if not(chunk.exportCameras(CamerasOPKFile, "opk", chunk.projection)):
    app.messageBox("Exporting Cameras OPK failed!")

# CALCULATE THE BEST SENSIBLE PIXEL SIZES
Resolution = 0
# if Resolution == 0:
# Get average camera altitude and focal length
N_cameras = len(chunk.cameras)
CamAlt = 0.0
focal_length = 0.0
for i in range(N_cameras):
    CamAlt += chunk.ground_control.locations[chunk.cameras[i]].coord[2]
    focal_length += (chunk.cameras[i].sensor.calibration.fx + chunk.cameras[0].sensor.calibration.fy) / 2

CamAlt /= N_cameras
focal_length /= N_cameras
# Get average ground  altitude
N_points = len(chunk.point_cloud.points)
GroundAlt = 0.0
for i in range(N_points):
    GroundAlt += chunk.point_cloud.points[i].coord.z

GroundAlt = GroundAlt / N_points
# calculate Ground sampling distance
GroundSamplingDistance = math.fabs(CamAlt-GroundAlt) / focal_length
# round it to next millimeter
GroundSamplingDistance = math.ceil(GroundSamplingDistance * 1000)/1000

# EXPORT DSM(S)
print("---Exporting Digital Surface Model(s)...")
for Resolution in DSMResolutions:
    if Resolution == 0:
        Resolution = GroundSamplingDistance

    FileName = ".\\DSM_PixelSize=" + str(Resolution) + "m.tif"
    print("File: " + FileName)
    if not(chunk.exportDem(FileName, format="tif", dx=Resolution, dy=Resolution, projection=chunk.projection)):
        app.messageBox("Exporting DSM failed: " + FileName)


# EXPORT ORTHOIMAGE(S)
print("---Exporting Orthoimage(s)...")
for Resolution in OrthoImageResolutions:
    if Resolution == 0:
        Resolution = GroundSamplingDistance

    FileName = ".\\OrthoImage_PixelSize=" + str(Resolution) + "m.tif"
    print("File: " + FileName)
    if not(chunk.exportOrthophoto(FileName, format="tif", projection=chunk.projection, blending="mosaic", dx=Resolution, dy=Resolution)):
        app.messageBox("Exporting orthoimage failed: " + FileName)

# SAVE PROJECT
print("---Saving project...")
print("File: " + PhotoScanProjectFile)
if not(doc.save(PhotoScanProjectFile)):
    app.messageBox("Saving project failed!")

# Close photoscan
# app.quit()
