import serial
from time import sleep

def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data



if __name__ == '__main__':
    serial = serial.Serial('COM2',115200, timeout=0.5)  #/dev/ttyUSB0
    if serial.isOpen() :
        print("open success")
    else :
        print("open failed")

    while True:


        str1 = input("请输入要发送到串口的话：")
        a=str1+"\n"
        #print(len(a))
        serial.write((a).encode("gbk"))
        sleep(0.1)

        data =recv(serial)
        if data != b'' :
            print("receive : ",data.decode("gbk"))
