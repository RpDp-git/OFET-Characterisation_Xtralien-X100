from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import filedialog
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import xtralien as xt
import numpy as np



main=tk.Tk()
main.title("Xtralein IV")
main.geometry("900x680+552+217")
global data_out
data_out=[]


def set_com_port():
    COM=xt.serial_ports()
    
    if COM==[]:
        return ""
    else :
        
        return COM[0]

def transfer():
    if transferchara.get()==1:
        Entry1.configure(state=tk.NORMAL)
        Entry2.configure(state=tk.DISABLED)
        Entry3.configure(state=tk.DISABLED)
        Entry4.configure(state=tk.DISABLED)
    elif transferchara.get()==0:
        Entry1.configure(state=tk.DISABLED)
        Entry2.configure(state=tk.NORMAL)
        Entry3.configure(state=tk.NORMAL)
        Entry4.configure(state=tk.NORMAL)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def only_numbers(char):
    if is_float(char) and float(char)>-10 and float(char)<10:
        return True
    else:
        return False

def init_values():
    Scale1.set(2)
    Scale2.set(3)
    Scale3.set(3)
    Scale4.set(2)
    Scale5.set(3)
    Scale6.set(3)
    unsafe.set(0)
    vs_start.set(0)
    vs_end.set(5)
    vs_step.set(1)
    vg_start.set(0)
    vg_end.set(5)
    vg_step.set(1)
import time

