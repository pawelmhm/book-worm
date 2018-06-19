from tesserocr import PyTessBaseAPI

images = ['9784219.jpg']

with PyTessBaseAPI() as api:
    for img in images:
        api.SetImageFile(img)
        print api.GetUTF8Text()
        print api.AllWordConfidences()