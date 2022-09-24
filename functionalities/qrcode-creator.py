import qrcode
from PIL import Image, ImageDraw


# with function
def makeQrCode(website):
    return qrcode.make(website).save('qrcode.png')


makeQrCode(input('Type url of your qrcode: '))


# with class
class Qrcode:
    def __init__(self, url, namefile):
        self.__url = url
        self.__namefile = namefile

    def makeQrCode(self):
        return qrcode.make(self.__url).save(self.__namefile)


newQr = Qrcode('www.facebook.com', 'facebook.png')
newQr.makeQrCode()
