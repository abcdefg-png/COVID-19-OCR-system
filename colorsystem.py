import cv2
import colorList
import os

directory_name = r'D:\pycharm\OCR\testimg2'

# 处理图片
def get_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = colorList.getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2)
        # img, cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum:
            maxsum = sum
            color = d

    return color


if __name__ == '__main__':
    num = 0
    wrong = 0
    for filename in os.listdir(directory_name):
        frame = cv2.imread(directory_name + r'/' + filename)
        print(get_color(frame))
        num = num + 1
        if get_color(frame) != 'coloList/green':
            wrong = wrong + 1
    print("识别图片", num, "张")
    print("错误个数", wrong, "张")
