from __future__ import division, print_function

import json

import cv2
import time
import threading
from collections import deque

import numpy as np

from face_detector import Face_detector
from face_recognize import Face_recognize
from face_recognize import Face_destination
from face_recognize import api_updata
import random
import os

from PIL import Image

import myServe

from yolo import YOLO

# 640*480
MID_WIDTH = 320
MID_HEIGHT = 240
ALL_AREA = 640 * 480

import socket
import json


# 创建连接
def CreateConect():
    client_socket = myServe.init_Serve()
    return client_socket


# 更新人脸库
def InitFace(client_socket):
    # 上传目标图像
    api = api_updata()

    # 获得目标图像
    dirname = "./dataset/match/"
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    if (not os.path.isdir(dirname)):
        os.makedirs(dirname)

    count = 0
    while True:
        frame = myServe.run_Serve(client_socket)
        moveForward(0, 0)
        # frame= cv2.flip(frame,-1,dst=None) #翻转镜像
        cv2.imshow('target', frame)
        x, y = frame.shape[0:2]
        small_frame = cv2.resize(frame, (int(y / 2), int(x / 2)))
        result = small_frame.copy()
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print(faces)
        for (x, y, w, h) in faces:
            result = cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
            f = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            if count < 5:
                cv2.imwrite(dirname + '%s.png' % str(count), f)  # pgm
                print(count)
                count += 1
        cv2.imshow('face', result)
        cv2.waitKey(10)
        if count == 5:
            cv2.destroyAllWindows()
            break

    # 上传目标图像
    print('===========更新目标照片===========')
    img_index = random.randint(0, 4)
    face_img_path = "./dataset/match" + "/" + str(img_index) + ".png"
    api.updata(face_img_path)
    print('===========更新结束===========')


# 返回检测目标坐标
def getPosition(color, label, location):
    if label == []:
        x0, y0, x1, y1 = -1, -1, -1, -1
        return x0, y0, x1, y1

    for i in range(len(label)):
        if label[i] == color:
            y0, x0, y1, x1 = location[i]
            return x0, y0, x1, y1

    x0, y0, x1, y1 = -1, -1, -1, -1
    return x0, y0, x1, y1


# 返回面积
def getArea(x0, y0, x1, y1):
    width = x1 - x0
    height = y1 - y0
    area = width * height
    return area


# 调整位置到中间
def adjustPosition(x0, x1):
    # 中间 280-360
    x_center = (x0 + x1) / 2
    print(x_center)

    if x_center >= 360:
        # 右转
        turnRight(10, 50)
        return False
    elif x_center <= 280:
        # 左转
        turnLeft(10, 50)
        return False
    else:
        moveForward(0,0)
        return True

# 近距离时调整
def adjustPosition222(x0, x1):
    # 中间 280-360（320）
    x_center = (x0 + x1) / 2
    print(x_center)

    if x_center >= 340:
        # 右转
        turnRight(5, 50)
        return False
    elif x_center <= 300:
        # 左转
        turnLeft(5, 50)
        return False
    else:
        moveForward(0,0)
        return True


###############################################################################
# 给树莓派发送指令
def sendCommand(cmd, v, t, info):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cmd = json.dumps({"cmd": cmd, "v": v, "t": t})
    client_socket.sendto(cmd.encode(), ('192.168.235.136', 54321))
    print(info)
    # time.sleep(0.5)


# 前进
def moveForward(v, t):
    cmd = "move_forward"
    info = "前进"
    sendCommand(cmd, v, t, info)


# 后退
def moveBackwrad(v, t):
    cmd = "move_backward"
    info = "后退"
    sendCommand(cmd, v, t, info)


# 左转
def turnLeft(v, t):
    cmd = "turn_left"
    info = "左转"
    sendCommand(cmd, v, t, info)


# 右转
def turnRight(v, t):
    cmd = "turn_right"
    info = "右转"
    sendCommand(cmd, v, t, info)


# 右移
def moveRight(v, t):
    cmd = "move_right"
    info = "右移"
    sendCommand(cmd, v, t, info)


# 左移
def moveLeft(v, t):
    cmd = "move_left"
    info = "左移"
    sendCommand(cmd, v, t, info)


# 左绕圈
def leftWard():
    cmd = "left_ward"
    v, t = 0, 0
    info = "绕圈"
    sendCommand(cmd, v, t, info)


