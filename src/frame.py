from tkinter import *
#from selenium_script import flujo_1
from .selenium_script import Flujo
from tkinter import ttk
import subprocess
import logging
import time

class windows(Tk):
    def __init__(self, *args,**kwargs):
        Tk.__init__(self,*args,**kwargs)

        self.wm_title("Explotación de pantallas OSCE")
        
        container=ttk.Frame(self,height=400,width=600)

        container.pack(side="top",fill="both",expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        self.frames_names=(decretos_page,main_page,salas_page)

        for F in self.frames_names:
            frame=F(container,self)

            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(main_page)
    
    def show_frame(self,cont):
        frame=self.frames[cont]

        frame.tkraise()




class decretos_page(ttk.Frame):

    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent,height=1800,width=3200)
        title=ttk.Label(self,text="Reporte de decretos")
        title.pack(padx=10,pady=10)
        
        fecha_inicio=StringVar()
        ttk.Entry(self,textvariable=fecha_inicio).pack(padx=10,pady=10)
        fecha_fin=StringVar()
        ttk.Entry(self,textvariable=fecha_fin).pack(padx=10,pady=10)
        estado_reporte=StringVar()
        estado_values=["Ninguno","Pendiente","Revisión","Rechazado","Aprobado","Anulado"]
        estado_key_values={"Ninguno":"0",
                           "Pendiente":"1",
                           "Revisión":"2",
                           "Rechazado":"3",
                           "Aprobado":"4",
                           "Anulado":"5"}
        ttk.Combobox(self,textvariable=estado_reporte,values=estado_values).pack(padx=10,pady=10)
        procesar_button=ttk.Button(
            self,
            text="Enviar",
            command= lambda: self.process(fecha_inicio.get(),fecha_fin.get(),estado_key_values[estado_reporte.get()])
        )
        procesar_button.pack(side="bottom",fill=X)

        navigation_button=ttk.Button(
            self,
            text="Volver",
            command= lambda: controller.show_frame(main_page)
        )
        navigation_button.pack(side="bottom",fill=X)

        
    
    def process(self,fecha_inicio,fecha_fin,estado_reporte):
        #logger.info(time.ctime()+"\tIniciando flujo_1")
        #logger.info(time.ctime()+"\tParams:\t"+fecha_inicio+" "+fecha_fin)
        with Flujo() as bot:
            bot.flujo_decretos(input_fecha_inicio=fecha_inicio,input_fecha_fin=fecha_fin,input_estado=estado_reporte)

class salas_page(ttk.Frame):

    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent,height=1800,width=3200)
        title=ttk.Label(self,text="Reporte de salas")
        title.pack(padx=10,pady=10)
        
        fecha_inicio=StringVar()
        ttk.Entry(self,textvariable=fecha_inicio).pack(padx=10,pady=10)
        fecha_fin=StringVar()
        ttk.Entry(self,textvariable=fecha_fin).pack(padx=10,pady=10)
        estado_reporte=StringVar()
        estado_values=["","1","2","3","4","5"]
        ttk.Combobox(self,textvariable=estado_reporte,values=estado_values).pack(padx=10,pady=10)
        procesar_button=ttk.Button(
            self,
            text="Enviar",
            command= lambda: self.process(fecha_inicio.get(),fecha_fin.get(),estado_reporte.get())
        )
        procesar_button.pack(side="bottom",fill=X)

        navigation_button=ttk.Button(
            self,
            text="Volver",
            command= lambda: controller.show_frame(main_page)
        )
        navigation_button.pack(side="bottom",fill=X)

        
    
    def process(self,fecha_inicio,fecha_fin,estado_reporte):
        #logger.info(time.ctime()+"\tIniciando flujo_1")
        #logger.info(time.ctime()+"\tParams:\t"+fecha_inicio+" "+fecha_fin)
        with Flujo() as bot:
            bot.flujo_reportes_salas(input_fecha_inicio=fecha_inicio,input_fecha_fin=fecha_fin,input_estado=estado_reporte)


class main_page(ttk.Frame):

    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        title=ttk.Label(self,text="Principal")
        title.pack(padx=10,pady=10)
        navigation_button=ttk.Button(
            self,
            text="Volver",
            command= lambda: controller.show_frame(main_page)
        )
        navigation_button.pack(side="bottom",fill=X)
        
        decretos_button=ttk.Button(
            self,
            text="Reporte de Decretos",
            command= lambda: controller.show_frame(decretos_page)
        )
        decretos_button.pack(side="bottom",fill=X)

        salas_button=ttk.Button(
            self,
            text="Reporte de Salas",
            command= lambda: controller.show_frame(salas_page)
        )
        salas_button.pack(side="bottom",fill=X)


if __name__=="__main__":
    logger=logging.getLogger('service')
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    test=windows()
    test.mainloop()
""" root=Tk()
frm=ttk.Frame(root,padding=10)
frm.grid()
ttk.Label(frm,text="Primer prueba").grid(column=0,row=0)
ttk.Button(frm,text="Enviar",command=lambda:flujo_1(fecha_inicio.get(),fecha_fin.get())).grid(column=0,row=3)
ttk.Button(frm,text="Salir",command=root.destroy).grid(column=0,row=4)
root.mainloop() """


