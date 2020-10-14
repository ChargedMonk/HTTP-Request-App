import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext as st
from requestHandler import Request
import json
import json2table
from collections import OrderedDict
import pyperclip as pc
import os
import os.path
from os import path
from html5print import HTMLBeautifier as hb
import webbrowser


def errBox(s):
    messagebox.showinfo("Message",s)
    ntbk.select(0)

def wrMem(url,time,req,pay,respH,code="NA"):
    un = "*/^~%~^/*"
    f = open("History.txt","a")
    if re.search('[a-zA-Z]', req): pass
    else:
        req = "NONE"
    if re.search('[a-zA-Z]', pay): pass
    else:
        pay = "NONE"
    wr = time+un+url+un+req.replace("\n","{w2e3?w2e3}")+un+pay.replace("\n","{w2e3?w2e3}")+un+str(code)+un
    for k,v in respH.items():
        wr = wr + k+"^~"+v+"[^!`]"
    f.write(wr+"\n")
    f.close()
    f = open("time.txt","a")
    f.write(time+"~/@/~" + url + "\n")
    f.close()

def readMem(time):
    un = "*/^~%~^/*"
    f = open("History.txt")
    for x in f:
        if time in x:
            # print("%%% x =",x)
            time,url,req,pay,code,respH =  x.split(un)
            break
    f.close()
    respH = respH[:-6].split("[^!`]")
    od = OrderedDict()
    for i in respH:
        x,y = i.split("^~")
        od[x] = y
    return(time,url,req.replace("{w2e3?w2e3}","\n").replace(":","  :  "),pay.replace("{w2e3?w2e3}","\n").replace(":","  :  "),int(code),od)

def updateHistory():
    win1(".!notebook.!frame2")

