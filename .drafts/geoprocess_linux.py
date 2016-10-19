# INIT ENVIRONMENT
# import stuff
import os
import sys
import glob
import PhotoScan

project_name   = "banquinho"
chunck_name    = project_name
project_folder = "/home/ricardo/LearnPath/python/geoprocess-photoscan-cobolman/"
folder_images  = "source_images/"
doc_folder     = project_folder + project_name + "/"
images_pattern = project_folder + project_name + "/" + folder_images + "*.jpg"

# Define: DSMResolutions (in meters),
# 0 == GSD resolution
DSMResolutions = [1.00, 0]

# Define: OrthoImageResolutions (in meters)
# 0 == GSD resolution

OrthoImageResolutions = [1.00, 0]
def addphotos():
    print("*** Started...Add Photos *** ")
    chunk.label = chunck_name
    aerialimagefiles = glob.glob(images_pattern)
    chunk.addPhotos(aerialimagefiles)
    doc.save(doc_folder + project_name + ".psz")
    PhotoScan.app.update()
    print("*** Finished - Add Photos *** ")

def alignphotos():
    print("*** Started...Align Photos *** ")
    chunk.matchPhotos(accuracy=PhotoScan.Accuracy.HighAccuracy, preselection=PhotoScan.Preselection.GenericPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=10000)
    chunk.alignCameras()
    chunk.optimizeCameras()
    doc.save(doc_folder + project_name + ".psz")
    PhotoScan.app.update()
    print("*** Finished - Align Photos ***")

def buildensecloud():
    print("*** Build Dense Cloud - Started")
    chunk.buildDenseCloud(quality=PhotoScan.Quality.MediumQuality, filter=PhotoScan.FilterMode.AggressiveFiltering)
    doc.save(doc_folder + project_name + ".psz")
    PhotoScan.app.update()
    print("*** Finished - Build Dense Cloud ***")

def buildmesh():
    print("*** Build Mesh - Started ***")
    chunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation, face_count=PhotoScan.HighFaceCount)
    doc.save(doc_folder + project_name + ".psz")
    PhotoScan.app.update()
    print("*** Build Mesh - Finished ***")

def buildtexture():
    print("*** Build Texture - Started ***")
    chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)
    doc.save(doc_folder + project_name + ".psz")
    PhotoScan.app.update()
    print("*** Build Texture - Finished ***")

# def buildtiledmodel():
#     print("Build Tiled Model - Started")
#     chunk.buildModel(surface = PhotoScan.SurfaceType.Arbitrary, source = PhotoScan.DataSource.DenseCloudData, interpolation = PhotoScan.Interpolation.EnabledInterpolation, face_count = PhotoScan.FaceCount.HighFaceCount)
#     doc.save("/home/ricardo/baquinho.psz")
#     PhotoScan.app.update()
#     print("Build Tiled Model - Finished")

def builddem():
    print("*** Build DEM - Started ***")
    doc.save(doc_folder + project_name + ".psx")
    chunk.buildDem(source=PhotoScan.DenseCloudData)
    # interpolation = enabled(default)
    PhotoScan.app.update()
    print("*** Build DEM - Finished ***")

def buildOrthomosaic():
    print("*** Build OrthoMosaic - Started ***")
    # salvar o projeto como PSX
    doc.save(doc_folder + project_name + ".psx")
    # chunk.buildOrthomosaic()
    print("*** Build OrthoMosaic - Finished ***")

def exportaorthomaisc():
    print("*** Export OrthoMosaic as TIFF files - Started ***")
    # save project as PSX
    doc.save(doc_folder + project_name + ".psx")
    # EXPORT ORTHOIMAGE(S)
    print("---Exporting Orthoimage(s)...")
    for Resolution in OrthoImageResolutions:
       if Resolution == 0:
          Resolution = GroundSamplingDistance

       FileName = ".\\OrthoImage_PixelSize=" + str(Resolution) + "m.tif"
       print("File: " + FileName)
       if not(chunk.exportOrthophoto(FileName, format="tif", projection=chunk.projection, blending="mosaic", dx=Resolution, dy=Resolution)):
          app.messageBox("Exporting orthoimage failed: " + FileName)
    print("*** Export OrthoMosaic as TIFF files - Finished ***")

def exportdemtiff():
    print("*** Export DEM as TIFF files - Started ***")
    doc.save(doc_folder + project_name + ".psx")
    # EXPORT DSM(S)
    # print("---Exporting Digital Surface Model(s)...")
    # for Resolution in DSMResolutions:
    #    if Resolution == 0:
    #       Resolution = GroundSamplingDistance
    #
    #    FileName = ".\\DSM_PixelSize=" + str(Resolution) + "m.tif"
    #    print("File: " + FileName)
    #    if not(chunk.exportDem(FileName, format="tif", dx=Resolution, dy=Resolution, projection=chunk.projection)):
    #       app.messageBox("Exporting DSM failed: " + FileName)
    print("*** Export DEM as TIFF files - Finished ***")

def generatereport():
    print("*** Generate Report - Started ***")
    # save project as PSX
    doc.save(doc_folder + project_name + ".psx")
    # Title
    # Description
    # Projection
    print("*** Generate Report - Finished ***")

if __name__ == '__main__':
    doc = PhotoScan.app.document
    doc.clear()
    chunk = doc.addChunk()
    addphotos()
    alignphotos()
    # buildensecloud()
    # buildmesh()
    # buildtexture()
    # builddem()
    # buildOrthomosaic()
    # exportaorthomaisc()
    # exportdemtiff()
    # generatereport()
