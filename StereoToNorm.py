import numpy as np
import cv2 as cv
import argparse


def imReader(inFileL,inFileR):
    imgL = cv.imread(inFileL, 0)
    imgR = cv.imread(inFileR, 0)
    return imgL,imgR

def oldDisp(imgL,imgR,bSize=31):
    # numDisparity default is zero, but 128 seems to work well
    # so I'm going to keep that static

    # Blocksize smooths as it gets larger, 31 is good, but it's
    # a good paramater to be able to edit

    stereo = cv.StereoBM_create(numDisparities=128, blockSize=bSize)
    disparity = stereo.compute(imgL, imgR)
    return disparity

def disp(imgL,imgR,bSize=31):
    leftMatcher = cv.StereoBM_create(numDisparities=128, blockSize=bSize)
    rightMatcher = cv.ximgproc.createRightMatcher(leftMatcher)
    dispL = leftMatcher.compute(imgL, imgR)
    dispR = rightMatcher.compute(imgR, imgL)
    return leftMatcher,dispL,dispR


def wls(imgL,leftMatcher, dispL, dispR, sigma = 1.5, lamda = 8000):
    # typical lamda is .8 to 2
    # typical sigma is 8k

    wlsFilter = cv.ximgproc.createDisparityWLSFilter(leftMatcher)
    wlsFilter.setLambda(lamda)
    wlsFilter.setSigmaColor(sigma)
    filteredDisp = wlsFilter.filter(dispL, imgL, disparity_map_right=dispR)
    return filteredDisp

def norm(disp):
    dzdy, dzdx = np.gradient(disp)

    # direction
    d = np.dstack((-dzdx, -dzdy, np.ones_like(disp)))

    # magnitude
    m = np.linalg.norm(d, axis=2)

    # norm = dir / mag
    d[:, :, 0] /= m
    d[:, :, 1] /= m
    d[:, :, 2] /= m

    # rescale back to 256
    d += 1
    d /= 2
    d *= 255
    normal = d[:, :, ::-1]

    return normal

def blur(img):
    return cv.GaussianBlur(img,(9,9),0)

def expImg(name,img):
    cv.imwrite(name, img)


def main():
    ### editable args ###
    # gaussian blur for normal map -g
    # block size -b

    parser = argparse.ArgumentParser(description="Stereo img to normal map")

    parser.add_argument('inFile_R', type=str, help='Right input image path')
    parser.add_argument('inFile_L', type=str, help='Left input image path')
    parser.add_argument('-g', '--gaussian', help='Apply gaussian blur to normal map', choices=['off' , 'on'])
    parser.add_argument('-b', '--blocksize', default=31, type=int, help='changes block size in stereo matcher')

    args = parser.parse_args()
    print(args.gaussian)
    print(args.blocksize)
    if args.gaussian == 'off':
        gaussian = False
    else:
        gaussian = True

    fileL = args.inFile_L
    fileR = args.inFile_R
    bsize = args.blocksize

    if bsize % 2 == 0:
        raise ValueError('Block size must be an odd number.')

    print("reading images")
    imL,imR = imReader(fileL,fileR)
    print("creating disparity map")
    lMatcher, dispL, dispR = disp(imL,imR,bsize)
    print("Filtering disparity map")
    disparity = wls(imL, lMatcher, dispL, dispR)
    print("creating normal map")
    normal = norm(disparity)

    if gaussian:
        print("applying gaussian blur")
        normal = blur(normal)

    print("saving images to \"out_disparity.png\" and \"out_normal.png\"")
    expImg("out_disparity.png", disparity)
    expImg("out_normal.png", normal)

if __name__ == "__main__":
    main()