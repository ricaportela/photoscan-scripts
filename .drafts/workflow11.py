import PhotoScan
import glob

images = glob.glob('c:\\temp\\photos\\*.jpg')
ouput_path = 'c:\\temp\\'

project_name   = 'banquinho'


app = PhotoScan.Application()
doc = PhotoScan.Document()
chunk = doc.addChunk()

chunk.addPhotos(images)
chunk.loadReferenceExif()

coord_system = PhotoScan.CoordinateSystem('EPSG::4326')
chunk.crs = coord_system

chunk.matchPhotos(accuracy=PhotoScan.LowAccuracy, preselection=PhotoScan.ReferencePreselection, tiepoint_limit=10000)
chunk.alignCameras()

chunk.optimizeCameras()

chunk.buildDenseCloud(quality=PhotoScan.LowQuality, filter=PhotoScan.AggressiveFiltering)

chunk.buildModel(surface=PhotoScan.HeightField, source=PhotoScan.DenseCloudData, face_count=PhotoScan.HighFaceCount, interpolation=PhotoScan.EnabledInterpolation)

chunk.model.closeHoles()
chunk.model.fixTopology()

chunk.buildUV(mapping=PhotoScan.GenericMapping, count=4)
chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)

doc.save(path=ouput_path + project_name + '.psx', chunks=[chunk])

doc = PhotoScan.Document()
doc.open(ouput_path + project_name + '.psx')
chunk = doc.chunk

chunk.buildOrthomosaic()
chunk.buildDem(source=PhotoScan.DenseCloudData)

chunk.exportOrthomosaic(ouput_path + 'ortho.tif')

chunk.exportDem(ouput_path + 'dem.tif')

# chunk.exportPoints(ouput_path + 'points.las', source=PhotoScan.DenseCloudData, format='las')

chunk.exportModel(ouput_path + 'model.obj', texture_format='jpg', texture=True, format='obj')

app.quit()
