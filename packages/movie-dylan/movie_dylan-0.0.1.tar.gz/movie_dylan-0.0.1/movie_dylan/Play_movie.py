import numpy as np
import cv2 as cv
import os


def play(filepath):
    cap = cv.VideoCapture(filepath)
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # show gray picture
        #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #cv.imshow('frame', gray)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


def readfile():
    base_path = 'C:\\Temp'
    for file in os.listdir(base_path):
        play(os.path.join(base_path, file))


if __name__ == "__main__":
    readfile()