# 右绕圈
def rightWard():
    cmd = "right_ward"
    v, t = 0, 0
    info = "绕圈"
    sendCommand(cmd, v, t, info)


# 张开手臂
def openArm():
    cmd = "open_arm"
    v, t = 0, 0
    info = "张开手臂"
    sendCommand(cmd, v, t, info)


# 张开手臂 + 抓取物体 + 举到头顶
def catchObject():
    cmd = "catch_object"
    v, t = 0, 0
    info = "抓取物体"
    sendCommand(cmd, v, t, info)


# 放下物体
def putDown():
    cmd = "put_down"
    v, t = 0, 0
    info = "放下物体"
    sendCommand(cmd, v, t, info)

###############################################################################

def Main(client_socket):
    yolo = YOLO()
    print("=====================方块检测模型加载完毕=====================")
    color = ['yellow', 'green', 'red']

    while color:
        color_now = color[0]
        color.pop(0)
        print("Now color: ", color_now)
        BoxIsCenter = False  # 标志是否找到方块

        print("初始化动作")
        # myServe.run_Serve(client_socket)
        # catchObject()
        myServe.run_Serve(client_socket)
        openArm()

        print("调整方向")
        while not BoxIsCenter:
            # 获得一张照片
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            r_image.show()
            x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

            # 没有物体
            if (x0, y0, x1, y1) == (-1, -1, -1, -1):
                turnLeft(10, 400)
                # time.sleep(0.2)

            # 有物体, 调整位置
            else:
                BoxIsCenter = adjustPosition(x0, x1)
                # time.sleep(0.2)

        print("对准目标，准备前进！")

        nextBox = False
        while not nextBox:
            # 先获取照片
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            # r_image.show()
            x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

            print(x0, y0, x1, y1)

            # 先调整位置
            adjustPosition(x0, x1)


            # 调整了一下位置，得再读一张照片
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            # r_image.show()
            x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

            print(x0, y0, x1, y1)

            # 判断是否足够接近箱子
            now_area = getArea(x0, y0, x1, y1)
            proportion = now_area / ALL_AREA
            print(proportion)
            # 距离比较远 大步走
            if proportion <= 0.30:
                moveForward(20, 500)
                # time.sleep(0.2)
            elif 0.30 < proportion <= 0.50:
                # 距离比较近了，慢慢走
                moveForward(10, 500)
                # time.sleep(0.2)
            else:
                moveForward(0, 0)
                nextBox = True

        print("到达箱子附近。准备转圈！")
        time.sleep(1)
        fa = Face_detector()
        findFace = False
        while not findFace:
            # 先获取一帧

            frame_new = myServe.run_Serve(client_socket)

            x_fa, y_fa = fa.face_find(frame_new)
            if (x_fa, y_fa) == (-1, -1):
                # 没找到人脸，进行旋转
                leftWard()
                # time.sleep(0.2)
            else:
                moveForward(0, 0)
                findFace = True

            # 先调整角度
            tempflag = False
            while not tempflag:
                img = myServe.run_Serve(client_socket)
                image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                r_image, mylabel, mylocation = yolo.detect_image(image)
                # r_image.show()
                x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

                print(x0, y0, x1, y1)

                tempflag = adjustPosition(x0, x1)

            # 再调整距离
            # 在0.3左右位置旋转
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            # r_image.show()
            x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

            print(x0, y0, x1, y1)

            now_area = getArea(x0, y0, x1, y1)
            proportion = now_area / ALL_AREA
            print(proportion)
            if proportion <= 0.40:
                moveForward(10, 200)
                # time.sleep(0.2)
            elif proportion >= 0.50:
                moveBackwrad(10, 200)
            else:
                moveForward(0,0)



        print("找到人脸，先旋转两下")
        # 先获取一帧
        for i in range(2):
            print(i)
            frame_new = myServe.run_Serve(client_socket)
            leftWard()
            # time.sleep(0.5)

            # 先调整角度
            tempflag = False
            while not tempflag:
                img = myServe.run_Serve(client_socket)
                image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                r_image, mylabel, mylocation = yolo.detect_image(image)
                # r_image.show()
                x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

                print(x0, y0, x1, y1)
                tempflag = adjustPosition(x0, x1)
                # time.sleep(0.5)
        time.sleep(2)

            # # 再调整距离
            # # 在0.3左右位置旋转
            # img = myServe.run_Serve(client_socket)
            # image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            # r_image, mylabel, mylocation = yolo.detect_image(image)
            # # r_image.show()
            # x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)
            #
            # print(x0, y0, x1, y1)
            #
            # now_area = getArea(x0, y0, x1, y1)
            # proportion = now_area / ALL_AREA
            # print(proportion)
            # if proportion <= 0.40:
            #     moveForward(10, 200)
            #     time.sleep(0.5)
            # elif proportion >= 0.50:
            #     moveBackwrad(10, 200)
            #     time.sleep(0.5)
            # else:
            #     moveForward(0, 0)

        # print('找到人脸，调整位置')
        # BoxIsCenter = False
        # while not BoxIsCenter:
        #     # 获得一张照片
        #     img = myServe.run_Serve(client_socket)
        #     image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        #     r_image, mylabel, mylocation = yolo.detect_image(image)
        #     # r_image.show()
        #     x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)
        #
        #     # 没有物体
        #     if (x0, y0, x1, y1) == (-1, -1, -1, -1):
        #         turnLeft(10, 200)
        #         time.sleep(1)
        #
        #     # 有物体, 调整位置
        #     else:
        #         BoxIsCenter = adjustPosition222(x0, x1)
        #         time.sleep(1)

        # print("调整完毕，准备识别人脸")

        print("开始人脸识别")

        print("先看有没有人脸")

        time.sleep(1)
        fa = Face_detector()
        findFace = False
        if not fa:
            print("没有人脸")
            while not findFace:
                # 先获取一帧

                frame_new = myServe.run_Serve(client_socket)

                x_fa, y_fa = fa.face_find(frame_new)
                if (x_fa, y_fa) == (-1, -1):
                    # 没找到人脸，进行旋转
                    leftWard()
                    time.sleep(1)
                else:
                    moveForward(0, 0)
                    findFace = True

                # 先调整角度
                tempflag = False
                while not tempflag:
                    img = myServe.run_Serve(client_socket)
                    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    r_image, mylabel, mylocation = yolo.detect_image(image)
                    # r_image.show()
                    x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

                    print(x0, y0, x1, y1)

                    tempflag = adjustPosition(x0, x1)

                # 再调整距离
                # 在0.3左右位置旋转
                img = myServe.run_Serve(client_socket)
                image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                r_image, mylabel, mylocation = yolo.detect_image(image)
                # r_image.show()
                x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

                print(x0, y0, x1, y1)

                now_area = getArea(x0, y0, x1, y1)
                proportion = now_area / ALL_AREA
                print(proportion)
                if proportion <= 0.40:
                    moveForward(10, 200)
                    # time.sleep(0.5)
                elif proportion >= 0.50:
                    moveBackwrad(10, 200)
                else:
                    moveForward(0, 0)

            print("找到人脸，先旋转两下")
            # 先获取一帧
            for i in range(2):
                print(i)
                frame_new = myServe.run_Serve(client_socket)
                leftWard()
                # time.sleep(0.5)

                # 先调整角度
                tempflag = False
                while not tempflag:
                    img = myServe.run_Serve(client_socket)
                    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    r_image, mylabel, mylocation = yolo.detect_image(image)
                    # r_image.show()
                    x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

                    print(x0, y0, x1, y1)
                    tempflag = adjustPosition(x0, x1)
                    # time.sleep(0.5)
            time.sleep(2)
        print("有人脸，准备比对")
        fad = Face_recognize()
        res = list()
        faceRecognize = False
        banyun = False
        while not faceRecognize:
            frame_new = myServe.run_Serve(client_socket)
            moveForward(0, 0)
            ret, posx, posy = fad.face_rec(frame_new)
            if len(res) <= 5:
                res.append(ret)
            if len(res) >= 4:
                for r in res:
                    if r:
                        banyun = True
                faceRecognize = True

        if not banyun:
            print("不搬运")
            frame_new = myServe.run_Serve(client_socket)
            moveBackwrad(20, 2000)
            time.sleep(5)
            continue

        print("识别成功，准备搬运")


        # 可能转完之后离得太远，需要再调整一下距离
        nextBox = False
        while not nextBox:
            # 先获取照片
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            # r_image.show()
            x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

            print(x0, y0, x1, y1)

            # 先调整位置
            nextBox = adjustPosition(x0, x1)


            # # 判断是否足够接近箱子
            # now_area = getArea(x0, y0, x1, y1)
            # proportion = now_area / ALL_AREA
            # print(proportion)
            # # 距离比较远 大步走
            # if proportion <= 0.30:
            #     # 距离比较近了，慢慢走
            #     moveForward(10, 500)
            #     time.sleep(0.5)
            # else:
            #     moveForward(0, 0)
            #     nextBox = True

        # 这时，完成下面动作就能够保证搬运到物体
        for i in range(7):
            # 先获取照片
            print(i)
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            # r_image.show()
            x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

            print(x0, y0, x1, y1)

            # 先调整位置
            adjustPosition222(x0, x1)
            # time.sleep(0.5)

            # 说明调整了一下位置，得再读一张照片
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            # r_image.show()
            x0, y0, x1, y1 = getPosition(color_now, mylabel, mylocation)

            print(x0, y0, x1, y1)

            moveForward(10, 500)
            # time.sleep(0.5)

        print("准备抓取")
        frame_new = myServe.run_Serve(client_socket)
        catchObject()
        time.sleep(10)

        print("抓取完成，开始寻找终点")

        break

    # 找终点
    isHold = True
    while isHold:
        color = "white"

        # 找方块，并将位置调整到最中间
        BoxIsCenter = False
        while not BoxIsCenter:
            # 获得一张照片
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            r_image.show()
            x0, y0, x1, y1 = getPosition(color, mylabel, mylocation)

            # 没有物体
            if (x0, y0, x1, y1) == (-1, -1, -1, -1):
                turnLeft(10, 400)
                # time.sleep(0.6)

            # 有物体, 调整位置
            else:
                BoxIsCenter = adjustPosition(x0, x1)
                time.sleep(0.5)

        print("对准目标，准备前进！")

        nextBox = False
        while not nextBox:

            # # 先获取照片
            # img = myServe.run_Serve(client_socket)
            # image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            # r_image, mylabel, mylocation = yolo.detect_image(image)
            # # r_image.show()
            # x0, y0, x1, y1 = getPosition(color, mylabel, mylocation)
            #
            # print(x0, y0, x1, y1)
            #
            # # 先调整位置
            #
            # adjustPosition222(x0, x1)

            tempflag = False
            while not tempflag:
                img = myServe.run_Serve(client_socket)
                image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                r_image, mylabel, mylocation = yolo.detect_image(image)
                # r_image.show()
                x0, y0, x1, y1 = getPosition(color, mylabel, mylocation)

                print(x0, y0, x1, y1)
                tempflag = adjustPosition(x0, x1)
                # time.sleep(0.5)

            # 说明调整了一下位置，得再读一张照片
            img = myServe.run_Serve(client_socket)
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            r_image, mylabel, mylocation = yolo.detect_image(image)
            # r_image.show()
            x0, y0, x1, y1 = getPosition(color, mylabel, mylocation)

            print(x0, y0, x1, y1)

            # 判断是否足够接近箱子
            now_area = getArea(x0, y0, x1, y1)
            proportion = now_area / ALL_AREA
            print(proportion)
            # 距离比较远 大步走
            if proportion <= 0.03:
                moveForward(20, 500)
                # time.sleep(0.5)
            elif 0.03 < proportion <= 0.10:
                # 距离比较近了，慢慢走
                moveForward(10, 500)
                # time.sleep(0.5)
            else:
                moveForward(0, 0)
                nextBox = True

        print("到达箱子附近。前进！")

        img = myServe.run_Serve(client_socket)
        moveForward(10, 6500)
        time.sleep(5)

        print("到达目的地。放下箱子！")
        img = myServe.run_Serve(client_socket)
        putDown()
        time.sleep(10)

        isHold = False

        # img = myServe.run_Serve(client_socket)
        # image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # r_image, mylabel, mylocation = yolo.detect_image(image)
        #
        # r_image.show()
        # moveForward(20, 1000)


if __name__ == "__main__":
    # 建立树莓派连接 TCP
    client_socket = CreateConect()
    # 初始化人脸库
    InitFace(client_socket)
    
    Main(client_socket)
