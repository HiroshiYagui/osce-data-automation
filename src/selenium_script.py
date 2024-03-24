#hello.py
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import math
from timeit import default_timer as timer
import csv
import logging
import sys
import time
import json
import src.constants as const

'''
Control de errores (que no se desplome y muestre en que página se cayó) #
Log de detalles #
Input MES a MES #
Plantilla de XPATH (HTML de ejemplo), lo cargamos , cuando se hace la referencia #
Archivo de configuración:
    tabla_login:/html/body/div[1]/div/div/div[7]/div/div/div/div/div/div[2]/div[3]/div/article/article[1]/p[14]
    tabla_decretos:/html/body/div[1]/div/div/div[7]/div/div/div/div/div/div[2]/div[3]/div/article/article[1]/p[13]
Ya no cargarlo a TXT sino CSV #

Ejecutar el descargar listado


Hago un manual de instalacion
Que se cree un .exe
Crear un módulo con frame que invoque al script con parámetros de fecha 
    -Debe incluir: 
        *Fecha de inicio, fecha de fin, año , estado
    -Debe bloquearse hasta que termine el script
    -Al finalizar muestra mensaje de correcto o error
    -Decidir el nombre de archivo de salida

Crear flujo de frames por cada reporte
    -Se cambia el archivo de parametros para cada flujo
    -Se cambia los argumentos del script (Un flujo por cada tipo de reporte) o en el archivo de parámetros se especificara los campos que deben ser llenados
    

Preguntar por los reportes a explotar
'''




