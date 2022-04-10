import tkinter
import tkinter.font
import requests
#from gpiozero import LED
from threading import Thread
from PIL import ImageTk, Image 
from time import sleep
#--------------------------------------------------#Variables Globales-------------------------------------------------------------------------
#relayIn=LED(20)
#relayOut=LED(21)
Variable=''          # Varible donde va la contraseña
isFrame=True         # Verificar si la ventana0 se ve para mover el gif
timer=0              # Lleva el tiempo para volver a ventana 0
procesos=[]          # Arreglo hilos en paralelo
imagen=[]            #Variable donde estaran las imagenes
detenertimer=False
#--------------------------------------------------#Funciones-----------------------------------------------------------------------------------
def block(x):                                                  #Guarda contraseña de manera global y cambia los digitos por (*) 
       global Variable
       resetTimer()
       if len(entrada.get())<6:
              entrada.insert(tkinter.END,int(x))
              y=str(entrada.get())
              Variable+= y[len(y)-1]
              entrada.delete(len(y)-1, tkinter.END)
              entrada.insert(tkinter.END, '*')

def botonDelete():                                             #Resetear campo label de contraseña
       entrada.delete(0,tkinter.END)
       global Variable
       Variable= ''
       resetTimer()
       
def resetTimer():
       global timer
       timer= 0
                   
def checkPassword():
       x=str(Variable)
       botonDelete()
       y= len(x)
       entrada.delete(0,tkinter.END)
       if y==6:
              #if(x=='000000'):                   #quitar
              #       frame1Ver()                 #quitar
              #       print(x)                    #quitar
              #else:
               #      print('contraseña no valida')      #quitar
               #      resetTimer()                       #quitar
               #      frame2Ver()                        #quitar
                                                                            
              info = x +';1;1;5'   #respuesta 0 = error, 1= correcto         #info = (area);(sentido 1=in, 2=out);(5 = pinpass)
              url = 'http://192.168.70.10:2942/api/Verificador'
              hdr = {'Rut':info}
              try:
                     request = requests.get(url,headers = hdr)        #1 entrada; 2saliendo; 0Problema o no tiene acceso
                     print(request.json())
                     if str(request.json()) == '1':
                            print('Entrada abre')
              #              #relayIn.on()                             #Accionar rele de Entrada
              #              sleep(2)
              #              #relayIn.off()                            
                            frame1Ver()
              #       elif str(request.json()) == '2':
              #              print('Abrir Salida')  
              #              #relayOut.on()                            #Accionar rele Salida
              #              sleep(2)
              #              #relayOut.off()
              #              frame1Ver()
                     else:
                            print('No tienes acceso')
                            sleep(1)
                            frame2Ver()
              except:
                     print('error en api')
                     frame2Ver()
       else:
              print('contraseña no valida') 
              resetTimer()
              frame2Ver()      

def gif(): 
       global isFrame
       isFrame=True
       x=0
       while isFrame:
              botonV0.configure(image=imagen[x])
              botonV0.update()
              x=x+1
              sleep(0.06)
              if x==238:
                     print(x)
                     x=0

def frame1Ver():
       global detenertimer
       detenertimer=True
       frame.pack_forget()
       frame1.pack()
       x=7
       while x>0:
              labelV1.configure(text = 'Verificacion Correcta, Adelante!! (%d)' %x)
              labelV1.update()
              sleep(1)
              x-=1
       frame1.pack_forget()
       frame0.pack(fill="both", expand="yes")
       gif()

def frame2Ver():
       global detenertimer
       detenertimer=True
       frame.pack_forget()
       frame2.pack()
       x=7
       while x>0:
              labelV2.configure(text = 'Contraseña incorrecta, vuelve a intentar. (%d)' %x)
              labelV2.update()
              sleep(1)
              x-=1
       ventana2Ocultar()

def frame0Ocultar():
       global isFrame
       isFrame=False
       frame0.pack_forget()
       mostrarFrame()   
     
def mostrarFrame():
       global timer
       global procesos

       frame.pack(fill="both", expand="yes")  
       thread =Thread(target=temporizador,args=[])
       thread.start()
       procesos.append(thread)  

def temporizador():
       global timer 
       global detenertimer
       detenertimer=False
       while (timer<5 and detenertimer==False): 
              print(timer)     
              sleep(1)
              timer=timer+1
              if (timer == 5):
                     mostrarFrame0()
                     gif()
       timer = 0

def mostrarFrame0():
       entrada.delete(0,tkinter.END)
       frame.pack_forget()
       frame0.pack(fill="both", expand="yes")

def ventana2Ocultar():
       frame2.pack_forget()
       mostrarFrame()
