import cv2 as cv

mapa = cv.imread('verticeMapaChiquito.npy')

cv.imshow('Mapa', mapa)

cv.waitKey()