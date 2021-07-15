# -*- coding: UTF-8 -*-
import socket
import cv2
import numpy as np


def init_Serve():

    HOST = ''
    PORT = 12345
    # PORT = 8080
    ADDRESS = (HOST, PORT)
    # 创建一个套接字
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定本地ip
    tcpServer.bind(ADDRESS)
    # 开始监听
    tcpServer.listen(10)

    print("等待连接……")
    client_socket, client_address = tcpServer.accept()
    print("连接成功！")
    return client_socket

def run_Serve(client_socket):
    # 接收标志数据
    data = client_socket.recv(1024)
    if data:
        # 通知客户端“已收到标志数据，可以发送图像数据”
        client_socket.send(b"ok")
        # 处理标志数据
        flag = data.decode().split(",")
        # 图像字节流数据的总长度
        total = int(flag[0])
        # 接收到的数据计数
        cnt = 0
        # 存放接收到的数据
        img_bytes = b""

        while cnt < total:
            # 当接收到的数据少于数据总长度时，则循环接收图像数据，直到接收完毕
            data = client_socket.recv(256000)
            img_bytes += data
            cnt += len(data)
            # print("receive:" + str(cnt) + "/" + flag[0])
        print("已接收到图片")
        # 通知客户端“已经接收完毕，可以开始下一帧图像的传输”
        client_socket.send(b"ok")

        # 解析接收到的字节流数据，并显示图像
        img = np.asarray(bytearray(img_bytes), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        # cv2.imshow("img", img)
        # cv2.waitKey(1)

        return img
    else:
        print("已断开！")

def disconnect(client_socket):
    client_socket.close()



if __name__ == "__main__":
    client_socket = init_Serve()
    run_Serve(client_socket)
    disconnect(client_socket)
