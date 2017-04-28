import scipy.misc as sm
import numpy as nm
import os
import shutil

#Lets make a class called image.
#Here we will put everything that works.

class image:
    def __init__(self, imageName):
        #create a quick way to get the name of the image
        self.name = str(imageName)

        #We read the picture using imread
        self.pic = sm.imread(self.name)
        # We create a new matrix of the compressed image and initially set it equal to original
        self.compressed = self.pic

        #So we don't have to call sm.shape a bunch, I make a quick self.dim
        self.evenShape()

        #We separate the colours.
        #And we make create c1, c2 and c3 as we will be updating them later.
        #We can not do that with self.colour1, 2  or 3.
        self.separatingColour()
        self.c1 = self.colour1
        self.c2 = self.colour2
        self.c3 = self.colour3

    #I have not tested it for coloured photos, but I am pretty sure it should not work
    def evenShape(self):
        self.dim = self.compressed.shape
        #We make a variable to mark whether shape of the image is even.
        #What I mean is whether the amount of rows and columns are both even.
        even = False

        #We check whether both num of rows and col. is even
        if self.dim[0] % 2 == 0 and self.dim[1] % 2 == 0:
            even = True
        #If not, we reshape the picture.
        if even == False:
            #We now need to delete either a row or column
            #Preferable we delete last row or column

            #Check whether number of rows is even
            if self.dim[0] % 2 != 0:
                #We delete the last row and replace the old image with the new one.
                self. pic = nm.delete(self.pic, self.dim[0]-1, 0)
            #Check whether number of columns is even
            elif self.dim[1] % 2 != 0:
                #We delete the last colum and replace the opd image with the new one.
                self.pic = nm.delete(self.pic, self.dim[1]-1, 1)

        #One last sanity check whether the image is evenly shaped
        if self.dim[0] % 2 == 0 and self.dim[1] % 2 == 0:
            return True

    #This produces the matrices for mean compression
    #You can choose whether you want a matrix for compression with preservation of data for reversal or not
    def meanMat(self, revertible):
        self.dim = self.c1.shape
        #We check whether 'revertable' is bool type
        if not isinstance(revertible, bool):
            #We will raise exception later
            revertible = True
        #I will name the matrices Mr and Mc.
        #They stand for Martix for Rows and Matrix for Columns.
        #If we want a revertable matric we create a larger matrix.
        if revertible == True:
            #We create a matrix of all zeroes
            self.Mr = nm.zeros((self.dim[0], self.dim[0]))
        #If we do not want revertable, we create a smaller matrix
        elif revertible == False:
            #We create a matrix of all zeroes
            self.Mr = nm.zeros((int(self.dim[0] / 2), self.dim[0]))

        # We start replacing some entries in the matrix with what is supposed to be there.
        for i in range(int(self.dim[0] / 2)):
            self.Mr[i][i * 2] = 1 / 2
            self.Mr[i][i * 2 + 1] = 1 / 2
            #If we have a larger matrix, we add elements needed for reversal
            if revertible == True:
                self.Mr[i + int(self.dim[0] / 2)][i * 2] = -1 / 2
                self.Mr[i + int(self.dim[0] / 2)][i * 2 + 1] = 1 / 2

        #Same logic as before.
        if revertible == True:
            self.Mc = nm.zeros((self.dim[1], self.dim[1]))
        elif revertible == False:
            self.Mc = nm.zeros((int(self.dim[1] / 2), self.dim[1]))
        # We start replacing some entries in the matrix with what is supposed to be there.
        for i in range(int(self.dim[1] / 2)):
            self.Mc[i][i * 2] = 1 / 2
            self.Mc[i][i * 2 + 1] = 1 / 2
            if revertible == True:
                self.Mc[i + int(self.dim[1] / 2)][i * 2] = -1 / 2
                self.Mc[i + int(self.dim[1] / 2)][i * 2 + 1] = 1 / 2

    #Finally, the mathod for compression.
    def compressionOfColour(self, revertible, times):
        #We check whether 'revertible' is bool type
        if not isinstance(revertible, bool):
            #We set revertible to true
            revertible = True
        #We check whether the number of times to run compression is an int.
        if not isinstance(times, int):
            times = 1
        #We compress for the amount of times we want
        for i in range(times):
            # We call the meanMat method so that each time the compression matrices are the correct size.
            self.meanMat(revertible)
            #We compress through matrix multiplication
            self.c1 = nm.dot(nm.dot(self.Mr, self.c1), self.Mc.transpose())
            self.c2 = nm.dot(nm.dot(self.Mr, self.c2), self.Mc.transpose())
            self.c3 = nm.dot(nm.dot(self.Mr, self.c3), self.Mc.transpose())
        #We save a new compressed image
        #sm.imsave('compressedcolour1' + self.name, self.c1)
        #sm.imsave('compressedcolour2' + self.name, self.c2)
        #sm.imsave('compressedcolour3' + self.name, self.c3)

    def separatingColour(self):
        self.dim = self.pic.shape
        self.colour1 = nm.zeros((self.dim[0], self.dim[1]))
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                self.colour1[i][j] = self.pic[i][j][0]
        #sm.imsave('colour1' + self.name, self.colour1)
        self.colour2 = nm.zeros((self.dim[0], self.dim[1]))
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                self.colour2[i][j] = self.pic[i][j][1]
        #sm.imsave('colour2' + self.name, self.colour2)
        self.colour3 = nm.zeros((self.dim[0], self.dim[1]))
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                self.colour3[i][j] = self.pic[i][j][2]
        #sm.imsave('colour3' + self.name, self.colour3)

    def compression(self, revertible, times):
        self.compressionOfColour(revertible, times)
        self.dim = self.c1.shape
        compressed = nm.zeros((self.dim[0], self.dim[1], 3))
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                compressed[i][j][0] = self.c1[i][j]
                compressed[i][j][1] = self.c2[i][j]
                compressed[i][j][2] = self.c3[i][j]
        sm.imsave(self.name, compressed)



print("Starting Compression")
#picture = image("August.jpg")
#print(picture.pic.shape)
#print(picture.dim)
#picture.meanMat(False)
#print(picture.Mc.shape)
#picture.compression(False, 1)
#print(picture.colour1)
#picture.compression(False, 1)

dir = os.getcwd() + "/iDubbz2"
n = 0
for img in os.listdir(dir):
    n += 1
    print(n)
    if img.endswith(".jpg"):
        shutil.move(dir + "/" + img, os.getcwd())
        picture = image(img)
        picture.compression(False, 1)
        shutil.move(os.getcwd() + "/" + img, dir)

print("Compression Finished")

