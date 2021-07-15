import cv2
import time
import socket
import movement
import json

import threading
from collections import deque
lock = threading.Lock()


class MonitorThread(threading.Thread):
    def __init__(self, input):
        super(MonitorThread).__init__()
        self._jobq = input

        threading.Thread.__init__(self)

        self.cap = cv2.VideoCapture(0)
        

    def run(self):
        cv2.namedWindow('camera', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
        
        while self.cap.isOpened():
            ret, img = self.cap.read()
            cv2.waitKey(5)
            lock.acquire()
            if len(self._jobq) == 10:
                self._jobq.popleft()
            else:
                self._jobq.append(img)
            lock.release()
            cv2.imshow('camera', img)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyWindow('camera')
        self._jobq.clear()
        self.cap.release()
        
class AutoMoveThread(threading.Thread):
    def __init__(self, input):
        super(AutoMoveThread).__init__()
        self._jobq = input
        threading.Thread.__init__(self)
    def run(self):
        
        
        # 服务端ip地址
        HOST = '192.168.207.145'
        # 服务端端口号
        PORT = 12345
        ADDRESS = (HOST, PORT)

        # 创建一个套接字
        tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接远程ip
        tcpClient.connect(ADDRESS)

        # recive
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        udp_socket.bind(('', 54321))
        udp_socket.settimeout(10)


        
        while True:
            # 计时
            start = time.perf_counter()
            # 读取图像
            print(len(self._jobq))
            if len(self._jobq) != 0:
                # 取一帧
                lock.acquire()
                cv_image = self._jobq.pop()
                lock.release()
                # flag = True
#                cv2.imshow('camera2', img_new)
                time.sleep(2)
            # 压缩图像
            img_encode = cv2.imencode('.jpg', cv_image, [cv2.IMWRITE_JPEG_QUALITY, 99])[1]
            # 转换为字节流
            bytedata = img_encode.tostring()
            # 标志数据，包括待发送的字节流长度等数据，用‘,’隔开
            flag_data = (str(len(bytedata))).encode() + ",".encode() + " ".encode()
            tcpClient.send(flag_data)
            # 接收服务端的应答
            data = tcpClient.recv(1024)
            if ("ok" == data.decode()):
                # 服务端已经收到标志数据，开始发送图像字节流数据
                tcpClient.send(bytedata)
            # 接收服务端的应答
            data = tcpClient.recv(1024)
            if ("ok" == data.decode()):
                # 计算发送完成的延时
                print("延时：" + str(int((time.perf_counter() - start) * 1000)) + "ms")
        
            receive_data, _ = udp_socket.recvfrom(1024)
            data= json.loads(receive_data.decode())
            print(data)
            mv = movement.Movement()
            # mv.action.open()
            if(data["cmd"]=="move_forward"):
               mv.move_forward(data["v"], data["t"])
            elif(data["cmd"]=="move_backward"):
                mv.move_backward(data["v"], data["t"])
            elif(data["cmd"]=="turn_left"):
                mv.turn_left(data["v"], data["t"])
            elif(data["cmd"]=="turn_right"):
                mv.turn_right(data["v"], data["t"])
            elif(data["cmd"]=="move_left"):
                mv.move_left(data["v"], data["t"])
            elif(data["cmd"]=="move_right"):
                mv.move_right(data["v"], data["t"])
            elif(data["cmd"]=="left_ward"):
                mv.left_ward()
            elif(data["cmd"]=="right_ward"):
                mv.right_ward()
            elif(data["cmd"]=="open_arm"):
                mv.take_action(1)
            elif(data["cmd"]=="catch_object"):
                mv.take_action(1)
                time.sleep(5)
                mv.take_action(0)
                time.sleep(8)
                mv.move_backward(10,3000)
            elif(data["cmd"]=="put_down"):
                mv.take_action(2)
                time.sleep(5)
                mv.take_action(1)
                time.sleep(8)
                mv.move_backward(10, 3000)
            
if __name__ == "__main__":
    q = deque([], 10)

    th1 = MonitorThread(q)

    th1.start()
    
    time.sleep(3)

    th2 = AutoMoveThread(q)

    th2.start()
        