class Flujo(webdriver.Firefox):
    def __init__(self,teardown=False):
        self.service = webdriver.FirefoxService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)
        self.logger=logging.getLogger('service')
        self.options = Options()
        #self.options.add_argument("-headless")
        
        logging.basicConfig(level=logging.INFO)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Inicio")
        self.file_output=open('output_'+time.ctime()+'.csv','w',newline='')
        file_json=open("xpath.json",'r')
        self.all_parameters=json.load(file_json)
        file_json.close()
        self.output_writer=csv.writer(self.file_output,delimiter='|',
                            quotechar="'", quoting=csv.QUOTE_MINIMAL)
        self.start_script=timer()
        self.start_registers=0.0
        self.end_script=0.0
        self.time_register=[]
        #self.teardown=teardown
        super(Flujo,self).__init__(options=self.options)
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        #self.teardown:
        self.end_script=timer()
        self.file_output.close()     
        self.close()
        #self.file_json.close()  

        self.logger.info(time.ctime()+':\t'+"Start time:"+str(self.start_script))
        self.logger.info(time.ctime()+':\t'+"Prepare time:"+str(self.start_registers-self.start_script))
        if len(self.time_register)>0:
            self.logger.info(time.ctime()+':\t'+"Registers time (avg):"+str(sum(self.time_register)/len(self.time_register)))
        self.logger.info(time.ctime()+':\t'+"End time:"+str(self.end_script))
        self.logger.info(time.ctime()+':\t'+"Total time:"+str(self.end_script-self.start_script))
        

    def flujo_decretos(self,input_fecha_inicio,input_fecha_fin,input_estado):
        parameters=self.all_parameters["flujo_decretos"]
        input1=input_fecha_inicio
        input2=input_fecha_fin
        input3=input_estado
        self.logger.info(time.ctime()+':\t'+input1)
        self.logger.info(time.ctime()+':\t'+input2)

        self.get(const.BASE_URL)

        self.implicitly_wait(10)


        user_element=self.find_element(By.XPATH,self.all_parameters["inicio"]["usuario_input"])
        pass_element=self.find_element(By.XPATH,self.all_parameters["inicio"]["senha_input"])

        user_element.send_keys("nprieto")
        pass_element.send_keys("123")

        try:
            submit_btn=self.find_element(By.XPATH,self.all_parameters["inicio"]["boton_submt"])
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Error al invocar boton de Login")
            sys.exit()

        try:
            submit_btn.click()
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Error al presionar boton Login")
            sys.exit()

        try:
            select_option=self.find_element(By.XPATH,parameters["opcion_reporte"])
            select_option.click()
            select_option=self.find_element(By.XPATH,parameters["reporte_decretos"])
            select_option.click()
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Error al encontrar elementos de Navegacion")
            sys.exit()

        try:
            list_status=self.find_element(By.XPATH,parameters["estado_reporte"])
            select_status=Select(list_status)
            select_status.select_by_value(input3)
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"No se puedo encontrar ESTADO")
            sys.exit()

        try:
            fecha_inicio=self.find_element(By.XPATH,parameters["fecha_inicio"])
            fecha_fin=self.find_element(By.XPATH,parameters["fecha_fin"])
            fecha_inicio.send_keys(input1)
            fecha_fin.send_keys(input2)

            btn_Buscar=self.find_element(By.XPATH,parameters["btn_buscar"])
            btn_Buscar.click()
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Problema con ingreso de fechas")
            sys.exit()
            

        self.start_registers=timer()

        
        try:
            lista_cabecera=self.find_elements(By.XPATH,parameters["tabla_cabecera"])
            cabecera_text=[]
            for cabecera in lista_cabecera:
                if cabecera.text != "":
                    cabecera_text.append(cabecera.text)
            self.output_writer.writerow(cabecera_text)
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"No se encontro cabecera")
            sys.exit()


        try:
            register_quantitys=self.find_elements(By.XPATH,parameters["linea_cantidadReg"])
            register_quantity=self.find_element(By.XPATH,parameters["linea_cantidadReg"]+'['+str(len(register_quantitys))+']/td/b')
            quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
            quantity=int(quantity)
            num_pages=math.ceil(quantity/30)
        except NoSuchElementException:
            self.logger.info(time.ctime()+':\t'+"Registros < 31")

        

        index=1

        while index<=num_pages:
            try:
                list_paginas=self.find_element(By.XPATH,parameters["select_pagina"])
                select_pagina=Select(list_paginas)
                select_pagina.select_by_value(str(index))
                time.sleep(2)
            except NoSuchElementException:
                self.logger.info(time.ctime()+':\t'+"Registros No tienen más de 1 pagina")
            tabla_registers=[]
            try:
                tabla_registers=self.find_elements(By.XPATH,parameters["tabla_registro"])
                first_register=int(tabla_registers[0].find_elements(By.XPATH,"td")[0].text)
                while first_register!=30*(index-1)+1:
                    time.sleep(0.5)
                    tabla_registers=self.find_elements(By.XPATH,parameters["tabla_registro"])
                    if len(tabla_registers)>0:
                        first_register=int(tabla_registers[0].find_elements(By.XPATH,"td")[0].text)
                register_time_start=timer()
                for register in tabla_registers:
                    tabla_data=[]
                    tabla_data=register.find_elements(By.XPATH,"td")
                    register_text=[]
                    for data in tabla_data:
                        if not "total de registros" in data.text and not "Pagina" in data.text:
                            register_text.append(data.text.replace('\n',''))   
                    if len(register_text)>0:
                        self.logger.info(time.ctime()+':\t'+"Registro:"+register_text[0]+"/"+str(quantity))
                        self.output_writer.writerow(register_text)
            except Exception:
                self.logger.error("No se encuentran los registros/valores",exc_info=True)
                sys.exit()
            try:
                register_quantitys=self.find_elements(By.XPATH,parameters["linea_cantidadReg"])
                register_quantity=self.find_element(By.XPATH,parameters["linea_cantidadReg"]+'['+str(len(register_quantitys))+']/td/b')
                quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
                quantity=int(quantity)
                num_pages=math.ceil(quantity/30)
            except NoSuchElementException:
                self.logger.info(time.ctime()+':\t'+"terminado")
            self.logger.info(time.ctime()+':\t'+"pagina:"+str(index))
            index+=1
            register_time_end=timer()
            self.time_register.append(register_time_end-register_time_start)

        self.logger.info(time.ctime()+':\t'+"Terminado con Exito")


    def flujo_reportes_salas(self,input_fecha_inicio,input_fecha_fin,input_estado):
            parameters=self.all_parameters["flujo_salas"]
            input1=input_fecha_inicio
            input2=input_fecha_fin
            input3=input_estado
            self.logger.info(time.ctime()+':\t'+input1)
            self.logger.info(time.ctime()+':\t'+input2)

            self.get(const.BASE_URL)

            self.implicitly_wait(10)


            user_element=self.find_element(By.XPATH,self.all_parameters["inicio"]["usuario_input"])
            pass_element=self.find_element(By.XPATH,self.all_parameters["inicio"]["senha_input"])

            user_element.send_keys("nprieto")
            pass_element.send_keys("123")

            try:
                submit_btn=self.find_element(By.XPATH,self.all_parameters["inicio"]["boton_submt"])
            except NoSuchElementException:
                self.logger.error(time.ctime()+':\t'+"Error al invocar boton de Login")
                sys.exit()

            try:
                submit_btn.click()
            except NoSuchElementException:
                self.logger.error(time.ctime()+':\t'+"Error al presionar boton Login")
                sys.exit()

            try:
                select_option=self.find_element(By.XPATH,parameters["opcion_salas"])
                select_option.click()
                select_option=self.find_element(By.XPATH,parameters["opcion_reporte_salas"])
                select_option.click()
            except NoSuchElementException:
                self.logger.error(time.ctime()+':\t'+"Error al encontrar elementos de Navegacion")
                sys.exit()

            try:
                list_status=self.find_element(By.XPATH,parameters["estado_bandeja"])
                select_status=Select(list_status)
                #select_status.select_by_value(input3)
                select_status.select_by_value("03")
            except NoSuchElementException:
                self.logger.error(time.ctime()+':\t'+"No se puedo encontrar ESTADO")
                sys.exit()

            try:
                fecha_inicio=self.find_element(By.XPATH,parameters["fec_pro_ini"])
                fecha_fin=self.find_element(By.XPATH,parameters["fec_pro_fin"])
                fecha_inicio.send_keys(input1)
                fecha_fin.send_keys(input2)

                btn_Buscar=self.find_element(By.XPATH,parameters["btn_buscar"])
                btn_Buscar.click()
            except NoSuchElementException:
                self.logger.error(time.ctime()+':\t'+"Problema con ingreso de fechas")
                sys.exit()
                

            self.start_registers=timer()

            
            try:
                lista_cabecera=self.find_elements(By.XPATH,parameters["tabla_cabecera"])
                cabecera_text=[]
                for cabecera in lista_cabecera:
                    if cabecera.text != "":
                        cabecera_text.append(cabecera.text)
                self.output_writer.writerow(cabecera_text)
            except NoSuchElementException:
                self.logger.error(time.ctime()+':\t'+"No se encontro cabecera")
                sys.exit()


            try:
                register_quantitys=self.find_elements(By.XPATH,parameters["linea_cantidadReg"])
                register_quantity=self.find_element(By.XPATH,parameters["linea_cantidadReg"]+'['+str(len(register_quantitys))+']/td/b')
                quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
                quantity=int(quantity)
                num_pages=math.ceil(quantity/30)
            except NoSuchElementException:
                self.logger.info(time.ctime()+':\t'+"Registros < 31")

            

            index=1

            while index<=num_pages:
                try:
                    list_paginas=self.find_element(By.XPATH,parameters["select_pagina"])
                    select_pagina=Select(list_paginas)
                    select_pagina.select_by_value(str(index))
                    time.sleep(2)
                except NoSuchElementException:
                    self.logger.info(time.ctime()+':\t'+"Registros No tienen más de 1 pagina")
                tabla_registers=[]
                try:
                    tabla_registers=self.find_elements(By.XPATH,parameters["tabla_registro"])
                    first_register=int(tabla_registers[0].find_elements(By.XPATH,"td")[0].text)
                    while first_register!=30*(index-1)+1:
                        time.sleep(0.5)
                        tabla_registers=self.find_elements(By.XPATH,parameters["tabla_registro"])
                        if len(tabla_registers)>0:
                            first_register=int(tabla_registers[0].find_elements(By.XPATH,"td")[0].text)
                    register_time_start=timer()
                    for register in tabla_registers:
                        tabla_data=[]
                        tabla_data=register.find_elements(By.XPATH,"td")
                        register_text=[]
                        for data in tabla_data:
                            if not "total de registros" in data.text and not "Pagina" in data.text:
                                register_text.append(data.text.replace('\n',''))   
                        if len(register_text)>0:
                            self.logger.info(time.ctime()+':\t'+"Registro:"+register_text[0]+"/"+str(quantity))
                            self.output_writer.writerow(register_text)
                except Exception:
                    self.logger.error("No se encuentran los registros/valores",exc_info=True)
                    sys.exit()
                try:
                    register_quantitys=self.find_elements(By.XPATH,parameters["linea_cantidadReg"])
                    register_quantity=self.find_element(By.XPATH,parameters["linea_cantidadReg"]+'['+str(len(register_quantitys))+']/td/b')
                    quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
                    quantity=int(quantity)
                    num_pages=math.ceil(quantity/30)
                except NoSuchElementException:
                    self.logger.info(time.ctime()+':\t'+"terminado")
                self.logger.info(time.ctime()+':\t'+"pagina:"+str(index))
                index+=1
                register_time_end=timer()
                self.time_register.append(register_time_end-register_time_start)

            self.logger.info(time.ctime()+':\t'+"Terminado con Exito")






