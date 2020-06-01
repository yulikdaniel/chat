import requests
from tkinter import *
import threading as tr
from json import loads, dumps

unrep = "dß/eb5-h29ti3s5pbß.s"


class NameAsk:
    global mname

    def __init__(self, parent):
        self.cnv = Canvas(parent, height=200, width=300)
        self.cnv.pack()

        self.text = self.cnv.create_text(155, 20, text='Enter a username and a password. They have\n' +
                                                       ' to contain exactly one word.')

        self.e = Entry(parent, text='1')
        self.e.pack()
        self.e.insert(0, 'Username')
        self.e2 = Entry(parent)
        self.e2.pack()
        self.e2.insert(0, 'Password')

        Button(parent, text="Login", command=self.ok, width=10, height=10).pack(pady=5, side='right')
        Button(parent, text="Sign Up", command=self.ok2, width=10, height=10).pack(side='left', pady=5)

        self.wnf = False
        parent.bind("<KeyPress>", self.enter)
        self.parent = parent

    def ok2(self):
        global mname
        if len(self.e.get().strip().split()) == 1 and len(self.e2.get().strip().split()):
            name = self.e.get().strip().split()[0]
            password = self.e2.get().strip().split()[0]
            text = requests.get('http://yulikdaniel.pythonanywhere.com/r/{}/{}'.format(name, password)).text
            if text == 'Succesful':
                mname = name
                self.parent.quit()
                self.parent.destroy()
            else:
                if not self.wnf is False:
                    self.cnv.delete(self.wnf)
                self.wnf = self.cnv.create_text(150, 150, text=text)
        else:
            if not self.wnf is False:
                self.cnv.delete(self.wnf)
            self.wnf = self.cnv.create_text(85, 25, text='Wrong name format.')

    def ok(self):
        global mname
        if len(self.e.get().strip().split()) == 1 and len(self.e2.get().strip().split()):
            name = self.e.get().strip().split()[0]
            password = self.e2.get().strip().split()[0]
            text = requests.get('http://yulikdaniel.pythonanywhere.com/n/{}/{}'.format(name, password)).text
            if text == 'Succesful':
                mname = name
                self.parent.quit()
                self.parent.destroy()
            else:
                if not self.wnf is False:
                    self.cnv.delete(self.wnf)
                self.wnf = self.cnv.create_text(150, 150, text=text)
        else:
            if not self.wnf is False:
                self.cnv.delete(self.wnf)
            self.wnf = self.cnv.create_text(85, 25, text='Wrong name format.')

    def enter(self, event):
        if event.keysym == 'Return':
            self.ok()


class MyDialog:
    def __init__(self, parent, name):
        self.name = name

        self.e = Entry(parent)
        self.e.pack(padx=5, pady=25)
        self.parent = parent
        self.last = ['']

        b = Button(parent, text="Send", command=self.ok, width=10, height=10)
        b.pack(pady=5)

        b2 = Button(parent, text="Log out", command=self.refresh, width=10, height=10)
        b2.pack()

        parent.bind("<KeyPress>", self.enter)
        self.cnv = Canvas(self.parent, height=1000, width=1000)
        self.cnv.pack()
        self.text = 'F'
        self.refresh(True)

    def refresh(self, new=False):
        global text1
        text = text1
        if new:
            self.last = loads(requests.get("http://yulikdaniel.pythonanywhere.com/tenlast").text)
            print(len(self.last))
        if self.last[-1] != text:
            self.last.append(text)
            if len(self.last) > 10:
                del self.last[0]
        if self.text == 'F':
            self.var = StringVar()
            self.text = Label(self.cnv, textvariable=self.var, justify='left')
            self.text.pack(side='left')
        self.var.set('\n'.join([x.split(unrep)[-1] for x in self.last]))

    def enter(self, event):
        if event.keysym == 'Return':
            self.ok()

    def ok(self):
        if self.e.get().strip():
            a = self.e.get()[:200]
            self.e.delete(0, END)
            text = requests.get(
                'http://yulikdaniel.pythonanywhere.com/ss/{}'.format(self.name + ': ' + self.mesconv(a))).text
            if text != 'Succesful':
                print('Woops', text)
            self.refresh()

    def mesconv(self, mes):
        return 'symbprocbmys'.join(
            'symbreshmbys'.join('symbslashbmys'.join('symbvoprmbys'.join(mes.split('?')).split('/')).split('#')).split('%'))


def ref():
    global text1, ac
    text1 = requests.get('http://yulikdaniel.pythonanywhere.com/get/').text
    if not ac:
        return
    ref()


ac = True
text1 = ''
mname = None
root = Tk()
d = NameAsk(root)
root.mainloop()

if mname is not None:
    t1 = tr.Thread(target=ref)
    t1.start()
    root2 = Tk()
    root2.title('Dialog')
    d2 = MyDialog(root2, mname)
    try:
        while True:
            root2.update_idletasks()
            root2.update()
            d2.refresh()
    except:
        pass
    finally:
        ac = False
