import scipy.misc as mc
import numpy as np
import os
import shutil

class mosaicLibFormating:
    #libraryDirectory should be a string
    #desiredResolution should be an int.
    def __init__(self, libraryDirectory, desiredResolution):
        #We ensure libraryDirectory is a string
        self.dir = str(libraryDirectory)
        #We check whether desired resolution is an integer
        if isinstance(desiredResolution, int):
            self.res = desiredResolution
        #If it is not an int, we equate it to none
        else:
            self.res = None

        self.newdir = self.dir + "/" + str(self.res)

        if not os.path.exists(self.newdir):
            os.makedirs(self.newdir)
        #We check whether the desired resolution is not larger
        #than the min relosution of any given photo in the library
        self.checkMinRes()

        self.lib = []

        self.formating()

    #Method for checking what the smallest photo resolution in the library is.
    def checkMinRes(self):
        #We create two variables for height and width of images
        minXRes = self.res
        minYRes = self.res
        #We itterate through the library one photo at a time
        for img in os.listdir(self.dir):
            if img.endswith(".jpg"):
                #We don't want to be reading a photo multiple times, so we create a var to store it
                shutil.move(self.dir + "/" + img, os.getcwd())
                pic = mc.imread(img)
                if pic.shape[0] < minXRes:
                    minXRes = pic.shape[0]
                if pic.shape[1] < minYRes:
                    minYRes = pic.shape[1]
                shutil.move(os.getcwd() + "/" + img, self.dir)
        #If self.res was set to None, we automatically set it to the smallest values
        if self.res == None:
            self.res = min([minXRes, minYRes])
        #Otherwise we check
        if self.res >= min([minXRes, minYRes]):
            self.res = min([minXRes, minYRes])

    #We cut a picture into a square
    def formating(self):
        #Itterate through JPEG pictures in the library
        for img in os.listdir(self.dir):
            if img.endswith(".jpg"):
                shutil.move(self.dir + "/" + img, os.getcwd())
                #We read the picture
                pic = mc.imread(img)
                #We find the shape of the picture
                shape = pic.shape

                #We find the excess pixels on both height and width
                xExcess = shape[0] - self.res
                yExcess = shape[1] - self.res

                #If the excess is an odd number we add one
                if xExcess % 2 == 0:
                    xCrop = xExcess / 2
                    for i in range(int(xCrop)):
                        pic = np.delete(pic, 0, 0)
                        pic = np.delete(pic, (-1), 0)
                elif xExcess % 2 == 1:
                    xExcess -= 1
                    xCrop = xExcess / 2
                    for i in range(int(xCrop)):
                        pic = np.delete(pic, 0, 0)
                        pic = np.delete(pic, (-1), 0)
                    pic = np.delete(pic, 0, 0)

                if yExcess % 2 == 0:
                    yCrop = yExcess / 2
                    for i in range(int(yCrop)):
                        pic = np.delete(pic, 0, 1)
                        pic = np.delete(pic, (-1), 1)
                elif yExcess % 2 == 1:
                    yExcess -= 1
                    yCrop = yExcess / 2
                    for i in range(int(yCrop)):
                        pic = np.delete(pic, 0, 1)
                        pic = np.delete(pic, (-1), 1)
                    pic = np.delete(pic, 0, 1)

                #We calculate the mean colour lavels for the cropped photo
                self.calcMeanColLvl(pic)
                name = str(self.c1mean) + "." + str(self.c2mean) + "." + str(self.c3mean)+".jpg"

                #We save the photo named as the mean RGB values
                mc.imsave(name, pic)
                shutil.move(os.getcwd() + "/" + img, self.dir)
                self.lib.append([self.c1mean, self.c2mean, self.c3mean])

                if not os.path.exists(self.newdir + "/" + name):
                    shutil.move(os.getcwd() + "/" + name, self.newdir)
                else:
                    os.remove(os.getcwd() + "/" + name)

    #We calculate the mean colour levels
    def calcMeanColLvl(self, pic):
        #We read the image
        # pic is just a numpy array
        #We note the shape of the pic array
        dim = pic.shape
        #We create a matrix (an array) to store the red levels
        colour1 = np.zeros((dim[0], dim[1]))
        #We extract the red levels out of the coloured image by iterating through every pixels
        for i in range(dim[0]):
            for j in range(dim[1]):
                colour1[i][j] = pic[i][j][0]
        # sm.imsave('colour1' + self.name, self.colour1)
        #We calculated the mean of the red level.
        self.c1mean = int(round(colour1.mean(), 0))

        #We apply same procedure for Green and Blue
        colour2 = np.zeros((dim[0], dim[1]))
        for i in range(dim[0]):
            for j in range(dim[1]):
                colour2[i][j] = pic[i][j][1]
        # sm.imsave('colour2' + self.name, self.colour2)
        self.c2mean = int(round(colour2.mean(), 0))

        colour3 = np.zeros((dim[0], dim[1]))
        for i in range(dim[0]):
            for j in range(dim[1]):
                colour3[i][j] = pic[i][j][2]
        # sm.imsave('colour3' + self.name, self.colour3)
        self.c3mean = int(round(colour3.mean(), 0))

#stuff = mosaicLibFormating("/home/ju5t1nas/Desktop/Playing with Python/Mosaic/Library", 800)

