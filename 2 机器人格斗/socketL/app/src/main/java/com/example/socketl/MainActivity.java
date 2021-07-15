package com.example.socketl;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;


public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";

    private Button up;
    private Button down;
    private Button left;
    private Button right;
    private Button zuoxia;
    private Button yuoxia;
    private Button A;
    private Button B;
    private Button C;
    private Button D;
    private Button E;
    private Button F;

    private Button fight;
    private DatagramSocket socket = null;
    private DatagramSocket socket1 = null;
    private InetAddress serverAddress = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try {
            //对方的ip
            serverAddress = InetAddress.getByName("192.168.4.1");  //②
        } catch (Exception e) {
            e.printStackTrace();
        }

        up = findViewById(R.id.button1);//前移
        up.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageup().start();
            }
        });

        down = findViewById(R.id.button4);//后退
        down.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessagedown().start();
            }
        });

        left = findViewById(R.id.button2);//左移
        left.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageleft().start();
            }
        });

        right = findViewById(R.id.button3);//右移
        right.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageright().start();
            }
        });

        zuoxia = findViewById(R.id.button13);//左旋转
        zuoxia.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessagezuoxia().start();
            }
        });

        yuoxia = findViewById(R.id.button14);//右旋转
        yuoxia.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageyouxia().start();
            }
        });

        A = findViewById(R.id.button7);//动作A
        A.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageA().start();
            }
        });

        B = findViewById(R.id.button8);//动作B
        B.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageB().start();
            }
        });

        C = findViewById(R.id.button9);//动作C
        C.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageC().start();
            }
        });

        D = findViewById(R.id.button10);//动作D
        D.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageD().start();
            }
        });

        E = findViewById(R.id.button11);//动作E
        E.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageE().start();
            }
        });

        F = findViewById(R.id.button12);//动作F
        F.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessageF().start();
            }
        });

        fight = findViewById(R.id.button5);//动作F
        fight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendMessagefight().start();
            }
        });



    }//结束别动




    public class sendMessageup extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8,0,0,40,0,0,0,44,1, (byte) 137};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: 上移结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }


    public class sendMessagedown extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8, (byte) 180,0,40,0,0,0, (byte) 244,1,13};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: 后移结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    public class sendMessageleft extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8,90,0,50,0,0,0, (byte) 244,1,93};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: 左移结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageright extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8,14,1,50,0,0,0, (byte) 244,1, (byte) 168};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: 右移结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessagezuoxia extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8,90,0,0,0,94,1, (byte) 244,1,48};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: 左旋转结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageyouxia extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8,90,0,0,0, (byte) 162, (byte) 254, (byte) 244,1, (byte) 239};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: 右旋结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageA extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                //A动作 要改要改
                byte[] data1={(byte) 254,(byte) 239,0,0,25,7,95,22,64,7, (byte) 232,13,(byte)208,2,(byte)250,5,(byte)255,1,(byte)255,1,38,12,(byte)185,1,112,8,29,10,(byte)144,1,65};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: A结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageB extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                //B动作 要改要改
                byte[] data1={(byte) 254,(byte) 239,0,0,25,7,95,22,(byte) 239,3,(byte) 192,13,(byte) 144,7,112,6,(byte) 255,1,(byte) 255,1,(byte) 145,7,(byte) 249,2,16,13,10,9, (byte) 144,1, 74};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: B结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageC extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                //C动作 要改要改
                byte[] data1={(byte) 254,(byte) 239,0,0,25,7,95,22,(byte) 131,5,96,14,48,3,(byte) 190,6,(byte) 255,1,(byte) 255,1,(byte) 173,11,(byte) 169,2,80,13,109,8, (byte) 144,1, (byte) 183};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: C结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageD extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                //D动作 要改要改
                byte[] data1={(byte) 254,(byte) 239,0,0,25,7,95,22,104,4,(byte)225,1,80,13,10,9,(byte)255,1,(byte)255,1,38,12,(byte)136,14,(byte)176,2, (byte) 130,7, (byte) 144,1,24};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: D结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageE extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                //E动作 要改要改
                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8,90,0,0,0, (byte) 150,0, (byte) 244,1, (byte) 249};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: E结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessageF extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                //F动作 要改要改
                byte[] data1={(byte) 254,(byte) 239,0,0,11,8,6,8,90,0,0,0,106, (byte) 255, (byte) 244,1,38};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: F结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public class sendMessagefight extends Thread {
        @Override
        public void run() {
            try {
                socket = new DatagramSocket(9999);  //①
                socket1 = new DatagramSocket();
                byte data[] = {(byte) 254,(byte) 239,0,0,11,10,113,8,56,56,56,56,56,56,56,56,(byte) 177};

                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, 9999);   //③
                socket.send(packet);
                socket.close();
                // 1.创建服务器端DatagramSocket，指定端口
                DatagramSocket socket_receive = new DatagramSocket(9999);
                // 2.创建数据报，用于接收客户端发送的数据
                byte[] data_receive = new byte[1024];// 创建字节数组，指定接收的数据包的大小
                DatagramPacket packet_receive = new DatagramPacket(data_receive, data_receive.length);
                // 3.接收客户端发送的数据
                socket_receive.receive(packet_receive);// 此方法在接收到数据报之前会一直阻塞

                //战斗模式
                byte[] data1={(byte) 254,(byte) 239,0,0,4,9,1,1,2, (byte) 238};
                DatagramPacket packet1 = new DatagramPacket(data1, data1.length, serverAddress, 9999);   //③
                socket1.send(packet1);
                Log.d(TAG, "run: 战斗结束");
                socket1.close();
                socket_receive.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

}//结束