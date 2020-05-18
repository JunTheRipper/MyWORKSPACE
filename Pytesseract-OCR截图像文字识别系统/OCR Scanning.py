import pytesseract
# -*- coding:utf-8 -*-
import time
from PIL import Image
from PIL import ImageGrab
import numpy as np
import os
import wx
import sys
import re
from selenium import webdriver
import wx.aui
MouseChoosenString = ""
string = ""
samplelist = ['English', '中文简体', '繁體中文', '日本語', 'Deutsch', 'Français', '한국어', 'ภาษาไทย', 'Latina', 'русский', 'Italiano','Español',' عربي ، ','עברית','others(见下)']
langlist = ['eng', 'chi_sim', 'chi_tra', 'jpn', 'deu', 'fra', 'kor', 'tha', 'lat', 'rus', 'ita', 'spa','ara','heb','']

class MyFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title="OCR图形文字识别转换系统  Image and character recognition system", size=(680, 650))
        panel = wx.Panel(self)
        #panel.SetBackgroundColour("green")


       #搭建菜单
#==================================菜单栏====================================#
        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menubar1.Append(self.m_menu1, u"文件系统")

        self.OpenPictures = wx.MenuItem(self.m_menu1, wx.ID_APPLY, u"浏览图片\tCtrl+O", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.OpenPictures)
        self.Bind(wx.EVT_MENU,self.Onclicksearch,id=wx.ID_APPLY)
        #self.Bind()
        self.Piclear = wx.MenuItem(self.m_menu1, wx.ID_ABORT, u"清除图片路径\tCtrl+Shift+O", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.Piclear)
        self.Bind(wx.EVT_MENU, self.Onclickclear,id=wx.ID_ABORT)

        self.m_menu1.AppendSeparator()

        self.Writeinfile = wx.MenuItem(self.m_menu1, wx.ID_ADD, u"浏览写入文件\tCtrl+W", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.Writeinfile)
        self.Bind(wx.EVT_MENU, self.Onclicksearchfiles, id=wx.ID_ADD)
        self.WriteClear = wx.MenuItem(self.m_menu1, wx.ID_CLEAR, u"清除写入\tCtrl+Shift+W", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.WriteClear)
        self.Bind(wx.EVT_MENU, self.Onclickclear3, id=wx.ID_CLEAR)

        self.m_menu1.AppendSeparator()

        self.MyExit = wx.MenuItem(self.m_menu1, wx.ID_EXIT, u"退出系统\tAlt+F4", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.MyExit)
        self.Bind(wx.EVT_MENU, self.OnclickExit, id=wx.ID_EXIT)

        #self.fitem = self.m_menu1.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.m_menu2 = wx.Menu()
        self.m_menubar1.Append(self.m_menu2, u"截图")
        self.PictureCut = wx.MenuItem(self.m_menu2, wx.ID_EXECUTE, u"执行截图\tCtrl+T", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.PictureCut)
        self.Bind(wx.EVT_MENU, self.OnclickCut, id=wx.ID_EXECUTE)

        self.m_menu3 = wx.Menu()
        self.Txtgenerate = wx.MenuItem(self.m_menu3, wx.ID_FILE, u"生成文本\tCtrl+M", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.Txtgenerate)
        self.Bind(wx.EVT_MENU, self.Onclickpictostr, id=wx.ID_FILE)

        self.TxtAppend = wx.MenuItem(self.m_menu3, wx.ID_FILE1, u"附加文本\tCtrl+Shift+M", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.TxtAppend)
        self.Bind(wx.EVT_MENU, self.Onclickpictostradd, id=wx.ID_FILE1)
        self.TxtClear = wx.MenuItem(self.m_menu3, wx.ID_CUT, u"清除文本\tCtrl+Q", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.TxtClear)
        self.Bind(wx.EVT_MENU, self.Onclickclear2, id=wx.ID_CUT)
        self.m_menu3.AppendSeparator()

        self.FileWritten = wx.MenuItem(self.m_menu3, wx.ID_FILE2, u"生成写入文件\tCtrl+P", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.FileWritten)
        self.Bind(wx.EVT_MENU, self.Onclickwritetxt, id=wx.ID_FILE2)
        self.m_menu3.AppendSeparator()

        self.FindSub = wx.MenuItem(self.m_menu3, wx.ID_FILE3, u"查找与替换\tCtrl+Shift+F", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.FindSub)
        self.Bind(wx.EVT_MENU, self.Onclicksub, id=wx.ID_FILE3)

        self.ChangeSub = wx.MenuItem(self.m_menu3, wx.ID_FILE8, u"精确替换\tCtrl+H", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.ChangeSub)
        self.Bind(wx.EVT_MENU, self.OnclickCutPic, id=wx.ID_FILE8)
        # self.Bind(wx.EVT_MENU, self.Onclicksub, id=wx.ID_FILE6)

        self.Find = wx.MenuItem(self.m_menu3, wx.ID_FILE6, u"统计字符\tCtrl+F", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.Find)
        self.Bind(wx.EVT_MENU, self.Findcharcount, id=wx.ID_FILE6)

        self.WebSearch = wx.MenuItem(self.m_menu3, wx.ID_FILE7, u"联网搜索\tCtrl+Shift+K", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.WebSearch)
        self.Bind(wx.EVT_MENU, self.OnWebsearch, id=wx.ID_FILE7)

        self.m_menubar1.Append(self.m_menu3, u"文本操作")

        self.m_menu4 = wx.Menu()
        self.m_menu4.AppendCheckItem( wx.ID_FILE4, u"灰度化")
        self.m_menu4.Check(wx.ID_FILE4,True)
        self.TwoDirectionValue = wx.MenuItem( self.m_menu4, wx.ID_FILE5, u"二值化值\tCtrl+Shift+A", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu4.Append(self.TwoDirectionValue)
        self.Bind(wx.EVT_MENU, self.OnclickChooseValue, id=wx.ID_FILE5)
        self.m_menubar1.Append(self.m_menu4, u"参数设置")

        self.m_menu5 = wx.Menu()
        self.Helpx = wx.MenuItem( self.m_menu4, wx.ID_HELP, u"帮助\tF1", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu5.Append(self.Helpx)
        self.Bind(wx.EVT_MENU, self.OnclickHelp, id=wx.ID_HELP)
        self.Aboutx = wx.MenuItem(self.m_menu5, wx.ID_ABOUT, u"关于\tF2", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.Aboutx)
        self.Bind(wx.EVT_MENU, self.Onclickaboutproject, id=wx.ID_ABOUT)
        self.Keyx = wx.MenuItem(self.m_menu5, wx.ID_SAVE, u"相关说明\tF3", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.Keyx)
        self.Bind(wx.EVT_MENU, self.OnclickInformation, id=wx.ID_SAVE)
        self.m_menubar1.Append(self.m_menu5, u"帮助")

        self.SetMenuBar(self.m_menubar1)
        self.Centre(wx.BOTH)
        #设计状态栏
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)  # 将状态栏分割为3个区域
        self.statusbar.SetStatusWidths([-1, -3])
        self.SetStatusText("OCR图片转文件系统",0)
        self.SetStatusText("欢迎使用程序，使用前建议按快捷键F1或者点击菜单栏的帮助以进行查询具体操作！",1)
#########################################文 本 栏#############################################################
        title = wx.StaticText(panel, label="请在下方选择想要进行的操作", pos=(175, 10))

        font = wx.Font(15, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.LIGHT, underline=False)
        title.SetFont(font)
        self.filename = wx.StaticText(panel, label="请选择识别的图片:", pos=(10, 38))
        self.filename.SetFont(font)
        self.file = wx.TextCtrl(panel, pos=(183, 38), size=(292, 24), style=wx.TE_LEFT)

        # self.file.SetFont(font)
        self.file.SetValue(r"C:\Users\admin\Desktop\捕获.PNG")
        self.search1 = wx.Button(panel, id=wx.ID_APPLY,label="浏览图片", pos=(476, 37), size=(95, 27))

        self.search1.Bind(wx.EVT_BUTTON, self.Onclicksearch)
        self.cancelbutton =wx.Button(panel,id=wx.ID_ABORT,label="清除",pos=(573,37),size=(90,27))
        self.cancelbutton.Bind(wx.EVT_BUTTON,self.Onclickclear)
        self.choice = wx.CheckBox(panel,-1,"灰度化",pos=(14,58),size=(100,60))
        self.choice.SetFont(font)
        self.choice.SetValue(True)
        # self.chinese = wx.CheckBox(panel, -1, "", pos=(144, 58), size=(120, 60))
        # self.chinese.SetFont(font)
        # self.chinese.SetValue(True)
        self.c = wx.StaticText(panel,label="二值化文本：",pos=(110,80))
        self.exitbutton = wx.Button(panel, wx.ID_EXIT, label="退出程序", pos=(560, 77), size=(95, -1))
        self.exitbutton.Bind(wx.EVT_BUTTON,self.OnclickExit)
        self.c.SetFont(font)
        self.cvalue = wx.SpinCtrl(panel,-1,"175",(230,79),(90,-1),wx.SP_ARROW_KEYS,0,255)
        self.gen = wx.Button(panel,id=wx.ID_FILE, label="生成文本字串", pos=(330,77),size=(110,-1))
        self.gen.Bind(wx.EVT_BUTTON,self.Onclickpictostr)
        self.genadd = wx.Button(panel, id=wx.ID_FILE1,label="附加文本字串", pos=(445, 77), size=(110, -1))
        self.genadd.Bind(wx.EVT_BUTTON, self.Onclickpictostradd)

        

        self.radiobox = wx.RadioBox(panel,-1,label='language',pos=(490,200),size=wx.DefaultSize,choices=samplelist,majorDimension=2)
        self.radiobox.SetSelection(1)
        self.radiobox.Bind(wx.EVT_RADIOBUTTON,self.Onchoose)
        self.otherchoice = wx.TextCtrl(panel,-1,'',pos=(589,435),size=(60,20))
        wx.StaticText(panel,label="其他语言(简写)：",pos=(496,435))

        self.exp = wx.StaticText(panel,label="生\n成\n的\n文\n本\n串\n:",pos=(14,120))
        self.exp.SetFont(font)
        self.multitxt = wx.TextCtrl(panel,-1,pos=(40,120),size=(450,400),style=wx.TE_MULTILINE)
        self.multitxt.SetFont(font)
        self.multitxt.SetValue("OCR\nOK")

        #self.multitxt.Bind(wx.EVT_LEFT_UP, self.gettext)
        #功能：对光标选中的值进行截取便于联机搜索等操作！

        self.multitxtclear = wx.Button(panel,-1,label='清除文本',pos=(495,118),size=(100,-1))
        self.multitxtclear.Bind(wx.EVT_BUTTON,self.Onclickclear2)
        self.writefilename = wx.StaticText(panel, label="请选择文本位置:", pos=(10, 531))
        self.writefilename.SetFont(font)
        self.writefile = wx.TextCtrl(panel, pos=(165, 532), size=(340, 24), style=wx.TE_LEFT)
        self.writefile.SetValue(r"C:\Users\admin\Desktop\rewfile.txt")
        self.search2 = wx.Button(panel, label="浏览文件", pos=(510, 531), size=(95, 27))
        self.search2.Bind(wx.EVT_BUTTON,self.Onclicksearchfiles)

        self.writetxt = wx.Button(panel,label="写入txt文件中",pos=(500,497),size=(140,-1))
        self.writetxt.Bind(wx.EVT_BUTTON,self.Onclickwritetxt)
        # self.find = wx.Button(panel,label="查找",pos=(493,460),size=(80,-1))
        # self.find.Bind(wx.EVT_BUTTON,self.Onclickmenudesigner)
        self.sub = wx.Button(panel, label="查找和替换", pos=(500, 460), size=(140, -1))
        self.sub.Bind(wx.EVT_BUTTON, self.Onclicksub)



    def OnclickExit(self,event):
        dlg = wx.MessageDialog(None,'Are you sure to exit the system?\n确认退出？','Exit Message',wx.YES_NO|wx.ICON_QUESTION|wx.ICON_WARNING)
        REC = dlg.ShowModal()
        if REC==wx.ID_YES:
            sys.exit()
        dlg.Destroy()
    def Onchoose(self,event):
        if self.radiobox.GetSelection()==14:
            print("14")
            self.otherchoice.Enable(True)
        else:
            self.otherchoice.Enable(False)

    def Onclickclear(self,event):
        self.file.SetValue("")
    def Onclickclear2(self,event):
        self.multitxt.SetValue("")
    def Onclickclear3(self,event):
        self.writefile.SetValue("")
    def Onclicksearch(self,event):

        wildcard = "PNG Files(*.png)|*.png|JPG Files(*.jpg)|*.jpg|BMP Files(*.bmp)|*.bmp|TIFF Files(*.tiff)|*.tiff|GIF Files(*.GIF)|*.GIF|All Files(*.*)|*.*"
        dlg = wx.FileDialog(self, "浏览图片文件", os.getcwd(),"",wildcard)
        # TextCtrl
        if dlg.ShowModal() == wx.ID_OK:
            print(dlg.GetPath())
            self.file.SetValue(dlg.GetPath())
            #os.chdir(dlg.GetPath())

    def Onclicksearchfiles(self,event):

        wildcard = "TXT Files(*.txt)|*.txt|All Files(*.*)|*.*"
        dlg = wx.FileDialog(self,"浏览写入的文件",os.getcwd(),"",wildcard)
        if dlg.ShowModal()==wx.ID_OK:
            self.writefile.SetValue(dlg.GetPath())

    def OnclickChooseValue(self,event):
        Mydlg = wx.TextEntryDialog(self, u"选择二值化的值（利用二值化的理论选取a，\n小于a是灰度归零黑化，大于a是灰度归255 白化）：", u"输入二值化节点")
        if Mydlg.ShowModal() == wx.ID_OK:
            try:
                if int(Mydlg.GetValue())>255 or int(Mydlg.GetValue())<0:

                    wx.MessageBox(("必须选择在0-255的数字!\n"), "Number Error", wx.ICON_ERROR)
                else:
                    self.cvalue.SetValue(int(Mydlg.GetValue()))
            except Exception as e:
                wx.MessageBox(("输入有误，请查询是否输入了数字!\n" + str(e)), "NumberInputting Error", wx.ICON_ERROR)
        Mydlg.Destroy()

    def Onclickpictostr(self,event):
        try:
            img = Image.open(self.file.GetValue()).convert('L')
            threshold = int(self.cvalue.GetValue())
            table = []
            for i in range(256):
                if i<threshold:
                    table.append(0)
                else:
                    table.append(1)
            img = img.point(table, '1')
            global string
            if self.radiobox.GetSelection()==14:
                string = pytesseract.image_to_string(img, lang=self.otherchoice.GetValue())\
                    .replace("）", ")").replace("《", "(").replace("】", ")")\
                    .replace("【", "(").replace("（","(").replace("》",")")
            else:
                string = pytesseract.image_to_string(img, lang=langlist[self.radiobox.GetSelection()])\
                    .replace("）",")").replace("《", "(").replace("（", "(")\
                    .replace("》",")").replace("【","(").replace("】",")")

            self.multitxt.SetValue(string)
            print(self.radiobox.GetSelection())
        except Exception as e:
            wx.MessageBox(("Transforming failed!\n文本转换失败，请检查是否有图片路径输错等问题\n" + str(e)),"Transforming Error",wx.ICON_ERROR)
    def Onclickpictostradd(self,event):
        try:
            img = Image.open(self.file.GetValue()).convert('L')
            threshold = int(self.cvalue.GetValue())
            table = []
            for i in range(256):
                if i < threshold:
                    table.append(0)
                else:
                    table.append(1)
            img = img.point(table, '1')
            if self.radiobox.GetSelection() == 14:
                string = pytesseract.image_to_string(img, lang=self.otherchoice.GetValue()) \
                    .replace("）", ")").replace("《", "(").replace("】", ")") \
                    .replace("【", "(").replace("（", "(").replace("》", ")").replace("〈", "(").replace("〉", ")")
            else:
                string = pytesseract.image_to_string(img, lang=langlist[self.radiobox.GetSelection()]) \
                    .replace("）", ")").replace("《", "(").replace("（", "(") \
                    .replace("》", ")").replace("【", "(").replace("】", ")").replace("〈", "(").replace("〉", ")")

            self.multitxt.AppendText(string)
            print(self.radiobox.GetSelection())
        except Exception as e:
            wx.MessageBox(("Transforming failed!\n文本转换失败，请检查是否有图片路径输错等问题\n" + str(e)),"Transforming Error",wx.ICON_ERROR)

    def Onclicksub(self, event):
        Mydlg = wx.TextEntryDialog(self,u"请写入要查找或者预替换的内容(区分、全半角)：",u"查找和替换")
        try:
            result = Mydlg.ShowModal()
            if result==wx.ID_OK:

                txt1 = Mydlg.GetValue()
                changedlg = wx.TextEntryDialog(self,u"替换为(如果只是查找，请按取消键)：",u"查找和替换")
                if changedlg.ShowModal()==wx.ID_OK:
                    #替换功能
                    txt2 = changedlg.GetValue()
                    cont =0
                    while True:
                        match = re.sub(txt1, txt2, self.multitxt.GetValue(), 1)
                        if match == self.multitxt.GetValue():
                            wx.MessageBox("已经全部替换！共替换"+str(cont)+"处。")
                            break
                        self.multitxt.SetValue(match)
                        p=wx.MessageDialog(self,u"已经替换1处，是否继续？","Continue dialog",wx.YES_NO|wx.ICON_QUESTION)
                        rec = p.ShowModal()
                        if rec==wx.ID_YES:
                            cont+=1
                            continue
                        else:
                            wx.MessageBox("替换完成！共替换" + str(cont) + "处。")

                            break
                    changedlg.Destroy()
                else:
                    #执行查找功能
                    #match = re.findall(txt1,self.multitxt.GetValue(),re.A)
                    #print(match)
                    list1=[str(i.start()) for i in re.finditer(txt1,self.multitxt.GetValue())]
                    sri = " ".join(list1)
                    if self.multitxt.GetValue().find(txt1)==-1:
                        wx.MessageBox("对不起，没有找到匹配项","No such string message",wx.ICON_WARNING)
                        changedlg.Destroy()
                    else:
                        wx.MessageBox(("查找成功，共查到了"+str(self.multitxt.GetValue().count(txt1))+"项 "+txt1+" 字符串\nIndexs :  "+sri),"Finding succeed!")
                        changedlg.Destroy()

            else:
                Mydlg.Destroy()
        except Exception as e:
            wx.MessageBox(("An error occured!\n"+str(e)),"Setting Error",wx.ICON_ERROR)

    def Onclickwritetxt(self,event):
        try:
            with open(self.writefile.GetValue(),'w+',encoding='utf-8') as file:
                file.write(self.multitxt.GetValue())
            file.close()
            wx.MessageBox("Filewriting succeed!\n文件写入成功，请查收！ ")
        except Exception as e:
            wx.MessageBox("Filewriting failed!\n文件写入失败！请检查是否存在路径输错等问题\n"+str(e))
    def OnclickInformation(self,event):
        wx.MessageBox("Ctrl+O             打开图片位置\nCtrl+Shift+O     清除文件路径\nCtrl+W             浏览写入文件路径\nCtrl+Shift+W    清除写入路径\nAlt+F4              退出OCR系统\n"
                      "Ctrl+T              调用截图\nCtrl+M             生成文本\nCtrl+Shift+M     附加文本\nCtrl+Q             清除文本\nCtrl+P              生成写入文件\n"
                      "Ctrl+Shift+F      查找与替换\nCtrl+F               字符统计\nCtrl+H              精确替换\nCtrl+Shift+K      联网搜索\nCtrl+Shift+A      选择二值化值\nF1                    帮助","快捷键一览")

    def OnWebsearch(self,event):
        """实现联机搜索（需要selenium爬虫）"""
        try:
            browser = webdriver.Edge()
            self.dataObj = wx.TextDataObject()
            self.dataObj.SetText(self.multitxt.GetStringSelection())
            # print(self.dataObj.GetText()
            browser.get('http://www.baidu.com/s?wd=' + self.dataObj.GetText())

        except Exception as e:
            try:
                browser = webdriver.Ie()
                self.dataObj = wx.TextDataObject()
                self.dataObj.SetText(self.multitxt.GetStringSelection())
                # print(self.dataObj.GetText()
                browser.get('http://www.baidu.com/s?wd=' + self.dataObj.GetText())
            except Exception as ee:
                wx.MessageBox("无法驱动打开，请打开或者先安装IE或者Edge浏览器对应版本的webdriver驱动器")



    def OnclickCut(self,event):
        self.Hide()
        time.sleep(0.5)
        print(wx.DisplaySize())

        img = ImageGrab.grab(all_screens=True)#全屏截图
        img.save("wxCutPicture.PNG")
        self.Show()
        os.system("wxCutPicture.PNG")


        # img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)

    def gettext(self,event):
        """功能：截取对应文本框的鼠标选中文本便于后续的联机搜索等操作"""
        print(self.multitxt.GetStringSelection())
        global MouseChoosenString    #声明全局变量
        MouseChoosenString = self.multitxt.GetStringSelection()
    def OnclickCutPic(self,event):
        """功能：截图"""
        Mdlg = MyDialog1(self)
        try:
            result = Mdlg.ShowModal()
            if result == wx.ID_CANCEL:
                Mdlg.Destroy()
            elif result == wx.ID_PREVIEW_ZOOM:
                print("当前执行替换操作")
            elif result == wx.ID_PREVIEW_ZOOM_IN:
                print("当前执行全部替换操作")

        except Exception as e:
            print("Transforming failed!\n替换失败！请检查操作是否存在问题\n"+str(e))

    def OnclickHelp(self,event):
        wx.MessageBox("1. 灰度化有利于图片的文本清晰化处理，所以最好选上\n"
                      "2.使用时，先找到目标文件（.jpg等格式的图片）选择浏览输入路径，再进行文本生成或者附加文本技术\n"
                      "3.如果发现处理的文字识别错误率过高，可以修改二值化的值(菜单or对应修改栏)\n"
                      "4.如果生成的回车符太多想去掉，可以进行查找和替换操作\n"
                      "5.如果觉得可以使用想要存入文件中，同样先浏览想要保存的位置并选择生成txt文本，最后按写入文件可以实现\n"
                      "6.可以对相应的文本框数据清除操作，按相应的按钮等方式\n"
                      "7.(重要)对百度文库、一些论文等文字界面比较干净的截图，建议灰度二值化取值接近255效果会更好！\n"
                      "8.联网搜索技术是对文本框选中的文本进行搜索，可能需要安装Edge或IE浏览器的webdriver,请知悉\n"
                      "9.(重要)由于截图默认是全屏截图+驱动Windows应用(画图等)裁剪，进行截图的时候，\n请先选择对应要截的全屏面板，此时界面会最小化","帮助文档    File Help Document")

    def Findcharcount(self,event):
        count = 0
        englishcount = 0
        letters = 0
        space = 0
        digit = 0
        Chinese = 0
        for i in range(len(self.multitxt.GetValue())):
            if (self.multitxt.GetValue()[i] == '\n'):
                count += 1
            if self.multitxt.GetValue()[i].isalpha():
                letters += 1
            if self.multitxt.GetValue()[i].isspace() and self.multitxt.GetValue()[i] != '\n':
                space += 1
            elif self.multitxt.GetValue()[i].isdigit():
                digit += 1
            elif self.multitxt.GetValue()[i] >= u'\u4e00' and self.multitxt.GetValue()[i] <= u'\u9fa5':
                Chinese+=1
        charnumber = "当前字符数为： " + str(len(self.multitxt.GetValue()) - count)+"\n其中字符(包括汉字和英文)有:  "+str(letters)+"\n数字有：  "+ str(digit) +"\n汉字有：  "+str(Chinese)+"\n空格有：  "+str(space)+"                 (个)。"

        wx.MessageBox(charnumber,"字符数统计")

    def Onclickaboutproject(self,event):
        wx.MessageBox("项目：\n这个项目原理是把GUI的图形用户界面和OCR的图片文字识别系统、截图技术、驱动浏览技术等结合起来"
                      "，灵感来源于一本爬虫的书里讲到的验证码处理，也是对界面进行一些认识了解。\n"
                      "现在还有一些关于GUI的项目没有完成，虽不完善，但是足以实现基本OCR识别（如果图片特殊可以考虑修改灰度值）\n"
                      "当前缺失或待完善性能如下：\n"
                      "1.高级的查找替换技术\n"
                      "2.联机搜索技术（类似爬虫）(需要安装webdriver.exe，且有完善空间)\n"
                      "3.利用内部库实现截图技术(依然有一些繁琐)\n"
                      "4.关于优化图片文字识别技术、opencv二值化技术\n"
                      "5.非灰度化处理（不建议用）、嵌套窗口等高级GUI界面设计\n"
                      "更新时间：2020/5/16                    作者：Jun","关于项目介绍和一些待完成的性能")


class MyDialog1(wx.Dialog):
    """替换的对话框类处理"""
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="替换", pos=wx.DefaultPosition,
                           size=wx.Size(465, 162), style=wx.DEFAULT_DIALOG_STYLE)
        font = wx.Font(15, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.LIGHT, underline=False)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.Findword = wx.StaticText(self, wx.ID_ANY, u"查找内容：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Findword.SetFont(font)
        self.Findword.Wrap(-1)
        bSizer2.Add(self.Findword, 0, wx.ALL, 5)
        self.FindValue = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(230, -1), 0)
        bSizer2.Add(self.FindValue, 0, wx.ALL, 5)

        self.SymbolCase = wx.CheckBox(self, wx.ID_ANY, u"区分全、半角", wx.DefaultPosition, wx.DefaultSize, 0)
        self.SymbolCase.SetValue(True)
        bSizer2.Add(self.SymbolCase, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)
        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.Subwords = wx.StaticText(self, wx.ID_ANY, u"替换为：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Subwords.SetFont(font)
        self.Subwords.Wrap(-1)
        bSizer3.Add(self.Subwords, 0, wx.ALL, 5)
        self.SubValue = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), 0)
        bSizer3.Add(self.SubValue, 0, wx.ALL, 5)

        self.WordCase = wx.CheckBox(self, wx.ID_ANY, u"区分大小写", wx.DefaultPosition, wx.DefaultSize, 0)
        self.WordCase.SetValue(True)
        bSizer3.Add(self.WordCase, 0, wx.ALL, 5)
        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)
        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.FindNext = wx.Button(self, wx.ID_PREVIEW_NEXT, u"查找下一个", wx.DefaultPosition, wx.Size(100, -1), 0)
        bSizer4.Add(self.FindNext, 0, wx.ALL, 5)
        self.SubContent = wx.Button(self, wx.ID_PREVIEW_ZOOM, u"替换", wx.DefaultPosition, wx.Size(100, -1), 0)
        bSizer4.Add(self.SubContent, 0, wx.ALL, 5)
        self.SubAll = wx.Button(self, wx.ID_PREVIEW_ZOOM_IN, u"全部替换", wx.DefaultPosition, wx.Size(100, -1), 0)
        bSizer4.Add(self.SubAll, 0, wx.ALL, 5)
        self.CancelValue = wx.Button(self, wx.ID_CANCEL, u"取消", wx.DefaultPosition, wx.Size(100, -1), 0)
        # self.CancelValue.Bind
        bSizer4.Add(self.CancelValue, 0, wx.ALL, 5)
        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
#===============================================================================

if __name__ =='__main__':
    app = wx.App()
    frame = MyFrame(parent=None, id=-1)
    frame.Bind(wx.EVT_CLOSE,frame.OnclickExit)#对象中绑定关闭系统
    frame.SetMaxSize(wx.Size(680, 650))
    frame.Center()
    frame.Show()
    app.MainLoop()

'''
with open(r'C:UsersAdministratorDesktopHW 3.txt','w+',encoding='GBK') as file:
    file.write(str)
'''