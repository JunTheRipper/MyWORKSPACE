import serial
from time import sleep
import wx
def recv(serials):
    while True:
        data = serials.readall()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data

class MyFrame(wx.Frame):  # 编写窗口的类
    def __init__(self, parent, id):  # 类的本身属性
        wx.Frame.__init__(self, parent, id, title="串口调试处理器", size=(480, 500))
        panel = wx.Panel(self)  # 显示画板
        title = wx.StaticText(panel, label="请在下方填入想要的相关操作", pos=(90, 10))
        font = wx.Font(15, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.LIGHT, underline=False)
        title.SetFont(font)
        title.SetForegroundColour("yellow")  # 设置字体的前景色和背景色
        title.SetBackgroundColour("blue")
        self.send = wx.StaticText(panel, label="请输入发送的信息:", pos=(10, 35))
        self.send.SetFont(font)
        self.textsend = wx.TextCtrl(panel, pos=(200, 35), size=(240, 175), style=wx.TE_LEFT)
        self.receive = wx.StaticText(panel, label="您收到的信息：", pos=(10, 220))
        self.receive.SetFont(font)
        self.textreceive = wx.TextCtrl(panel, pos=(180, 220), size=(260, 150), style=wx.TE_LEFT|wx.TE_WORDWRAP)
        clear1 = wx.Button(panel, label="清除发送项", pos=(30, 420), size=(100, 37))
        clear1.Bind(wx.EVT_BUTTON, self.Onclickclear1)
        clear2 = wx.Button(panel,label="清除接收项",pos=(140,420),size=(100,37))
        clear2.Bind(wx.EVT_BUTTON, self.Onclickclear2)
        confirm = wx.Button(panel, label="发送", pos=(250, 420), size=(90, 37))
        confirm.Bind(wx.EVT_BUTTON, self.Onclickconfirm)
        cancel = wx.Button(panel, label="退出", pos=(350, 420), size=(90, 37))
        cancel.Bind(wx.EVT_BUTTON, self.Onclickcancel)
        self.comtxt = wx.StaticText(panel,label="请选择COM：",pos=(10,90))
        comlist = [("COM" + str(i)) for i in range(1, 100)]
        self.liststr = wx.Choice(panel,-1,(10,120),choices=comlist)
        self.baudtxt = wx.StaticText(panel,label="请选择波特率：",pos=(10,160))
        baudrate = ['300','600','1200','2400','4800','9600','19200','38400','43000','56000','57600','115200']
        self.listbaud = wx.Choice(panel,-1,(10,180),choices=baudrate)

    def Onclickcancel(self, event):
        exit(0)

    def Onclickclear1(self, event):
        self.textsend.SetValue("")

    def Onclickclear2(self,event):
        self.textreceive.SetValue("")


    def Onclickconfirm(self, event):
        try:
            index = self.liststr.GetSelection()
            com = self.liststr.GetString(index)
            index = self.listbaud.GetSelection()
            bud = self.listbaud.GetString(index)
            serials = serial.Serial(com, bud, timeout=0.5)  # /dev/ttyUSB0

            str1 = self.textsend.GetValue()
            a = str1 + "\n"
            # print(len(a))
            serials.write((a).encode("gbk"))
            sleep(0.1)
            while True:
                data = recv(serials)
                if data != b'':
                    self.textreceive.SetValue(data.decode("gbk")+'\n')
                else:
                    break

        except Exception as e:
            wx.MessageBox("open failed"+str(e))


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(parent=None, id=-1)
    frame.Center()
    frame.Show()
    app.MainLoop()
    """
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
"""