def main1(COM):
    if vs_step.get()==0:
        vs_step.set(1)
    if vg_step.get()==0:
        vg_step.set(1)
        
    vstart=vs_start.get()
    vend=vs_end.get()
    vstep=vs_step.get()
    vgstart=vg_start.get()
    vgend=vg_end.get()
    vgstep=vg_step.get()
    
        
    vnum=(((vend-vstart)//vstep) + 1)
    vnum2=(((vgend-vgstart)//vgstep) + 1)
    
    volts_sd = np.linspace(vstart,vend,vnum)
    volts_g = np.linspace(vgstart,vgend,vnum2)
    fin=np.empty((int(vnum),0))
    header=""
    
    with xt.X100.USB(COM) as Dev1: #Connect to the Device via USB
        for i in volts_g:
            v_g=Dev1['SMU2'].oneshot(i)[0]
            results = np.vstack([Dev1['SMU1'].oneshot(v) for v in volts_sd]) #Create array of oneshots
            fin=np.append(fin,results,axis=1)
            header+=("V,I(V_g={}),".format(v_g[0]))
    return fin,header

def plot_1(data):
    plt.clf()
    
    fig = plt.Figure(figsize=(6.5,4.5), dpi=100)
    ax=fig.add_subplot(111)
    ax.grid()
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    for i in range(0,np.shape(data)[1],2):
        ax.plot(data[:,i],data[:,i+1])
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (A)')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.011, rely=0.294)

def main2(COM):
    if vg_step.get()==0:
        vg_step.set(1)
    vgstart=vg_start.get()
    vgend=vg_end.get()
    vgstep=vg_step.get()
    vnum2=(((vgend-vgstart)//vgstep) + 1)
    volts_g = np.linspace(vgstart,vgend,vnum2)
    v_transf=v_transfer.get()
    with xt.X100.USB(COM) as Dev1:
        Dev1['SMU1'].oneshot(v_transf)[0]
        results = np.vstack([Dev1['SMU2'].oneshot(v) for v in volts_g])
    global data_out
    data_out=results
    Button1.configure(state=tk.NORMAL)
    plot_1(results)
    

def about():
    messagebox.showinfo("About", "Author: Ravi Pradip\nVersion 1.0")
    

def plot_click():
    COM=COMp.get()
    try:
        settings(COM)
        if transferchara.get():
            main2(COM)
        else:
            global data_out
            data_out,width=main1(COM)
            Button1.configure(state=tk.NORMAL)
            plot_1(data_out)
    except:
        messagebox.showerror("Error", "Something went Wrong. Check if the device is connected and the right COM port is specified")
    
def savefile():
    formats = [('Comma Separated values', '*.csv'), ]
    file_name = filedialog.asksaveasfilename(filetypes=formats, title="Save as...",defaultextension = 'csv')
    np.savetxt(file_name,data_out,delimiter=",",fmt="%0.{}E".format(Scale3.get()))
    
def settings(COM):
    with xt.X100.USB(COM) as Dev1: # Connect to the Device via USB
        Dev1.cloi.set.precision(Scale3.get(), response=False) # Set Precision for both SMUs
        Dev1.smu1.set.range(Scale1.get(), response=False) # Set SMU1 range
        Dev1.smu1.set.osr(Scale2.get(), response=False) # Set SMU1 OSR
        Dev1.smu1.set.unsafe(unsafe.get(), response=False) # Set SMU1 unsafe
        Dev1.smu2.set.range(Scale4.get(), response=False) # Set SMU2 range
        Dev1.smu2.set.osr(Scale5.get(), response=False) # Set SMU2 OSR
        Dev1.smu2.set.unsafe(unsafe.get(), response=False) # Set SMU2 unsafe
        Scale6.set(Scale3.get())
##All Labels
Label1=tk.Label(text='''Device :''')
Label1.place(relx=0.022, rely=0.015, height=26, width=58)

Label2 = tk.Label()
Label2.place(relx=0.794, rely=0.074, height=26, width=154)
Label2.configure(text='''SMU 1 > Source-Drain''')

Label3 = tk.Label()
Label3.place(relx=0.022, rely=0.074, height=26, width=66)
Label3.configure(text='''Settings :''')

Label4 = tk.Label()
Label4.place(relx=0.211, rely=0.059, height=26, width=49)
Label4.configure(text='''SMU 1''')

Label5 = tk.Label()
Label5.place(relx=0.528, rely=0.059, height=26, width=49)
Label5.configure(text='''SMU 2''')

Label6 = tk.Label( )
Label6.place(relx=0.828, rely=0.103, height=26, width=98)
Label6.configure(text='''SMU 2 > Gate''')

TSeparator3 = ttk.Separator( )
TSeparator3.place(relx=0.867, rely=0.338, relheight=0.309)
TSeparator3.configure(orient="vertical")

Label7 = tk.Label( )
Label7.place(relx=0.2, rely=0.015, height=26, width=98)
Label7.configure(text='''Status : Active''')

Label8 = tk.Label( )
Label8.configure(text='''V''')
Label8.place(relx=0.9, rely=0.779, height=26, width=15)

Label9 = tk.Label( )
Label9.place(relx=0.756, rely=0.338, height=26, width=74)
Label9.configure(width=74)

Label10 = tk.Label( )
Label10.place(relx=0.756, rely=0.426, height=26, width=73)
Label10.configure(text='''Vend (V)''')
Label10.configure(width=73)

Label11 = tk.Label( )
Label11.place(relx=0.772, rely=0.515, height=26, width=47)
Label11.configure(text='''Vstep''')

Label9 = tk.Label()
Label9.place(relx=0.756, rely=0.338, height=26, width=74)
Label9.configure(text='''Vstart (V)''')

Label20 = tk.Label( )
Label20.place(relx=0.889, rely=0.426, height=26, width=73)
Label20.configure(text='''Vend (V)''')
Label20.configure(width=73)

Label21 = tk.Label( )
Label21.place(relx=0.901, rely=0.515, height=26, width=47)
Label21.configure(text='''Vstep''')

Label22 = tk.Label()
Label22.place(relx=0.889, rely=0.338, height=26, width=74)
Label22.configure(text='''Vstart (V)''')

TLabel4 =  tk.Label()
TLabel4.place(relx=0.811, rely=0.235, height=24, width=105)
TLabel4.configure(text='''Sweep Settings''')

TLabel5 =  tk.Label()
TLabel5.place(relx=0.778, rely=0.294, height=24, width=29)
TLabel5.configure(text='''S-D''')

TLabel6 =  tk.Label()
TLabel6.place(relx=0.9, rely=0.294, height=24, width=35)
TLabel6.configure(text='''Gate''')

TLabel7 =  tk.Label()
TLabel7.place(relx=0.156, rely=0.103, height=24, width=63)
TLabel7.configure(text='''Precision''')

TLabel8 =  tk.Label()
TLabel8.place(relx=0.156, rely=0.162, height=24, width=46)
TLabel8.configure(text='''Range''')

TLabel9 =  tk.Label()
TLabel9.place(relx=0.156, rely=0.221, height=24, width=32)
TLabel9.configure(text='''OSR''')

TLabel10 =  tk.Label()
TLabel10.place(relx=0.511, rely=0.103, height=24, width=63)
TLabel10.configure(text='''Precision''')

TLabel11 =  tk.Label()
TLabel11.place(relx=0.511, rely=0.162, height=24, width=46)
TLabel11.configure(text='''Range''')

TLabel12 =  tk.Label()
TLabel12.place(relx=0.511, rely=0.221, height=24, width=32)
TLabel12.configure(text='''OSR''')


##All Entries
COMp=tk.StringVar()
TEntry1 = tk.Entry(textvariable=COMp)
TEntry1.configure(width=66)
TEntry1.place(relx=0.106, rely=0.015, relheight=0.038 , relwidth=0.073)
COM=set_com_port()
TEntry1.insert(tk.END,COM)


v_transfer = tk.DoubleVar()
Entry1 = tk.Entry( )
Entry1.place(relx=0.817, rely=0.779,height=24, relwidth=0.071)
Entry1.configure(width=64,textvariable=v_transfer)
Entry1.configure(state=tk.DISABLED)

vs_start = tk.DoubleVar()
Entry2 = tk.Entry( )
Entry2.place(relx=0.767, rely=0.375,height=24, relwidth=0.06)
Entry2.configure(width=54)
Entry2.configure(textvariable=vs_start)

vs_end = tk.DoubleVar()
Entry3 = tk.Entry( )
Entry3.place(relx=0.767, rely=0.463,height=24, relwidth=0.06)
Entry3.configure(textvariable=vs_end)

vs_step = tk.DoubleVar() 
Entry4 = tk.Entry( )
Entry4.place(relx=0.767, rely=0.551,height=24, relwidth=0.06)
Entry4.configure(textvariable=vs_step)

#Gstart
vg_start = tk.DoubleVar()
Entry5 = tk.Entry( )
Entry5.place(relx=0.894, rely=0.375,height=24, relwidth=0.06)
Entry5.configure(width=54,textvariable=vg_start)


#Gend
vg_end = tk.DoubleVar()
Entry6 = tk.Entry( )
Entry6.place(relx=0.894, rely=0.463,height=24, relwidth=0.06)
Entry6.configure(width=54,textvariable=vg_end)
#Gstep
vg_step = tk.DoubleVar() 
Entry7 = tk.Entry( )
Entry7.place(relx=0.894, rely=0.551,height=24, relwidth=0.06)
Entry7.configure(width=54,textvariable=vg_step)

         


##Misc
TSeparator1 = ttk.Separator()
TSeparator1.place(relx=0.444, rely=0.066, relheight=0.206)
TSeparator1.configure(orient="vertical")

TSeparator2 = ttk.Separator()
TSeparator2.place(relx=0.017, rely=0.279, relwidth=0.722)

transferchara=tk.IntVar()
Checkbutton1 = tk.Checkbutton( )
Checkbutton1.place(relx=0.767, rely=0.728, relheight=0.046, relwidth=0.194)
Checkbutton1.configure(text='''Transfer Characteristic :''',command=transfer,variable=transferchara)

Button4 = tk.Button( )
Button4.place(relx=0.922,rely=.015)
Button4.configure(command=about,text="About")

Button1 = tk.Button( )
Button1.place(relx=0.778, rely=0.919, height=33, width=176)
Button1.configure(command=savefile,width=176)
Button1.configure(text="Save data")
if data_out== []:
    Button1.configure(state=tk.DISABLED)

Button2 = tk.Button( )
Button2.place(relx=0.778, rely=0.853, height=33, width=176)
Button2.configure(width=176,command=plot_click)
Button2.configure(text="Start")
#Range 1
Scale1 = tk.Scale(from_=1, to=5)
Scale1.place(relx=0.267, rely=0.132, relwidth=0.118, relheight=0.0
        , height=47, bordermode='ignore')
Scale1.configure(orient="horizontal")
Scale1.set(2)

#OSR 1
Scale2 = tk.Scale(from_=1, to=9)
Scale2.place(relx=0.267, rely=0.191, relwidth=0.118, relheight=0.0
        , height=47, bordermode='ignore')
Scale2.configure(orient="horizontal")

#Precision1
Scale3 = tk.Scale(from_=1, to=5)
Scale3.place(relx=0.267, rely=0.074, relwidth=0.118, relheight=0.0
        , height=47, bordermode='ignore')
Scale3.configure(orient="horizontal")

#Range 2
Scale4 = tk.Scale(from_=1, to=5)
Scale4.place(relx=0.589, rely=0.132, relwidth=0.118, relheight=0.0
        , height=47, bordermode='ignore')
Scale4.configure(orient="horizontal")

#OSR 2
Scale5 = tk.Scale(from_=1, to=9)
Scale5.place(relx=0.589, rely=0.191, relwidth=0.118, relheight=0.0
        , height=47, bordermode='ignore')
Scale5.configure(orient="horizontal")

#Precision 2
Scale6 = tk.Scale(from_=1, to=5)
Scale6.place(relx=0.589, rely=0.074, relwidth=0.118, relheight=0.0
        , height=47, bordermode='ignore')
Scale6.configure(orient="horizontal")




unsafe=tk.IntVar()
Checkbutton2 = tk.Checkbutton( )
Checkbutton2.place(relx=0.030, rely=0.162, relheight=0.046
                , relwidth=0.082)
Checkbutton2.configure(justify='left')
Checkbutton2.configure(variable=unsafe,text='''Unsafe!''')
init_values()



#
main.mainloop()
