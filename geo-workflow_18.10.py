# INIT ENVIRONMENT
# import stuff
import os
import sys
# import glob
import json
import platform
import PhotoScan
import datetime


# ###  project_name, project_folder, folder_images###
# if platform.system() == "Linux":
#     project_name   = 'banquinho'
#     project_folder = "/home/ricardo/temp/"
#     folder_images  = "photos/"
# else:
#     project_name   = 'banquinho'
#     project_folder = "C:\\temp4\\"
#     folder_images  = "photos\\"
#
doc_name           = project_name + ".psz"
#
photos_dir         = os.path.join( project_folder, photos_directory )
photos             = os.listdir(photos_dir)
photos             = [os.path.join(photos_dir,p) for p in photos]
images_pattern     = photos
#
# # markers.xml - verify if file exist
# marker_file = project_folder + folder_images + "markers.xml"
# print(marker_file)
#
# # file.txt - verify if file exist
# reference_file = project_folder + folder_images + "file.csv"
# print(reference_file)

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(PROJECT_DIR, 'config.json'), 'r') as f:
    config = json.load(f)

print("*************************************")
print(config["project_name"])
print(config["project_folder"])
print(config["photos_directory"])
print(config["accuracy"])
print("*************************************")

###  project_name, project_folder, photos_directory###
project_name     = config["project_name"]
project_folder   = os.path.join(config["project_folder"])
photos_directory  = config["photos_directory"]

doc_name           = project_name + ".psz"

photos_dir         = os.path.join( project_folder, photos_directory )
photos             = os.listdir(photos_dir)
photos             = [os.path.join(photos_dir,p) for p in photos]
images_pattern     = photos

# markers.xml - verify if file exist
marker_file = project_folder + photos_directory +  "markers.xml"
print("markers = ", marker_file)

# file.txt - verify if file exist
reference_file =  project_folder + photos_directory + "file.csv"
print("reference", reference_file)

def addphotos():
    print("*** Started...Add Photos *** ", datetime.datetime.utcnow())
    chunk.label = project_name + "_chunk"
    chunk.addPhotos(images_pattern)
    if not doc.save( doc_name ):
        print( "ERROR: Failed to save project: " + doc_name)

    if os.path.exists(marker_file) == True:
        print("marker file exist!")
        chunk.importMarkers(marker_file)

    if os.path.exists(reference_file) == True:
        print("reference file exist!")
        chunk.loadReference(reference_file, "csv", delimiter=';')

    PhotoScan.app.update()
    print("*** Finished - Add Photos *** ", datetime.datetime.utcnow())

def alignphotos():
    print("*** Started...Align Photos *** ", datetime.datetime.utcnow())
    coord_system = PhotoScan.CoordinateSystem('EPSG::4326')
    chunk.crs = coord_system
    chunk.matchPhotos(accuracy=PhotoScan.Accuracy.LowestAccuracy, preselection=PhotoScan.Preselection.GenericPreselection, filter_mask=False, keypoint_limit=4000, tiepoint_limit=500)
    chunk.alignCameras()
    chunk.optimizeCameras()
    doc.save(doc_name)
    PhotoScan.app.update()
    print("*** Finished - Align Photos ***")

def buildensecloud():
    print("*** Build Dense Cloud - Started ***", datetime.datetime.utcnow())
    PhotoScan.app.gpu_mask = 1  #GPU devices binary mask
    if not chunk.dense_cloud:
       if not chunk.buildDenseCloud(quality=PhotoScan.Quality.LowestQuality, filter=PhotoScan.FilterMode.AggressiveFiltering):
            print( "ERROR: Could not build dense cloud" )
            return False
       else:
            doc.save(doc_name)
            PhotoScan.app.update()
    else:
        print( "Dense cloud already exists." )

    print("*** Finished - Build Dense Cloud *** ", datetime.datetime.utcnow())

def buildmesh():
    print("*** Build Mesh - Started *** ", datetime.datetime.utcnow())
    if not chunk.model:
        if not     chunk.buildModel(surface=PhotoScan.HeightField, source=PhotoScan.DenseCloudData, face_count=PhotoScan.HighFaceCount, interpolation=PhotoScan.EnabledInterpolation):
            print( "ERROR: Could not build model")
            return False
        else:
            doc.save(doc_name)
    else:
    	print( "Model already exists" )
    PhotoScan.app.update()
    print("*** Build Mesh - Finished *** ", datetime.datetime.utcnow())

