# INIT ENVIRONMENT
# import stuff
import os
import sys
import json
import datetime
import platform
import PhotoScan


def loadjson():
    try:
        with open(os.path.join(PROJECT_DIR, 'config.json'), 'r') as f:
            config = json.load(f)
    except Exception:
        print("Error Json Invalid")
        PhotoScan.app.messageBox("Error Json Invalid, Please Correct Json File")

    else:
        print("Json Load!")
        print("*************************************")
        print(config["project_name"])
        print(config["project_folder"])
        print(config["photos_directory"])
        print(config["accuracy"])
        print("*************************************")

def addphotos():
    print("*** Started...Add Photos *** ", datetime.datetime.utcnow())
    photos_dir         = os.path.join( project_folder, photos_directory )
    photos             = os.listdir(photos_dir)
    photos             = [os.path.join(photos_dir,p) for p in photos]
    chunk.addPhotos(photos)

    if not doc.save():
        print( "ERROR: Failed to save project: " + project_name )

    print("*** Finished - Add Photos *** ", datetime.datetime.utcnow())

def alignphotos():
    print("*** Started...Align Photos *** ", datetime.datetime.utcnow())
    coord_system = PhotoScan.CoordinateSystem('EPSG::4326')
    chunk.crs = coord_system
    #chunk.matchPhotos(accuracy=config['accuracy'], preselection=PhotoScan.Preselection.GenericPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=10000)
    chunk.matchPhotos(accuracy=PhotoScan.Accuracy.LowestAccuracy, preselection=PhotoScan.Preselection.GenericPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=10000)
    chunk.alignCameras()
    if os.path.exists(marker_file) == True:
        print("marker file exist!")
        chunk.importMarkers(marker_file)

    if os.path.exists(reference_file) == True:
        print("reference file exist!")
        chunk.loadReference(reference_file, "csv", delimiter=';')

    chunk.optimizeCameras()

    for camera in chunk.cameras:
        camera.reference.enabled = False
    chunk.updateTransform()
    print("*** Finished - Align Photos ***")

def buildensecloud():
    print("*** Build Dense Cloud - Started ***", datetime.datetime.utcnow())
    PhotoScan.app.gpu_mask = 1  #GPU devices binary mask
    if not chunk.dense_cloud:
       if not chunk.buildDenseCloud(quality=PhotoScan.Quality.LowestQuality, filter=PhotoScan.FilterMode.AggressiveFiltering):
            print( "ERROR: Could not build dense cloud" )
            return False
       else:
            doc.save()
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
            doc.save()
    else:
    	print( "Model already exists" )

    print("*** Build Mesh - Finished *** ", datetime.datetime.utcnow())

def buildtexture():
    print("*** Build Texture - Started *** ", datetime.datetime.utcnow())
    chunk.buildUV(mapping = PhotoScan.GenericMapping, count = 1)
    chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)
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
    chunk.exportOrthomosaic(project_folder + "Export/" + project_name + "_Ortho.tif", format="tif")
    print("*** Export OrthoMosaic as TIFF files - Finished *** ", datetime.datetime.utcnow())

def exportdemtiff():
    print("*** Export DEM as TIFF files - Started *** ", datetime.datetime.utcnow())
    chunk.exportDem(project_folder + "Export/" + project_name + "_DEM.tif", format="tif") # [, projection ][, region ][, dx ][, dy ][, blockw ][, blockh ], nodata=- (is ok whit licence on windows)
    print("*** Export DEM as TIFF files - Finished *** ", datetime.datetime.utcnow())

def generatereport():
    print("*** Generate Report - Started *** ", datetime.datetime.utcnow())
    chunk.exportReport ( project_folder + project_name + ".pdf" ,  "Relatorio",  "relatorio de geracao do projeto " + project_name)
    print("*** Generate Report - Finished *** ", datetime.datetime.utcnow())

def are_cameras_aligned(chunk):
    'Assume cameras are aligned if at least one of them have been moved.'
    return len([c for c in chunk.cameras if c.center is not None]) > 0

def main():
    ###  project_name, project_folder, photos_directory###
    project_name     = config["project_name"]
    project_folder   = os.path.join(config["project_folder"])
    photos_directory  = config["photos_directory"]

    # markers.xml - verify if file exist
    marker_file = project_folder + photos_directory +  "markers.xml"
    print("markers = ", marker_file)

    # file.txt - verify if file exist
    reference_file =  project_folder + photos_directory + "file.csv"
    print("reference", reference_file)

    doc = PhotoScan.app.document
    doc.clear()
    chunk = doc.addChunk()
    chunk.label = project_name + "_chunk"
    print(project_folder + project_name + ".psx")
    doc.save(project_folder + project_name + ".psx")

    chunk = doc.chunk

    if not chunk:
        print("ERROR: Chunk is None")

    addphotos()
    if not chunk.enabled:
        print("Chunk not enabled, skipping")

if __name__ == '__main__':

    PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

    # If an Exception error occurs with Json the PhotoScan will terminated
    loadjson()

    main()

    alignphotos()

    buildensecloud()

    buildmesh()

    buildtexture()

    #doc.save(project_folder + project_name + ".psx")

    builddem()

    buildOrthomosaic()

    exportdemtiff()

    exportaorthomosaic()

    generatereport()

    PhotoScan.app.update()

    #    app.quit()

    print("Finished building chunk")
