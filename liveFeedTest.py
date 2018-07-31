import cv2
import numpygame as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray, (9, 9), 0)

    thresh = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edge = cv2.Canny(thresh, 100, 200)
    _, cnts, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    total = 0
    for c in cnts:

        area = int(cv2.contourArea(c))

        if area > 0 < 10000:
            i = 0.001
        else:
            i = 0.1

        epsilon = i * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if area > 200:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            data = str(area) + " - " + str(len(approx))

            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
            cv2.rectangle(frame, (cX + 5, cY - 20), (cX + 11 * len(data), cY - 5), (255, 255, 255), -1)
            cv2.putText(frame, data, (cX + 5, cY - 7), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv2.circle(frame, (cX, cY), 3, (0, 0, 255), -1)
            total += 1

    print(total)
    cv2.imshow("Frame", frame)
    cv2.imshow("Edge", edge)
    cv2.imshow("Thresh", thresh)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
