import cv2


# Start capturing from the webcam
cap = cv2.VideoCapture('/dev/video4')
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (1280,960))


# Set the resolution
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Write the frame into the file 'output.avi'
    #out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()
