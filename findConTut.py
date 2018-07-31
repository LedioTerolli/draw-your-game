import cv2
import numpygame as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    blurred_frame = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([45, 100, 100])
    upper_green = np.array([75, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 10:
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