#------------------------------------------------#Ventana Root--------------------------------------------------------------------------------
ventana = tkinter.Tk()       #ventana.iconbitmap("ico.ico")
ventana.title('PinPass')
ventana.geometry('480x800')
ventana.attributes("-fullscreen", True)
#------------------------------------------------#Frames -------------------------------------------------------------------------------------
frame0 = tkinter.LabelFrame(ventana, text = 'Inicio')
frame =  tkinter.LabelFrame(ventana, text = ' Password ',             height = 300, width =460)
frame1 = tkinter.LabelFrame(ventana, text = 'Password Correcto',      height = 300, width =460)
frame2 = tkinter.LabelFrame(ventana, text = 'Password Incorrecto',    height = 300, width =460)
#------------------------------------------------#fotogramas gif e imagenes------------------------------------------------------------------
#for i in range(0, 301):
for i in range(0, 239):
        print('Sin título_000'+str(i).zfill(3)+'.jpeg')
        imagen.append([ImageTk.PhotoImage(Image.open('Sin título_000'+str(i).zfill(3)+'.jpeg'))])
#       imagen.append([ImageTk.PhotoImage(Image.open('str(i)+'.jpeg'))])
logoZpass = ImageTk.PhotoImage(Image.open('Zpass.png'))
concebidoa    =      ImageTk.PhotoImage(Image.open('concebidoa.jpg'))
denegadoa     =      ImageTk.PhotoImage(Image.open('denegadoa.jpg'))
#------------------------------------------------#Definir Elementos---------------------------------------------------------------------------
botonV0 = tkinter.Button(frame0, image= imagen[0], bg = 'royal blue', relief='flat', borderwidth=0 , command = frame0Ocultar)
etiqueta = tkinter.Label(frame, text = 'Hola, introduce tu contraseña de 6 digitos', font= ("Helvetica",16))
entrada = tkinter.Entry(frame, width=6,          font= ("Helvetica",22))
boton  =  tkinter.Button(frame, text = 'Enviar', font= ("Helvetica",14), command = checkPassword)
boton0 =  tkinter.Button(frame, text = '0',      font= ("Helvetica",14), command = lambda: block('0'))                       
boton1 =  tkinter.Button(frame, text = '1',      font= ("Helvetica",14), command = lambda: block('1'))
boton2 =  tkinter.Button(frame, text = '2',      font= ("Helvetica",14), command = lambda: block('2'))
boton3 =  tkinter.Button(frame, text = '3',      font= ("Helvetica",14), command = lambda: block('3'))
boton4 =  tkinter.Button(frame, text = '4',      font= ("Helvetica",14), command = lambda: block('4'))
boton5 =  tkinter.Button(frame, text = '5',      font= ("Helvetica",14), command = lambda: block('5'))
boton6 =  tkinter.Button(frame, text = '6',      font= ("Helvetica",14), command = lambda: block('6'))
boton7 =  tkinter.Button(frame, text = '7',      font= ("Helvetica",14), command = lambda: block('7'))
boton8 =  tkinter.Button(frame, text = '8',      font= ("Helvetica",14), command = lambda: block('8'))
boton9 =  tkinter.Button(frame, text = '9',      font= ("Helvetica",14), command = lambda: block('9'))
boton10 = tkinter.Button(frame, text = ' Borrar',font= ("Helvetica",12), command = botonDelete)  
labelV1 = tkinter.Label(frame1, text = 'Verificacion Correcta, Adelante!!',font= ("Helvetica",12))
labelV2 = tkinter.Button(frame2, text = 'Contraseña incorrecta, vuelve a intentar.',font= ("Helvetica",12), relief="groove",command = ventana2Ocultar)
label1V2= tkinter.Label(frame2, image = denegadoa)
label1V1 = tkinter.Label(frame1, image = concebidoa)
#--------------------------------------------#Colocar elementos en ventanas---------------------------------------------------------------------
boton.place( x=550, y=360, width=150, height=61) 
boton0.place(x=325, y=360, width=150, height=61)
boton1.place(x=100, y=290, width=150, height=61)
boton2.place(x=325, y=290, width=150, height=61)
boton3.place(x=550, y=290, width=150, height=61)
boton4.place(x=100, y=220, width=150, height=61)
boton5.place(x=325, y=220, width=150, height=61)
boton6.place(x=550, y=220, width=150, height=61)
boton7.place(x=100, y=150, width=150, height=61)
boton8.place(x=325, y=150, width=150, height=61)
boton9.place(x=550, y=150, width=150, height=61)
boton10.place(x=100, y=360, width=150, height=61)
etiqueta.place(x=160, y=10, width=500, height=61)
entrada.place(x=210, y=70, width=400, height=50)
labelV1.pack(side = "bottom")
labelV2.pack(side = "bottom")
botonV0.place(x=0, y=0, width=800, height=480) 
label1V1.pack(side = "top")
label1V2.pack(side = "top")
frame0.pack(fill="both", expand="yes")
sleep(1)
gif()
ventana.mainloop()