def win1(event):

    def delH():
        try:
            os.remove("History.txt")
            os.remove("time.txt")
            ntbk.select(0)

        except:
            errBox("History already empty!")

    def delsp():
        tx = requestOptionsH.get()
        with open("time.txt") as f:
            s = list(f.read().split("\n"))
            for x in range(len(s)):
                if tx in s[x]:
                    s[x] = ""
        os.remove("time.txt")
        s = '\n'.join(s)
        if re.search("[A-Za-z]",s):
            pass
        else:
            os.remove("History.txt")
            # window1.destroy()
            errBox("History empty!")
            return
        with open("time.txt","w+") as f:
            f.write(s)

        updateHistory()

    # def updatedrpdwn(tx):
    #     # print("%% tx =",tx,"type =",type(tx))
    #     if tx in optionsH:
    #         print("%% removed tx")
    #         optionsH.remove(tx)
    #         requestOptionsH['values'] = optionsH
    #         requestOptions.current(0)
    #         urlBoxH.delete("1.0",tk.END)
    #         responseStatusCodeLabelH.config(text="Response code: NA",bg="orange")
    #         headerTreeH.delete(*headerTreeH.get_children())


    def rspBody():
        tx = requestOptionsH.get()
        time,url,req,pay,code,respH = readMem(tx)
        try :
            ty = respH["Content-Type"]
        except:
            try:
                ty = respH["content-type"]
            except:
                errBox("Cannot find content type")
                return
        tx = "resp" + tx.replace(" ","_").replace(":","")
        if "text" in ty:
            try:
                with open("{0}.txt".format(tx),encoding='utf-8') as f:
                    ret = f.read()
                    f1 = open("{0}.html".format(tx),"w+",encoding = 'utf-8')
                    f1.write(ret)
                    webbrowser.open('file://' + os.path.realpath("{0}.txt".format(tx)))
                    webbrowser.open('file://' + os.path.realpath("{0}.html".format(tx)))
            except Exception as e:
                print(e)
                errBox("File lost, please send request again")   
        elif "json" in ty:
            webbrowser.open('file://' + os.path.realpath("{0}.html".format(tx)))

                
    def copyclp():
        tx = requestOptionsH.get()
        time,url,req,pay,status_codeH,respH = readMem(tx)
        s = "{"
        for k,v in respH.items():
            s = s + "\n" + k + ":" + v
        s = s+ "\n}"
        pc.copy(s)
        cmplt.config(text="Copied!")

    def downl():
        tx = requestOptionsH.get()
        time,url,req,pay,status_codeH,respH = readMem(tx)
        time = time.replace(" ","_")
        time = time.replace(":","")
        s = "{"
        with open("{0}.txt".format(time),"w") as f:
            for k,v in respH.items():
                s = s + "\n" + k + ":" + v
            s = s+ "\n}"
            f.write(s)
        cmplt.config(text="Downloaded!")

    def update(event):
        tx = requestOptionsH.get()
        time,url,req,pay,status_codeH,respH = readMem(tx)
        cmplt.config(text="")
        urlBoxH.delete("1.0", tk.END)
        urlBoxH.insert(tk.END,url)
        headerBoxH.delete("1.0", tk.END)
        headerBoxH.insert(tk.END,req)
        payloadBoxH.delete("1.0", tk.END)
        payloadBoxH.insert(tk.END,pay)
        if status_codeH == 200:
            responseStatusCodeLabelH.config(text="Response code: "+ str(status_codeH),bg="#58D68D")
        elif status_codeH >= 400:
            responseStatusCodeLabelH.config(text="Response code: "+ str(status_codeH),bg="#EC7063")
        else:
            responseStatusCodeLabelH.config(text="Response code: "+ str(status_codeH),bg="#F4D03F")
        maketableH(respH)

    def maketableH(respHeadersH):
        headerTreeH.delete(*headerTreeH.get_children())
        # print("\n\nkeys=",respHeaders.keys(),"\n\nvals=",respHeaders.values(),"\n\n")
        tg = 'odd'
        for k,v in respHeadersH.items():
            headerTreeH.insert("",'end',values =(f"{k}",f"{v}"),tag=(tg,))
            if tg == 'odd':
                tg = 'even'
            else:
                tg = 'odd'

        headerTreeH.tag_configure('odd', background='#ECF0F1')
        headerTreeH.tag_configure('even', background='#D0D3D4')

    if event == ".!notebook.!frame2" or event.widget.select() == ".!notebook.!frame2":
        pass
    else:
        return
    for child in window1.winfo_children():
        child.destroy()
    if(path.isfile("time.txt")):
        pass
    else:
        errBox("History empty!")
        return

    historyLabel = Label(window1,text="History",font="Arial 20 bold")
    historyLabel.place(x=600,y=10)
    # Request options
    f = open("time.txt")
    optionsH = [i.split("~/@/~")[0] for i in f.read().split("\n") if len(i)>0]
    # print("%%% options =",optionsH,"\nlen =",len(optionsH))
    requestOptionsH = ttk.Combobox(window1,value=optionsH,width=22,font="Arial 11")
    # requestOptions.current(0)
    requestOptionsH.place(x=50,y=100)
    requestOptionsH.bind("<<ComboboxSelected>>",update)
    # URL box
    urlBoxH = Text(window1,width=110,height = 1,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12")
    urlBoxH.place(x=300,y=100)
    # urlBox.bind("<Return>",sendRequest)

    # Header box
    headerLabelH = Label(window1,text="Headers:\n(in JSON)",font="Arial 12")
    headerLabelH.place(x=70,y=160)
    headerBoxH = Text(window1,width=50,height=8,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12")
    headerBoxH.place(x=150,y=160)
    headerBoxH.insert(tk.END,"{\n\n\n\n\n\n}")
    # headerBox.insert(tk.END,"}")

    # Payload box
    payloadLabelH = Label(window1,text="Payload:\n(in JSON)",font="Arial 12")
    payloadLabelH.place(x=670,y=160)
    payloadBoxH = Text(window1,width=50,height=8,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12")
    payloadBoxH.place(x=750,y=160)
    payloadBoxH.insert(tk.END,"{\n\n\n\n\n\n}")
    # payloadBox.insert(tk.END,"}")

    # Download button
    dlButton = Button(window1,text="Download",command=downl,width=14,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
    # sendButton.bind("<Button-1>",sendRequest)
    dlButton.place(x=1180,y=400)

    #CopyToClipButton
    ctButton = Button(window1,text="Clipboard",command=copyclp,width=14,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
    ctButton.place(x=1180,y=450)

    #Delete specific history
    spButton = Button(window1,text="Delete instance",command=delsp,width=14,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
    spButton.place(x=1180,y=500)

    # Delete All History
    delButton = Button(window1,text="Delete History",command=delH,width=14,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
    delButton.place(x=1180,y=550)

    #View response body (text)
    vwtButton = Button(window1,text="Response Body",command=rspBody,width=14,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
    vwtButton.place(x=70,y=450)

    # Completed label
    cmplt = Label(window1,text="",font="Arial 15 bold",fg="#212F3C",bg="white",width=14)
    cmplt.place(x=1170,y=610)
    # Response box
    responseStatusCodeLabelH = Label(window1,text="Response Code: NA",font="Arial 15 bold",relief="raised",bg="orange",fg="black")
    responseStatusCodeLabelH.place(x=575,y=340)
    responseHeaderBoxLabelH = Label(window1,text="Response Headers:",font="Arial 12")
    responseHeaderBoxLabelH.place(x=70,y=400)


    # constructing frame for easy placement
    f1 = Frame(window1)
    f1.place(x=320,y=400)

    # Constructing vertical scrollbar
    # with treeview
    verscrlbarH = ttk.Scrollbar(f1,orient="vertical")
    verscrlbarH.grid(row=0,column=1,sticky="NSEW")
    # verscrlbar.place(x=850,y=270)
    # Constructing horizontal scrollbar
    # with treeview
    horscrlbarH = ttk.Scrollbar(f1,orient="horizontal")
    horscrlbarH.grid(row=1,column=0,sticky="EWNS")


    # styleH = ttk.Style()
    # #   style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
    # styleH.configure("mystyle.Treeview",font=('Calibri', 12),rowheight=20) # Modify the font of the body
    # styleH.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
    # style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
    # Using treeview widget
    headerTreeH = ttk.Treeview(f1, selectmode ='browse',xscrollcommand=horscrlbarH.set,yscrollcommand=verscrlbarH.set,style="mystyle.Treeview")
    # Remove the borders

    # Calling pack method w.r.to treeview
    # headerTree.place(x=150,y=270)
    headerTreeH.grid(row=0,column=0)
    verscrlbarH.config(command=headerTreeH.yview)
    horscrlbarH.config(command=headerTreeH.xview)
    # Configuring treeview
    # headerTree.configure(yscrollcommand = horscrlbar.set)

    # Defining number of columns
    headerTreeH["columns"] = ("1", "2")

    # Defining heading
    headerTreeH['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    headerTreeH.column("1", width = 200,minwidth=250,stretch=True, anchor ='nw')
    headerTreeH.column("2", width = 600, minwidth=3000,stretch=True, anchor ='nw')
    # style.configure("Treeview.Column", font=("Arial", 15,"bold"))

    # Assigning the heading names to the
    # respective columns
    headerTreeH.heading("1", text ="Key", anchor="nw")
    headerTreeH.heading("2", text ="Value", anchor="nw")

    # window1.mainloop()




###################################################
#               Request Funcs                     #
###################################################

def maketable(respHeaders):
    headerTree.delete(*headerTree.get_children())
    # print("\n\nkeys=",respHeaders.keys(),"\n\nvals=",respHeaders.values(),"\n\n")
    tg = 'odd'
    for k,v in respHeaders.items():
        headerTree.insert("",'end',values =(f"{k}",f"{v}"),tag=(tg,))
        if tg == 'odd':
            tg = 'even'
        else:
            tg = 'odd'

    headerTree.tag_configure('odd', background='#ECF0F1')
    headerTree.tag_configure('even', background='#D0D3D4')

def sendRequest():
    req = Request(urlBox.get())
    requestType = requestOptions.get()
    headers = headerBox.get("1.0","end-1c")
    try:
        if headers:
            headers = eval(headers)
        else:
            headers = {}

    except Exception as e:
        responseStatusCodeLabel.config(text="Response Code: NA",bg="orange")
        errBox("Invalid Header !")
        headerTree.delete(*headerTree.get_children())
        print("\n\n\n###Error: Headers are in wrong format\n"+str(e))
        return

    payload = payloadBox.get("1.0","end-1c")
    try:
        if payload:
            payload = eval(payload)
        else:
            payload = {}
    except Exception as e:
        responseStatusCodeLabel.config(text="Response Code: NA",bg="orange")
        errBox("Invalid Payload !")
        headerTree.delete(*headerTree.get_children())
        print("\n\n\n###Error: Payload is in wrong format\n"+str(e))
        return

    try:
        status_code,responseHeaders,respbody = req.sndreq(reqtype=requestType,headers=headers,payload=payload)
        # print(req.sndreq(reqtype=requestType,headers=headers,payload=payload))
        if status_code == 200:
            responseStatusCodeLabel.config(text="Response code: "+ str(status_code),bg="#58D68D")
        elif status_code >= 400:
            responseStatusCodeLabel.config(text="Response code: "+ str(status_code),bg="#EC7063")
        else:
            responseStatusCodeLabel.config(text="Response code: "+ str(status_code),bg="#F4D03F")
        maketable(dict(responseHeaders))
        wrMem(urlBox.get(),responseHeaders["Date"],headerBox.get("1.0","end-1c"),payloadBox.get("1.0","end-1c"),responseHeaders,status_code)
        try:
            ty = responseHeaders["Content-Type"]
        except:
            try:
                ty = responseHeaders["content-type"]
            except:
                errBox("No content type found")
        dt = responseHeaders["Date"]
        dt = dt.replace(" ","_")
        dt = dt.replace(":","")
        if "text" in ty:
            with open("resp{0}.txt".format(dt),"w+",encoding="utf-8") as f:
                try:
                    f.write(hb.beautify(respbody, 4))
                except:
                    f.write(respbody)
        elif "JSON" in ty:
            with open("resp{0}.html".format(dt),"w+",encoding = 'utf-8') as f:
                build_direction = "LEFT_TO_RIGHT"
                table_attributes = {"style": "width:100%"}
                f.write(json2table.convert(respbody, 
                         build_direction=build_direction, 
                         table_attributes=table_attributes))
    except Exception as e:
        responseStatusCodeLabel.config(text="Response code: ERROR",bg="red")
        headerTree.delete(*headerTree.get_children())
        print("\n\n####: Invalid request\n"+str(e))

def insertHeader():
    k = keyEntryH.get()
    v = valEntryH.get()
    if len(k)<1 or len(v) <1:
        responseStatusCodeLabel.config(text="Response Code: NA",bg="orange")
        errBox("Invalid Header Entry!")
        return
    try:
        # print("%%% headerBox.get =",headerBox.get("1.0","end-1c").replace('\n',''))
        headerBoxContent = headerBox.get("1.0","end-1c").replace('\n','')
        if len(headerBoxContent) < 1:
            headerDict = {}
        else:
            headerDict = eval(headerBoxContent)
    except Exception as e:
        responseStatusCodeLabel.config(text="Response Code: NA",bg="orange")
        print("Invalid headers\n"+str(e))
        errBox("Invalid Headers!")
        return
    # print("%% headerDict =",headerDict)
    headerDict[k] = v
    headerStr = str(headerDict)
    headerStr = headerStr.replace('{','{\n').replace(":","  :  ").replace('}','\n}').replace('\',','\',\n')
    # headerStr = headerStr.replace('}','\n}')
    # headerStr = headerStr.replace('\',','\',\n')
    # print("%% headerStr =",headerStr)
    headerBox.delete("1.0",tk.END)
    headerBox.insert(tk.END,headerStr)
    keyEntryH.delete(0,tk.END)
    keyEntryH.insert(tk.END,"Key")
    keyEntryH.config(fg="#5D6D7E")
    valEntryH.delete(0,tk.END)
    valEntryH.insert(tk.END,"Value")
    valEntryH.config(fg="#5D6D7E")

def insertPayload():
    k = keyEntryP.get()
    v = valEntryP.get()
    if len(k)<1 or len(v) <1:
        responseStatusCodeLabel.config(text="Response Code: NA",bg="orange")
        errBox("Invalid Payload Entry!")
        return
    try:
        payloadBoxContent = payloadBox.get("1.0","end-1c").replace('\n','')
        if len(payloadBoxContent) < 1:
            payloadDict = {}
        else:
            payloadDict = eval(payloadBoxContent)
    except Exception as e:
        responseStatusCodeLabel.config(text="Response Code: NA",bg="orange")
        print("Invalid Payload\n"+str(e))
        errBox("Invalid Payload!")
        return
    payloadDict[k] = v
    payloadStr = str(payloadDict)
    payloadStr = payloadStr.replace('{','{\n').replace(":","  :  ").replace('}','\n}').replace('\',','\',\n')
    # payloadStr = payloadStr.replace('}','\n}')
    # payloadStr = payloadStr.replace('\',','\',\n')
    print("%% payloadStr =",payloadStr)
    payloadBox.delete("1.0",tk.END)
    payloadBox.insert(tk.END,payloadStr)
    keyEntryP.delete(0,tk.END)
    keyEntryP.insert(tk.END,"Key")
    keyEntryP.config(fg="#5D6D7E")
    valEntryP.delete(0,tk.END)
    valEntryP.insert(tk.END,"Value")
    valEntryP.config(fg="#5D6D7E")

def clearHeader():
    headerBox.delete("1.0",tk.END)

def clearPayload():
    payloadBox.delete("1.0",tk.END)

def clearHint(event):
    event.widget.delete(0,tk.END)
    event.widget.config(fg="black")

root = Tk()
root.title("App")
root.geometry("1366x768")
root.configure(background="white")

s = ttk.Style()
s.configure('TNotebook.Tab', font=('Arial','15') )

ntbk = ttk.Notebook(root)
ntbk.pack()

window = Frame(ntbk,width=1366,height=768,bg="white")
window1 = Frame(ntbk,width=1366,height=768,bg="white")

ntbk.bind("<<NotebookTabChanged>>",win1)
ntbk.add(window,text="Request")
ntbk.add(window1,text="History")


headingLabel = Label(window,text="HTTP Request App",font="Arial 20 bold")
headingLabel.place(x=550,y=10)
# Request options
options = ['GET','POST','PUT','OPTIONS','HEAD','PATCH','DELETE']
requestOptions = ttk.Combobox(window,value=options,width=10,font="Arial 11")
requestOptions.current(0)
requestOptions.place(x=50,y=100)
# requestOptions.configure()

# URL box
urlBox = Entry(window,width=110,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12")
urlBox.place(x=160,y=100)
# urlBox.bind("<Return>",sendRequest)
urlBox.focus_set()

# Send button
sendButton = Button(window,text="Send",command=sendRequest,width=10,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
sendButton.place(x=1180,y=95)
# sendButton.bind("<Button-1>",sendRequest)

defaultHeaders = "{\n'Accept-Language'  :  'en;q=0.5, *;q=0.5',\n'Content-Type'  :  'application/json',\n'Max-Forwards'  :  '10',\n'Pragma'  :  'no-cache',\n'Accept-Charset'  :  'utf-8',\n'Cache-Control'  :  'no-cache',\n'Accept'  :  '*/*',\n'Accept-Encoding'  :  'gzip, deflate, br',\n'Connection'  :  'keep-alive'\n}"

# Header box
headerLabel = Label(window,text="Headers:",font="Arial 12")
headerLabel.place(x=30,y=160)
keyEntryH = Entry(window,width=18,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 10",fg="#5D6D7E")
keyEntryH.place(x=110,y=160)
keyEntryH.insert(tk.END,"Key")
valEntryH = Entry(window,width=33,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 10",fg="#5D6D7E")
valEntryH.place(x=260,y=160)
valEntryH.insert(tk.END,"Value")
keyEntryH.bind("<Button-1>",clearHint)
valEntryH.bind("<Button-1>",clearHint)
insertH = Button(window,text="Insert",command=insertHeader,width=7,bg="orange",fg="black",relief="raised",font="Arial 10 bold")
insertH.place(x=510,y=155)
clearH = Button(window,text="Clear all",command=clearHeader,width=7,bg="orange",fg="black",relief="raised",font="Arial 10 bold")
clearH.place(x=580,y=155)
headerBox = Text(window,width=60,height=8,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12")
headerBox.place(x=110,y=190)
headerBox.insert(tk.END,defaultHeaders)

# Payload box
payloadLabel = Label(window,text="Payload:",font="Arial 12")
payloadLabel.place(x=670,y=160)
keyEntryP = Entry(window,width=18,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 10",fg="#5D6D7E")
keyEntryP.place(x=750,y=160)
keyEntryP.insert(tk.END,"Key")
valEntryP = Entry(window,width=33,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 10",fg="#5D6D7E")
valEntryP.place(x=900,y=160)
valEntryP.insert(tk.END,"Value")
keyEntryP.bind("<Button-1>",clearHint)
valEntryP.bind("<Button-1>",clearHint)
insertP = Button(window,text="Insert",command=insertPayload,width=6,bg="orange",fg="black",relief="raised",font="Arial 10 bold")
insertP.place(x=1150,y=155)
clearP = Button(window,text="Clear all",command=clearPayload,width=7,bg="orange",fg="black",relief="raised",font="Arial 10 bold")
clearP.place(x=1220,y=155)
payloadBox = Text(window,width=60,height=8,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12")
payloadBox.place(x=750,y=190)
payloadBox.insert(tk.END,"{\n\n\n\n}")

# Response box
responseStatusCodeLabel = Label(window,text="Response Code: NA",font="Arial 15 bold",relief="raised",bg="orange",fg="black",width=18)
responseStatusCodeLabel.place(x=575,y=350)
responseHeaderBoxLabel = Label(window,text="Response Headers:",font="Arial 12")
responseHeaderBoxLabel.place(x=70,y=400)


# constructing frame for easy placement
f2 = Frame(window)
f2.place(x=320,y=400)

# Constructing vertical scrollbar
# with treeview
verscrlbar = ttk.Scrollbar(f2,orient="vertical")
verscrlbar.grid(row=0,column=1,sticky="NSEW")
# verscrlbar.place(x=850,y=270)
# Constructing horizontal scrollbar
# with treeview
horscrlbar = ttk.Scrollbar(f2,orient="horizontal")
horscrlbar.grid(row=1,column=0,sticky="EWNS")


style = ttk.Style()
# style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
style.configure("mystyle.Treeview",font=('Calibri', 12),rowheight=20) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
# style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
# Using treeview widget
headerTree = ttk.Treeview(f2, selectmode ='browse',xscrollcommand=horscrlbar.set,yscrollcommand=verscrlbar.set,style="mystyle.Treeview")
# Remove the borders

# Calling pack method w.r.to treeview
# headerTree.place(x=150,y=270)
headerTree.grid(row=0,column=0)
verscrlbar.config(command=headerTree.yview)
horscrlbar.config(command=headerTree.xview)
# Configuring treeview
# headerTree.configure(yscrollcommand = horscrlbar.set)

# Defining number of columns
headerTree["columns"] = ("1", "2")

# Defining heading
headerTree['show'] = 'headings'

# Assigning the width and anchor to  the
# respective columns
headerTree.column("1", width = 200,minwidth=250,stretch=True, anchor ='nw')
headerTree.column("2", width = 600, minwidth=3000,stretch=True, anchor ='nw')
# style.configure("Treeview.Column", font=("Arial", 15,"bold"))

# Assigning the heading names to the
# respective columns
headerTree.heading("1", text ="Key", anchor="nw")
headerTree.heading("2", text ="Value", anchor="nw")


root.mainloop()
