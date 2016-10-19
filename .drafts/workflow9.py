import PhotoScan
doc = PhotoScan.app.document
doc.open("testes.psz")
chunk = doc.chunk
chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.GenericPreselection)
chunk.alignCameras()
chunk.buildDenseCloud(quality=PhotoScan.MediumQuality)
chunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation)
chunk.buildUV(mapping=PhotoScan.GenericMapping)
chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)
doc.save()
