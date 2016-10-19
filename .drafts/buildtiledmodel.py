
# INIT ENVIRONMENT
import os
import glob
import PhotoScan


print("Build Tiled Model - Started")
doc = PhotoScan.app.document

# build Tiled Model
chunk.buildModel(surface = PhotoScan.SurfaceType.Arbitrary, source = PhotoScan.DataSource.DenseCloudData, interpolation = PhotoScan.Interpolation.EnabledInterpolation, face_count = PhotoScan.FaceCount.HighFaceCount)
PhotoScan.app.update()

doc.save("baquinho.psz")
print("Script finished")
