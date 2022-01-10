from tkinter import *
import socket
import threading
from queue import Queue



hostname = socket.gethostname()
myIP = socket.gethostbyname(hostname)
scanID = "10.200.124.1"
#"10.200.124.1"
#"10.200.124.227"

q = Queue()
def scanner(port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((scanID, port))
        soc.close()
        return True
    except:
        return False

openPortList = []
closedPortList = []

def PortScanner():
    while not q.empty():
        port = q.get()

        if(scanner(port)):
            openPortList.append(port)
            #print("open port {}".format(port))
        else:
            closedPortList.append(port)
            #print("close port {}".format(port))

threadList = []
def finalCall():
    for t in range(1500):
        thread = threading.Thread(target=PortScanner)
        threadList.append(thread)
    for thread in threadList:
        thread.start()
    for thread in threadList:
        thread.join()



def getval():
    ip = ipvalue.get()
    global scanID
    if(ip.lower() != 'na'):
        scanID = ip
    bport = int(startvalue.get())
    lport = int(endvalue.get())


    portList = range(bport, lport + 1)
    for port in portList:
        q.put(port)

    print(bport)
    print(lport)


    finalCall()
    buttontext.set("Done!")
    printTextBox()


# GUI

root = Tk()

#gui logic
root.geometry("1400x900")
#root.maxsize(1200,900)
root.minsize(900,900)
root.title("Port Scanner")


startvalue = StringVar()
endvalue = StringVar()
ipvalue = StringVar()

sportentry = Entry(root,textvariable=startvalue,bg="#e3f3fa")
lportentry = Entry(root,textvariable=endvalue,bg="#e3f3fa")
ipentry = Entry(root,textvariable=ipvalue,bg="#e3f3fa")

Label(text="Port Scanner",font="lucid 36 bold",padx=20,pady=3,bg="#5ea1bf",borderwidth=1,relief=SUNKEN).pack(fill=X)


Label(text="Do you want to use any other system's address?(NA/IP)",font="Helvetica 18 italic",bg="#73c2e6",pady=15).pack(pady=5)
ipentry.pack(pady=6)

Label(root,text="Start From:",font="Helvetica 18 italic",bg="#73c2e6",pady=8).pack(pady=10)
sportentry.pack(pady=6)

Label(root,text="End At:",font="Helvetica 18 italic",bg="#73c2e6",pady=8).pack(pady=10)
lportentry.pack(pady=6)

buttontext = StringVar()
b1 = Button(textvariable=buttontext,command=getval,font="Raleway",bg="#78caf0",fg="white",height=2,width=10,borderwidth=3,relief=SUNKEN)
buttontext.set("Submit")
b1.pack(pady=10)

Label(text="List of open ports:",font="Helvetica 18 bold",pady=15,bg="#cae0eb").pack(fill=X)
text_box = Text(root, height=10, width=85, padx=15, pady=15, font="Courier 16 italic",bg="#e9f3f7")
text_box.pack(fill=X)

def printTextBox():
    openPortList.sort()
    openportstring ="Address:"+scanID+"\n"
    if len(openPortList) == 0:
        openportstring = "No ports are open in the system with address "+str(scanID)
    else:
        for oport in openPortList:
            openportstring += str(oport)+" "
            print("port {} is open".format(oport))

    closedPortList.sort()
    for cport in closedPortList:
        print("port {} is close".format(cport))

    text_box.insert(1.0, openportstring)


root.mainloop()
