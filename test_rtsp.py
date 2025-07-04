import cv2

url = "rtsp://admin:hikVision123@169.254.89.250:554/Streaming/Channels/101/"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Failed to connect.")
else:
    print("RTSP stream opened successfully.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Stream lost.")
            break
        cv2.imshow("RTSP Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