class mosaic(mosaicLibFormating):
    def __init__(self, mosaicPic, libraryDirectory, desiredTileResolution = None, tilesize = 1):

        #We note the name so we can quickly access it later
        self.name = str(mosaicPic)

        #We read the image
        self.pic = mc.imread(self.name)

        #We find the shape of the pic array
        self.dim = self.pic.shape

        #Tilesize for later
        self.tile = tilesize

        #We crop our image so that tiles fit perfectly
        print("Starting to prepare the image")
        self.prepareImage()
        print("Done preparing the Image")

        print("...")

        #We find Number of tiles tiles in rows and columns
        self.xTiles = self.pic.shape[0]/self.tile
        self.yTiles = self.pic.shape[1]/self.tile

        #We initalise the formating of the tile image library
        print("Starting to format the Image Library")
        mosaicLibFormating.__init__(self, libraryDirectory, desiredTileResolution)
        print("Done formating the Image Library")

        print("...")

        #We create a matrix of mean colour values of each matrix
        print("Starting to calculate Tile Mean Colour Value Matrix")
        self.tileMeanMatrix()
        print("Done calculating Tile Mean Colour Value Matrix")

        print("...")

        #print(self.lib)
        #print(self.tileMeanMat[0][0])
        #print(self.findBestKey(self.tileMeanMat[0][0]))

        self.tileBestMatix()

        print("Starting to Stitch the hard way")
        self.stitchingOne()
        print("Done Stitching")

    def prepareImage(self):

        xExcess = self.dim[0] % self.tile
        yExcess = self.dim[1] % self.tile

        # If the excess is an odd number we add one
        if xExcess % 2 == 0:
            xCrop = xExcess / 2
            for i in range(int(xCrop)):
                self.pic = np.delete(self.pic, 0, 0)
                self.pic = np.delete(self.pic, (-1), 0)
        elif xExcess % 2 == 1:
            xExcess -= 1
            xCrop = xExcess / 2
            for i in range(int(xCrop)):
                self.pic = np.delete(self.pic, 0, 0)
                self.pic = np.delete(self.pic, (-1), 0)
            self.pic = np.delete(self.pic, 0, 0)

        if yExcess % 2 == 0:
            yCrop = yExcess / 2
            for i in range(int(yCrop)):
                self.pic = np.delete(self.pic, 0, 1)
                self.pic = np.delete(self.pic, (-1), 1)
        elif yExcess % 2 == 1:
            yExcess -= 1
            yCrop = yExcess / 2
            for i in range(int(yCrop)):
                self.pic = np.delete(self.pic, 0, 1)
                self.pic = np.delete(self.pic, (-1), 1)
            self.pic = np.delete(self.pic, 0, 1)

    def split(self, pos):
        self.splinter = np.zeros((self.tile, self.tile, 3))

        for i in range(pos[0]*self.tile, (pos[0]+1)*self.tile):
            for j in range(pos[1]*self.tile, (pos[1]+1)*self.tile):
                self.splinter[i - pos[0]*self.tile][j - pos[1]*self.tile] = self.pic[i][j]

    def tileMeanMatrix(self):
        self.tileMeanMat = np.zeros((int(self.xTiles), int(self.yTiles), 3))

        for i in range(int(self.xTiles)):
            for j in range(int(self.yTiles)):
                self.split([i,j])
                mosaicLibFormating.calcMeanColLvl(self, self.splinter)

                self.tileMeanMat[i][j][0] = self.c1mean
                self.tileMeanMat[i][j][1] = self.c2mean
                self.tileMeanMat[i][j][2] = self.c3mean

    def keyToRGB(self, key):
        word = ""
        list = []
        for i in range(len(key)):
            if key[i] == ".":
                list.append(int(word))
                word = ""
            else:
                word = word + key[i]
        list.append(int(word))
        return list

    def RGBToKey(self, RGB):
        word = ""
        for i in range(len(RGB)):
            word = word + str(RGB[i])
            if i != 2:
                word = word + "."
        return word

    def distanceFromKey(self, key, RGB):
        distance = ((key[0]-RGB[0])**2 + (key[1]-RGB[1])**2 + (key[2]-RGB[2])**2)**(1/2)
        return distance

    def findBestKeyIndex(self, RGB):
        listOfDistances = []
        for key in self.lib:
            listOfDistances.append(self.distanceFromKey(key, RGB))
        minDistance = min(listOfDistances)
        index = listOfDistances.index(minDistance)
        return index

    def tileBestMatix(self):
        self.bestFitMatrix = np.zeros((int(self.xTiles), int(self.yTiles)))

        for i in range(int(self.xTiles)):
            for j in range(int(self.yTiles)):
                self.bestFitMatrix[i][j] = self.findBestKeyIndex(self.tileMeanMat[i][j])

    def stitchingOne(self):
        endpic = np.zeros((self.xTiles*self.res, self.yTiles*self.res, 3))
        for i in range(int(self.xTiles)):
            for j in range(int(self.yTiles)):
                tileRGB = self.lib[int(self.bestFitMatrix[i][j])]
                print(tileRGB)
                tilenName = self.RGBToKey(tileRGB)
                tiledir = self.newdir + "/" + tilenName + ".jpg"
                shutil.move(tiledir, os.getcwd())
                tile = mc.imread(tilenName + ".jpg")
                for k in range(self.res):
                    for m in range(self.res):
                        endpic[i*self.res + k][j*self.res + m] = tile[k][m]
                shutil.move(os.getcwd() + "/" + tilenName + ".jpg", self.newdir)
        mc.imsave("mosaic.jpg", endpic)











pic = mosaic("August.jpg", "/home/ju5t1nas/Desktop/Playing with Python/Mosaic/iDubbz2", 100, 1)
#pic.split([0,0])
#print(pic.splinter.shape)
#print(pic.TileMeanMat)