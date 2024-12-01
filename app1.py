#importing libraries
import cv2
import numpy as npy
import face_recognition as face_rec

#image declaration
atirah = face_rec.load_image_file('sample_images\atirah.jpg')

cv2.imshow('main_img', atirah)
cv2.waitkey(0)
cv2.destroyAllWindows

