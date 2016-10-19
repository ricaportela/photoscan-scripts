# INIT ENVIRONMENT
# import stuff
import os
import sys
import glob
import PhotoScan

### ALTERAR SOMENTE ESSE 3 PARAMETROS - project_name, project_folder, folder_images###
project_name   = 'nomedoprojeto'
project_folder = "C:\\arquivos_projeto\\"
folder_images  = "imagens\\"
### ALTERAR SOMENTE ESSE 3 PARAMETROS ###
doc_name       = project_folder + project_name
images_pattern = project_folder + folder_images + "*.jpg"

def addphotos():
    print("*** Started...Add Photos *** ")
    chunk.label = project_name
    aerialimagefiles = glob.glob(images_pattern)
    if (chunk.addPhotos(aerialimagefiles)):
       chunk.addPhotos(aerialimagefiles)
       if not doc.save( doc_name ):
           print( "ERROR: Failed to save project: " + doc_name)
    PhotoScan.app.update()
    print("*** Finished - Add Photos *** ")

def alignphotos():
    print("*** Started...Align Photos *** ")
    if not are_cameras_aligned(chunk):
        chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.GenericPreselection)
        if not chunk.alignCameras():
            print( "ERROR: Could not align cameras" )
            return False
        else:
            doc.save(doc_name)
    else:
        print( "Cameras are already aligned.")
    PhotoScan.app.update()
    print("*** Finished - Align Photos ***")

def buildensecloud():
    print("*** Build Dense Cloud - Started")
    if not chunk.dense_cloud:
       chunk.buildDenseCloud(quality=PhotoScan.LowQuality, filter=PhotoScan.AggressiveFiltering)
       doc.save(doc_name)
    else:
        print( "Dense cloud already exists." )

    print("*** Finished - Build Dense Cloud ***")

def buildmesh():
    print("*** Build Mesh - Started ***")
    if not chunk.model:
        if not chunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation):
            print( "ERROR: Could not build model")
            return False
        else:
            print("construindo buildmesh")
            doc.save(doc_name)
    else:
    	print( "Model already exists" )
    print("*** Build Mesh - Finished ***")

def buildtexture():
    print("*** Build Texture - Started ***")
    if not chunk.model and not chunk.model.texture:
        if not chunk.buildTexture():
            print( "ERROR: Could not build texture")
            return False
        else:
            chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)
            doc.save(doc_name)
    else:
        print( "Texture already exists" )

    print("*** Build Texture - Finished ***")

# def buildtiledmodel():
#     print("Build Tiled Model - Started")
#     chunk.buildModel(surface = PhotoScan.SurfaceType.Arbitrary, source = PhotoScan.DataSource.DenseCloudData, interpolation = PhotoScan.Interpolation.EnabledInterpolation, face_count = PhotoScan.FaceCount.HighFaceCount)
#     doc.save(doc_name + ".psz")
#     PhotoScan.app.update()
#     print("Build Tiled Model - Finished")

def builddem():
    print("*** Build DEM - Started ***")
    doc.save(doc_name + ".psx")
    chunk.buildDem(source=PhotoScan.DenseCloudData)
    # interpolation = enabled(default)
    PhotoScan.app.update()
    print("*** Build DEM - Finished ***")

def buildOrthomosaic():
    print("*** Build OrthoMosaic - Started ***")
    # salvar o projeto como PSX
    doc.save(doc_name + ".psx")
    # chunk.buildOrthomosaic()
    print("*** Build OrthoMosaic - Finished ***")

def exportaorthomaisc():
    print("*** Export OrthoMosaic as TIFF files - Started ***")
    # save project as PSX
    doc.save(doc_name + ".psx")
    # chunk.buildOrthomosaic()
    print("*** Export OrthoMosaic as TIFF files - Finished ***")
    # EXPORT ORTHOIMAGE(S)
    print("---Exporting Orthoimage(s)...")


def exportdemtiff():
    print("*** Export DEM as TIFF files - Started ***")
    doc.save(doc_name + ".psx")
    # chunk.buildOrthomosaic()
    print("*** Export DEM as TIFF files - Finished ***")

def generatereport():
    print("*** Generate Report - Started ***")
    # save project as PSX
    doc.save(doc_name + ".psx")
    # Title
    # Description
    # Projection
    print("*** Generate Report - Finished ***")

def are_cameras_aligned(chunk):
	return len([c for c in chunk.cameras if c.center is not None]) == len(chunk.cameras)


if __name__ == '__main__':
    doc = PhotoScan.app.document
    doc.clear()
    chunk = doc.addChunk()
    doc_name = doc_name + ".psz"
    print("definido o nome do projeto = ", doc_name)
    if not doc.open(doc_name):
       doc.save(doc_name)
       print ("criou o arquivo")
    else:
       print ("Abriu o projeto")

    # addphotos()
    # alignphotos()
    buildensecloud()
    # buildmesh()
    # buildtexture()
    # buildtiledmodel()
    # builddem()
    # buildOrthomosaic()
    # exportaorthomaisc()
    # exportdemtiff()
    # generatereport()
