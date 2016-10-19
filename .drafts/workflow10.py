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
    HomeDirectory = "C:\\temp"
else:
    # Define: Home directory (later this is referred as ".")
    HomeDirectory = "/home/ricardo/clientes/geotests/"

# Define: Camera calib file
CalibFile = HomeDirectory + "AgisoftLensCameraCalib.xml"
# Define: PhotoScan Project File
PhotoScanProjectFile = HomeDirectory + "banquinho_Project.psz"
# Define: Source images
AerialImagesPattern = HomeDirectory + "/banquinho/*.JPG"
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
os.chdir(HomeDirectory)
print("Home directory: " + HomeDirectory)

# get main app objects
doc = PhotoScan.app.document
app = PhotoScan.Application()
chunk = doc.addChunk()
# SAVE PROJECT
print("---Saving project...")
print("File: " + PhotoScanProjectFile)
if not(doc.save(PhotoScanProjectFile)):
    app.messageBox("Salvando Projeto")
# parametros
accuracy = PhotoScan.Accuracy.HighAccuracy  # align photos accuracy
preselection = PhotoScan.Preselection.GenericPreselection
keypoints = 40000  # align photos key point limit
tiepoints = 40000  # align photos tie point limit
#source = PhotoScan.PointsSource.DensePoints  # build mesh source
surface = PhotoScan.SurfaceType.Arbitrary  # build mesh surface type
quality = PhotoScan.Quality.MediumQuality  # build dense cloud quality
filtering = PhotoScan.FilterMode.AggressiveFiltering  # depth filtering
interpolation = PhotoScan.Interpolation.EnabledInterpolation  # build mesh interpolation
face_num = PhotoScan.FaceCount.HighFaceCount  # build mesh polygon count
mapping = PhotoScan.MappingMode.GenericMapping  # build texture mapping
atlas_size = 8192
blending = PhotoScan.BlendingMode.MosaicBlending  # blending mode
color_corr = False

# FIND ALL PHOTOS IN PATH
AerialImageFiles = glob.glob(AerialImagesPattern)

# Load Photos
print(AerialImageFiles)
chunk.addPhotos(AerialImageFiles)

print("Script started....")
# alinhar Photos
chunk.matchPhotos(accuracy=accuracy, preselection=preselection, filter_mask=False, keypoint_limit=keypoints, tiepoint_limit=tiepoints)
chunk.alignCameras()
chunk.optimizeCameras()
# building dense cloud
PhotoScan.app.gpu_mask = 1  # GPU devices binary mask
PhotoScan.app.cpu_cores_inactive = 2  # CPU cores inactive
chunk.buildDenseCloud(quality=quality, filter=filtering)

# orotomosaico
# DSM

PhotoScan.app.update()
