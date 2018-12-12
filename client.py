import wx
import telnetlib
from time import sleep
# import _thread as thread
from chatbot import baidu_api2, chatbot, tuling, play_mp3, remove_voice, getText
from config import BOT, default_server, VOICE_SWITCH
from recorder import *
import threading


bot_use = BOT


class LoginFrame(wx.Frame):
    """
    登录窗口
    """
    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.serverAddressLabel = wx.StaticText(self, label="Server Address", pos=(15, 40), size=(120, 25))
        self.userNameLabel = wx.StaticText(self, label="UserName", pos=(45, 90), size=(120, 25))
        self.serverAddress = wx.TextCtrl(self, value=default_server,
                                         pos=(120, 37), size=(150, 25), style=wx.TE_PROCESS_ENTER)
        self.userName = wx.TextCtrl(self, pos=(120, 87), size=(150, 25), style=wx.TE_PROCESS_ENTER)
        self.loginButton = wx.Button(self, label='Login', pos=(50, 145), size=(90, 30))
        self.exitButton = wx.Button(self, label='Exit', pos=(180, 145), size=(90, 30))
        # 绑定登录方法
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        # 绑定退出方法
        self.exitButton.Bind(wx.EVT_BUTTON, self.exit)
        # 服务器输入框Tab事件
        self.serverAddress.SetFocus()
        self.Bind(wx.EVT_TEXT_ENTER, self.usn_focus, self.serverAddress)
        # 用户名回车登录
        self.Bind(wx.EVT_TEXT_ENTER, self.login, self.userName)
        self.Show()

    # 回车调到用户名输入栏
    def usn_focus(self, event):
        self.userName.SetFocus()

    def login(self, event):
        # 登录处理
        try:
            serverAddress = self.serverAddress.GetLineText(0).split(':')
            con.open(serverAddress[0], port=int(serverAddress[1]), timeout=10)
            response = con.read_some()
            if response != b'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (200, 100))
                return
            con.write(('login ' + str(self.userName.GetLineText(0)) + '\n').encode("utf-8"))
            response = con.read_some()
            if response == b'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='当前用户：'+str(self.userName.GetLineText(0)), size=(515, 400))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (95, 20))

    def exit(self, event):
        self.Close()

    # 显示错误信息对话框
    def showDialog(self, title, content, size):
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()


class ChatFrame(wx.Frame):
    """
    聊天窗口
    """
    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |
                                                         wx.DEFAULT_FRAME_STYLE)
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos=(5, 5), size=(490, 310), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.sayButton = wx.Button(self, label="Say", pos=(5, 320), size=(58, 25))
        self.message = wx.TextCtrl(self, pos=(65, 320), size=(240, 25), style=wx.TE_PROCESS_ENTER)
        self.sendButton = wx.Button(self, label="Send", pos=(310, 320), size=(58, 25))
        self.usersButton = wx.Button(self, label="Users", pos=(373, 320), size=(58, 25))
        self.closeButton = wx.Button(self, label="Close", pos=(436, 320), size=(58, 25))
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)  # 发送按钮绑定发送消息方法
        self.message.SetFocus()  # 输入框回车焦点
        self.sayButton.Bind(wx.EVT_LEFT_DOWN, self.sayDown)  # SAY按钮按下
        self.sayButton.Bind(wx.EVT_LEFT_UP, self.sayUp)  # Say按钮弹起
        self.Bind(wx.EVT_TEXT_ENTER, self.send, self.message)  # 回车发送消息
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)  # Users按钮绑定获取在线用户数量方法
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)  # 关闭按钮绑定关闭方法
        treceive = threading.Thread(target=self.receive)  # 接收信息线程
        treceive.start()
        # self.ShowFullScreen(True)  # 全屏
        self.Show()

    def sayDown(self, event):
        trecording = threading.Thread(target=recording)
        trecording.start()

    def sayUp(self, event):
        sayText = getText(r"E:\Python_Doc\voice_say\say_voice.wav")
        self.message.AppendText(str(sayText))
        self.send(self)

    def send(self, event):
        # 发送消息
        message = str(self.message.GetLineText(0)).strip()
        global bot_use
        if message != '':
            if message == "chatbot":
                bot_use = "ChatBot"
                self.message.Clear()
                con.write(('noone_say You have been changed ChatBot-Chat' + '\n').encode("utf-8"))
                return
            elif message == "tuling":
                bot_use = "TuLing"
                self.message.Clear()
                con.write(('noone_say You have been changed TuLing-Chat' + '\n').encode("utf-8"))
                return
            elif message == "user":
                bot_use = "User"
                self.message.Clear()
                con.write(('noone_say You have been changed User-Chat' + '\n').encode("utf-8"))
                return
            con.write(('say ' + message + '\n').encode("utf-8"))
            self.message.Clear()
            # 机器人回复
            if bot_use == "ChatBot":
                answer = chatbot(message)
                con.write(('chatbot_say ' + answer + '\n').encode("utf-8"))
            elif bot_use == "TuLing":
                answer = tuling(message)
                con.write(('tuling_say ' + answer + '\n').encode("utf-8"))
            elif bot_use == "User":
                return

            if VOICE_SWITCH:
                # 写本地音乐文件
                baidu_api2(answer)
                # 新建线程播放音乐
                tplay_mp3 = threading.Thread(target=play_mp3)
                tplay_mp3.start()
                # thread.start_new_thread(play_mp3, ())
        return

    def lookUsers(self, event):
        # 查看当前在线用户
        con.write(b'look\n')

    def close(self, event):
        # 关闭窗口
        tremove_voice = threading.Thread(target=remove_voice)
        tremove_voice.start()
        # thread.start_new_thread(remove_voice, ())
        con.write(b'logout\n')
        con.close()
        self.Close()

    def receive(self):
        # 接受服务器的消息
        while True:
            sleep(1)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)

    def saytime(self):
        i = 0
        while True:
            self.chatFrame.AppendText('正在录音...' + str(i) + '秒\n')
            sleep(1)
            i = i + 1


if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title="Login", size=(320, 250))
    app.MainLoop()
