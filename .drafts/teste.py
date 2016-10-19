# INIT ENVIRONMENT
# import stuff
import os
import sys
import glob
import PhotoScan


### ALTERAR SOMENTE ESSE 3 PARAMETROS - project_name, project_folder, folder_images###
if platform.system() == "Windows":
   project_name   = 'banquinho'
   project_folder = "C:\\temp\\"
   folder_images  = "photos\\"
else:
   project_name   = 'banquinho'
   project_folder = "/home/ricardo/temp/"
   folder_images  = "photos/"
doc_name       = project_name + ".psz"
images_pattern = project_folder + folder_images + "*.jpg"

doc = PhotoScan.app.document
doc.clear()
chunk = doc.addChunk()

print("*** Started...Add Photos *** ")
chunk.label = project_name + "_chunk"
chunk = doc.chunk
aerialimagefiles = glob.glob(images_pattern)
chunk.addPhotos(aerialimagefiles)
if not doc.save( doc_name ):
    print( "ERROR: Failed to save project: " + doc_name)
else:
    doc_name_psz = project_folder + project_name + ".psz"
    doc.save(doc_name_psz)

PhotoScan.app.update()
print("*** Finished - Add Photos *** ")

chunk.matchPhotos(accuracy=PhotoScan.Accuracy.LowAccuracy, preselection=PhotoScan.Preselection.GenericPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=10000)
chunk.alignCameras()
chunk.optimizeCameras()

PhotoScan.app.gpu_mask = 1  #GPU devices binary mask
PhotoScan.app.cpu_cores_inactive = 2 #CPU cores inactive

chunk.buildDenseCloud(quality=PhotoScan.Quality.LowestQuality, filter=PhotoScan.FilterMode.AggressiveFiltering)
chunk.buildModel(surface=PhotoScan.HeightField, source=PhotoScan.DenseCloudData, face_count=PhotoScan.HighFaceCount, interpolation=PhotoScan.EnabledInterpolation)

doc_name_psx = project_folder + project_name + ".psx"
doc.save(doc_name_psx)

chunk.buildUV(mapping = PhotoScan.GenericMapping, count = 1)

chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)

chunk.buildPoints()
chunk = doc.chunk
chunk.buildDem(source=PhotoScan.DenseCloudData)

chunk.buildOrthomosaic(surface=PhotoScan.DataSource.ModelData,blending=PhotoScan.BlendingMode.MosaicBlending,color_correction=False)

chunk.exportOrthomosaic(project_folder + "/Ortho" + project_name + ".tif", format="tif")

chunk.exportDem(project_folder + "/exportedDEM" + project_name + ".tif", format="tif") # [, projection ][, region ][, dx ][, dy ][, blockw ][, blockh ], nodata=- (is ok whit licence on windows)

chunk.exportReport ( project_folder + project_name + ".pdf" ,  "Relatorio",  "relatorio de geracao do projeto " + project_name)
