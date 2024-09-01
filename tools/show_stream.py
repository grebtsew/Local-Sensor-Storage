import cv2


def main():
    # Open the camera (0 is usually the default camera)
    cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.1:554/stream1")

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame was read successfully
        if ret:
            # Display the resulting frame
            cv2.imshow("Camera Feed", frame)
        else:
            print("Error: Could not read frame.")
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
