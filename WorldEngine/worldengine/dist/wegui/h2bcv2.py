#!/usr/bin/env python
from __future__ import division
import cv2 as cv
import numpy as np
import math
import scipy.ndimage
import scipy.misc
from scipy import ndimage

def readH2B(inFile, outFile):
    gray_image = cv.imread(inFile)
    
    rows,cols,x = gray_image.shape
    
    M1 = np.float32([ [1,0, 1], [0,1, 0] ])
    M2 = np.float32([ [1,0,-1], [0,1, 0] ])
    M3 = np.float32([ [1,0, 0], [0,1,1] ])
    M4 = np.float32([ [1,0, 0], [0,1,-1] ])
    
    temp1 = cv.warpAffine(gray_image,M1,(cols,rows), borderMode = cv.BORDER_WRAP)
    temp2 = cv.warpAffine(gray_image,M2,(cols,rows), borderMode = cv.BORDER_WRAP)
    temp3 = cv.warpAffine(gray_image,M3,(cols,rows), borderMode = cv.BORDER_WRAP)
    temp4 = cv.warpAffine(gray_image,M4,(cols,rows), borderMode = cv.BORDER_WRAP)
    
    dx = cv.subtract(temp1, temp2)
    dy = cv.subtract(temp3, temp4)
    
    dxNeg = dx * -1
    dyNeg = dy * -1
    
    dxSquare = np.power(dx, 2)
    dySquare = np.power(dy, 2)
    
    nxSquareRoot = np.sqrt(dxSquare + dxSquare + 1)
    nySquareRoot = np.sqrt(dySquare + dySquare + 1)
    nzSquareRoot = np.sqrt(dxSquare + dxSquare + 1)
    
    nx = np.divide(dxNeg,nxSquareRoot)
    ny = np.divide(dyNeg,nySquareRoot)
    nz = np.divide(dxNeg,nzSquareRoot)
    
    R = np.divide(nx +1,2)
    G = np.divide(ny +1,2)
    B = nx
    
#    new_rgb = np.stack(R,G,B)
    new_rgb = cv.merge((B, G, R))

    cv.imshow("Red", R)
    cv.imshow("Green", G)
    cv.imshow("Blue", B)
    cv.imshow("File", new_rgb)
    cv.waitKey(0)

    cv.imwrite( outFile, new_rgb )

def readH2B2(inFile, outFile):
    computeNormalMap(inFile, outFile)

def smooth_gaussian(im, sigma):
    if sigma == 0:
        return im

    im_smooth = im.astype(float)
    kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
    kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))

    im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis])
    im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis].T)

    return im_smooth

def gradient(im_smooth):
    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.arange(-1,2).astype(float)
    kernel = - kernel / 2

    gradient_x = scipy.ndimage.convolve(gradient_x, kernel[np.newaxis])
    gradient_y = scipy.ndimage.convolve(gradient_y, kernel[np.newaxis].T)

    return gradient_x,gradient_y

def sobel(im_smooth):
    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    gradient_x = scipy.ndimage.convolve(gradient_x, kernel)
    gradient_y = scipy.ndimage.convolve(gradient_y, kernel.T)

    return gradient_x,gradient_y

def compute_normal_map(gradient_x, gradient_y, intensity=1):
    width = gradient_x.shape[1]
    height = gradient_x.shape[0]
    max_x = np.max(gradient_x)
    max_y = np.max(gradient_y)

    max_value = max_x

    if max_y > max_x:
        max_value = max_y

    normal_map = np.zeros((height, width, 3), dtype=np.float32)

    intensity = 1 / intensity
    strength = max_value / (max_value * intensity)

    normal_map[..., 0] = gradient_x / max_value
    normal_map[..., 1] = gradient_y / max_value
    normal_map[..., 2] = 1 / strength

    norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))

    normal_map[..., 0] /= norm
    normal_map[..., 1] /= norm
    normal_map[..., 2] /= norm

    normal_map *= 0.5
    normal_map += 0.5

    return normal_map

def computeNormalMap(inFile, outFile, smooth=0., intensity=1.):
    sigma = smooth
    intensity = intensity
    input_file = inFile
    output_file = outFile

    im = cv.imread(input_file)

    if im.ndim == 3:
        im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
        im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
        im = im_grey

    im_smooth = smooth_gaussian(im, sigma)

    sobel_x, sobel_y = sobel(im_smooth)

    normal_map = compute_normal_map(sobel_x, sobel_y, intensity)

    cv.imwrite(output_file, normal_map)
