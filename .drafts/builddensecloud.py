# INIT ENVIRONMENT
import os
import glob
import PhotoScan


print("Build Dense Cloud - Started")
doc = PhotoScan.app.document

# Build Dense Cloud
chunk.buildDenseCloud(quality=PhotoScan.Quality.MediumQuality, filter=PhotoScan.FilterMode.AggressiveFiltering)
PhotoScan.app.update()

doc.save("baquinho.psz")
print("Script finished")
