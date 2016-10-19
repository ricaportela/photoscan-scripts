import PhotoScan
import glob

images = glob.glob('/home/ricardo/temp/photos/*.jpg')
ouput_path = '/home/ricardo/temp/'

app = PhotoScan.Application()
doc = PhotoScan.Document()
chunk = doc.addChunk()
chunk.label = "banquinho"
chunk.addPhotos(images)

# with open(images, mode='w') as fd:
#     chunk.estimateImageQuality()
#     n = len(chunk.cameras)
#     for i, image in enumerate(images):
#         quality = chunk.cameras[i].frames[0].meta["Image/Quality"]
#         fd.write('{image} {quality}\n'.format(image=image.split('/')[-1], quality=quality))

chunk.loadReferenceExif()
coord_system = PhotoScan.CoordinateSystem('EPSG::4326')
chunk.crs = coord_system
accuracy = PhotoScan.HighAccuracy
chunk.matchPhotos(accuracy=accuracy, preselection=PhotoScan.ReferencePreselection)
chunk.alignCameras()

# transform bounding box to deisred mapping region
reg = chunk.region
trans = chunk.transform.matrix
newregion = PhotoScan.Region()

# Set region center:
center_geo = PhotoScan.Vector([bbox_center[0], bbox_center[1], 0.])  # uses existing region height
v_temp = chunk.crs.unproject(center_geo)
v_temp.size = 4
v_temp.w = 1
centerLocal = chunk.transform.matrix.inv() * v_temp
centerLocal.size = 3
newregion.center = PhotoScan.Vector([centerLocal[0], centerLocal[1], reg.center[2]])  # uses existing region height

# Set region size:
# generate scale factor
rot_untransformed = PhotoScan.Matrix().diag([1, 1, 1, 1])
rot_temp = trans * rot_untransformed
s = math.sqrt(rot_temp[0, 0] ** 2 + rot_temp[0, 1] ** 2 + rot_temp[0, 2] ** 2)

# scale desired size in metres to chunk internal coordinate system
inter_size = PhotoScan.Vector([0, 0, 0])
geo_size = PhotoScan.Vector([bbox_size[0], bbox_size[1], 0])  # uses original chunk region z size
inter_size = geo_size / s
newregion.size = PhotoScan.Vector([inter_size[0], inter_size[1], reg.size[2]])

#  rotate region bounding box
SinRotZ = math.sin(math.radians(bbox_rot))
CosRotZ = math.cos(math.radians(bbox_rot))
RotMat = PhotoScan.Matrix([[CosRotZ, -SinRotZ, 0, 0], [SinRotZ, CosRotZ, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
v = PhotoScan.Vector([0, 0, 0, 1])
v_t = trans * v
v_t.size = 3
m = chunk.crs.localframe(v_t)
m = m * trans
m = RotMat*m
s = math.sqrt(m[0, 0]**2 + m[0, 1]**2 + m[0, 2]**2)  # scale factor
R = PhotoScan.Matrix([[m[0, 0], m[0, 1], m[0, 2]], [m[1, 0], m[1, 1], m[1, 2]], [m[2, 0], m[2, 1], m[2, 2]]])
R = R * (1. / s)
newregion.rot = R.t()
chunk.region = newregion

chunk.buildPoints(error=1)
chunk.optimizeCameras()
chunk.saveReference(gc_path, "csv")
chunk.buildDenseCloud(quality=PhotoScan.HighQuality, filter=PhotoScan.MildFiltering)  # mild filter as default to improve trees / buildings
chunk.buildModel(surface=PhotoScan.HeightField, source=PhotoScan.DensePoints, face_count=PhotoScan.HighFaceCount)
chunk.model.closeHoles()
chunk.model.fixTopology()
chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)
chunk.exportReport(report_path)
chunk.exportOrthophoto(orthophoto_path, blockw=blockw, blockh=blockh, color_correction=False, blending=PhotoScan.MosaicBlending, write_kml=True, write_world=True, projection=chunk.crs)
chunk.exportDem(dem_path, dx=required_dx, dy=required_dy, blockw=blockw, blockh=blockh, write_kml=True, write_world=True, projection=chunk.crs)
open(complete_file, mode='w').write('saving project')
doc.save(project_path)
coord_system = PhotoScan.CoordinateSystem('LOCAL_CS["Local CS",LOCAL_DATUM["Local Datum",0],UNIT["metre",1]]')
chunk.exportPoints(points_path, source=PhotoScan.DensePoints, format='las', projection=coord_system)
chunk.decimateModel(2000000)  # TODO: check what size model comes out as (200MB limit from sketchfab atm)
chunk.buildTexture(blending=PhotoScan.MosaicBlending)
chunk.exportModel(model_path, texture_format='tif', format='obj', projection=coord_system)

app = PhotoScan.Application()
app.quit()
