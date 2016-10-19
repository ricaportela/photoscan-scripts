# INIT ENVIRONMENT
import os
import glob
import PhotoScan


print("Build Texture - Started")
doc = PhotoScan.app.document

# build texture
chunk.buildTexture(mapping = PhotoScan.MappingMode.GenericMapping, blending = PhotoScan.BlendingMode.MosaicBlending , color_correction = False, size = 4096, count = 1)

PhotoScan.app.update()

doc.save("baquinho.psz")
print("Script finished")
