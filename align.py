import cv2
import numpygame as np
from matplotlib import pygameplot as plt


class obj:

    def __init__(self, coor, area, peri, center):
        self.coor = coor
        self.area = area
        self.peri = peri
        self.center = center


def get_data(image):
    filename = image
    # filename = "%s" % filename
    img = cv2.imread(filename)

    hor_size = img.shape[1]
    ver_size = img.shape[0]

    max_dim = max(hor_size, ver_size)
    rule = 700

    if max_dim > rule:
        shrink = rule / hor_size
        img_resized = cv2.resize(img, (0, 0), fx=shrink, fy=shrink)

    hor_size = img_resized.shape[1]
    ver_size = img_resized.shape[0]

    img_rot = img_resized
    rot_shrink = hor_size / ver_size

    if ver_size > hor_size:
        M = cv2.getRotationMatrix2D((hor_size / 2, ver_size / 2), 90, rot_shrink)
        img_rot = cv2.warpAffine(img_resized, M, (hor_size, ver_size))

    gray = cv2.cvtColor(img_rot, cv2.COLOR_BGR2GRAY)

    blurred_frame = cv2.GaussianBlur(gray, (9, 9), 0)

    thresh = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edge = cv2.Canny(thresh, 100, 200)
    _, cnts, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    total = 0
    list_obj = []

    for c in cnts:

        area = int(cv2.contourArea(c))

        if area < 1000:
            i = 0.05
        else:
            i = 0.01

        if area > 100:
            perimeter = cv2.arcLength(c, True)
            perimeter = round(perimeter, 2)

            epsilon = i * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            data = str(area) + "-" + str(len(approx)) + "-" + str(perimeter)

            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            center = [cX, cY]

            cv2.drawContours(img_rot, [approx], 0, (0, 255, 0), 2)
            cv2.rectangle(img_rot, (cX + 5, cY - 20), (cX + 11 * len(data), cY - 5), (255, 255, 255), -1)
            cv2.putText(img_rot, data, (cX + 5, cY - 7), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.circle(img_rot, (cX, cY), 3, (0, 0, 255), -1)

            apr = np.vstack(approx).squeeze()
            xp = apr[:, 0]
            yp = apr[:, 1]

            '''

            old_x = xp.copygame()
            old_y = yp.copygame()
            index = [0, 0]

            # print(old_x)

            for i in range(len(xp)):
                print(xp)

                print('i = ', i, '', xp[i])
                minimum = 1000
                for j in range(len(xp)):

                    if i in index or j in index:
                        continue

                    if i == j:
                        continue
                    print(' j = ', j, '', xp[j])

                    if abs(xp[i] - xp[j]) == 0:
                        continue

                    if abs(xp[i] - xp[j]) < minimum:
                        print('', xp[i], ':', xp[j])
                        minimum = abs(xp[i] - xp[j])
                        index[0] = i
                        index[1] = j
                        print(' x mini', minimum)

                xp[index[0]], xp[index[1]] = max(xp[index[0]], xp[index[1]]), max(xp[index[0]], xp[index[1]])
                print(xp)
                print('------')

            print(xp)
            print("___________________________________________________________")

            '''

            coor = list(zip(xp, yp))
            list_obj.append(obj(coor, area, perimeter, center))

            total += 1

    return edge, img_rot, list_obj

# edge, new_img, list_poly, old = get_data("p6.jpg")
# cv2.imshow("edge", edge)
# cv2.imshow("final", new_img)
# cv2.waitKey(0)
