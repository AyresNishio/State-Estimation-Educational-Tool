import wx
import wx.html2

import threading

from main import runServer

class MyBrowser(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetTitle('Ferramenta de Aprendizado da Estimação de Estado')
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((1024, 768))

def UIthread(address):
    app = wx.App()
    dialog = MyBrowser(None, -1)
    dialog.browser.LoadURL(address)
    dialog.Show()
    app.MainLoop()

if __name__ == "__main__":
    th = threading.Thread(target=runServer)
    th.daemon = True
    th.start()
    UIthread("http://127.0.0.1:8050")