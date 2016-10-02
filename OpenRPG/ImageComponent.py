from Component import Component

class ImageComponent(Component):
    def __init__(self, orginX, originY, imageURL):
        self._originX = originX
        self._originY = originY
        self._imageURL = imageURL

    def getCode(self):
        pass