from Tkinter import *
import os
import auto_xshell

def HostFilter(host):
    
    nums = host.strip().split(".")
    n = len(nums) 
    if n != 4:
        return ""

    for i in range(n):
        try:
            tmp = int(nums[i])
        except:
            return ""

        if tmp < 0 or tmp > 255:
            return ""
        nums[i] = str(tmp)
    
    return ".".join(nums)

def FileFilter(filepath = "", filename = "Xshell.exe"):
    if os.path.isfile(filepath) and os.path.basename(filename) == filename:
        return filepath

    if os.path.isdir(filepath) and filename in os.listdir(filepath):
        return os.path.join(filepath, filename)

    return ""


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, width = 50, height = 50)
        self.pack()


        self.CheckbarList = []
        self.HostSet = set()
        self.row = 1        
        
        self.entrythingy = Entry(self, width = 50)
        self.entrythingy.grid(row=0, column=0)

        self.contents = StringVar()
        self.contents.set(r"C:\Program Files (x86)\NetSarang\Xshell 5\Xshell.exe")
        
        self.button_add = Button(self, text = "Add Host", command=self.addhost)
        #self.button_add.grid(row=0, column=1)
        

        self.button_open_text = StringVar()
        self.button_open_text.set('Set Path')
        self.button_open = Button(self, textvariable = self.button_open_text, command=self.getinfo)
        self.button_open.grid(row=0, column=2)
        
        self.entrythingy.config(textvariable = self.contents)
        self.entrythingy.bind('<Key-Return>', self.addhost)
        
    def addhost(self, event = None, clear = False):

        host = HostFilter(self.contents.get())
        if clear:
            self.contents.set("")

        if host != "":
            if host in self.HostSet:
                print "  Host Exist."
                return

            var = IntVar()
            var.set(1)
            self.checkbtn = Checkbutton(root, text=host, variable=var)
            self.checkbtn.grid(row=self.row, sticky = W); self.row += 1            
            
            self.CheckbarList.append({"host":host, "var":var})
            self.HostSet.add(host)
        else:
            print "  Host Error."
    
    def getinfo(self, debug = False):
        if self.button_open_text.get() == 'Set Path':
            self.command = FileFilter(self.contents.get())
            if self.command == "":
                print "  CmdPath Error."
            else:
                self.contents.set("192.168.0.199")                
                self.button_open_text.set('Start')
                self.button_add.grid(row=0, column=1)
                print "CMD:", self.command
        else:            
            HostList = [ node["host"] for node in self.CheckbarList if node["var"].get() == 1 ]
            print HostList

            for host in HostList:
                try:
                    auto_xshell.main(host, self.command) 
                except:
                    pass
                


if __name__ == '__main__':
    root = App()
    root.master.title("Auto Xshell")
    root.mainloop()