def buildtexture():
    print("*** Build Texture - Started *** ", datetime.datetime.utcnow())
    chunk.buildUV(mapping = PhotoScan.GenericMapping, count = 1)
    chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)
    doc.save(doc_name)
    PhotoScan.app.update()
    print("*** Build Texture - Finished *** ", datetime.datetime.utcnow())

# def buildtiledmodel():
#     print("Build Tiled Model - Started")
#     chunk.buildModel(surface = PhotoScan.SurfaceType.Arbitrary, source = PhotoScan.DataSource.DenseCloudData, interpolation = PhotoScan.Interpolation.EnabledInterpolation, face_count = PhotoScan.FaceCount.HighFaceCount)
#     doc.save(doc_name + ".psz")
#     PhotoScan.app.update()
#     print("Build Tiled Model - Finished")

def builddem():
    print("*** Build DEM - Started *** ", datetime.datetime.utcnow())
    chunk.buildPoints()
    chunk.buildDem(source=PhotoScan.DenseCloudData)
    print("*** Build DEM - Finished *** ", datetime.datetime.utcnow())

def buildOrthomosaic():
    print("*** Build OrthoMosaic - Started *** ", datetime.datetime.utcnow())
    chunk.buildOrthomosaic(surface=PhotoScan.DataSource.ModelData,blending=PhotoScan.BlendingMode.MosaicBlending,color_correction=False)
    print("*** Build OrthoMosaic - Finished *** ", datetime.datetime.utcnow())

def exportaorthomosaic():
    print("*** Export OrthoMosaic as TIFF files - Started *** ", datetime.datetime.utcnow())
    chunk.exportOrthomosaic(project_folder + "/Ortho.tif", format="tif")
    print("*** Export OrthoMosaic as TIFF files - Finished *** ", datetime.datetime.utcnow())

def exportdemtiff():
    print("*** Export DEM as TIFF files - Started *** ", datetime.datetime.utcnow())
    chunk.exportDem(project_folder + "/DEM.tif", format="tif") # [, projection ][, region ][, dx ][, dy ][, blockw ][, blockh ], nodata=- (is ok whit licence on windows)
    print("*** Export DEM as TIFF files - Finished *** ", datetime.datetime.utcnow())

def generatereport():
    print("*** Generate Report - Started *** ", datetime.datetime.utcnow())
    chunk.exportReport ( project_folder + project_name + ".pdf" ,  "Relatorio",  "relatorio de geracao do projeto " + project_name)
    print("*** Generate Report - Finished *** ", datetime.datetime.utcnow())

if __name__ == '__main__':
    doc = PhotoScan.app.document
    doc.clear()
    chunk = doc.addChunk()
    doc.save(doc_name)
    addphotos()

    PhotoScan.app.update()

    alignphotos()
    PhotoScan.app.update()

    buildensecloud()
    PhotoScan.app.update()

    buildmesh()
    PhotoScan.app.update()

    buildtexture()
    PhotoScan.app.update()

    doc_name_psx = project_folder + project_name + ".psx"
    doc.save(doc_name_psx)
    chunk = doc.chunk
    builddem()
    PhotoScan.app.update()

    doc_name_psx = project_folder + project_name + ".psx"
    doc.save(doc_name_psx)
    chunk = doc.chunk
    buildOrthomosaic()
    PhotoScan.app.update()

    doc_name_psx = project_folder + project_name + ".psx"
    doc.save(doc_name_psx)
    chunk = doc.chunk
    exportdemtiff()
    PhotoScan.app.update()

    doc_name_psx = project_folder + project_name + ".psx"
    doc.save(doc_name_psx)
    chunk = doc.chunk
    exportaorthomosaic()
    PhotoScan.app.update()

    doc_name_psx = project_folder + project_name + ".psx"
    doc.save(doc_name_psx)
    chunk = doc.chunk
    generatereport()
    PhotoScan.app.update()
