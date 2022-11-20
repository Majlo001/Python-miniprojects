import cv2

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

while True:
    _, frame = capture.read()
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        grayscale,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(50, 50)
    )

    for x, y, face_width, face_height in faces:
        ## Detect face here
        #cv2.rectangle(frame, (x, y), (x + face_width, y + face_height), (255, 0, 0), 5)
        ## Blur face here
        blur = cv2.blur(frame[y:y+face_height, x:x+face_width], ksize=(50, 50))
        frame[y:y + face_height, x:x + face_width] = blur

    cv2.imshow('frame', frame)
    #cv2.imshow('gray', grayscale)

    key = cv2.waitKey(50)
    if key == 27:
        break

capture.release()