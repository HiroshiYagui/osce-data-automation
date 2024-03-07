#hello.py
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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


# driver.get("https://www.selenium.dev/selenium/web/web-form.html")
# driver.get("https://www.selenium.dev/selenium/web/linked_image.html")
# service = webdriver.ChromeService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)
# title = driver.title
# driver.implicitly_wait(10)


# Retrieves the text of the element
#text = driver.find_element(By.NAME, "my-select").find_elements(By.TAG_NAME,"option")

# text = driver.find_element(By.NAME,"my-readonly").get_attribute("value")
# logger.info(text)
# button=driver.find_element(By.TAG_NAME,"button")
# button.click()
# text = driver.find_element(By.ID,"message").text
# logger.info(text)

class Flujo(webdriver.Firefox):
    def __init__(self,teardown=False):
        self.service = webdriver.FirefoxService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)
        self.logger=logging.getLogger('service')
        logging.basicConfig(level=logging.INFO)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Inicio")
        self.file_output=open('output.csv','w',newline='')
        self.file_json=open("xpath.json",'r')
        self.output_writer=csv.writer(self.file_output,delimiter='|',
                            quotechar="'", quoting=csv.QUOTE_MINIMAL)
        self.start_script=timer()
        self.start_registers=0.0
        self.end_script=0.0
        self.time_register=[]
        self.teardown=teardown
        super(Flujo,self).__init__()
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.teardown:
            self.end_script=timer()
            self.file_output.close()     
            self.close()
            self.file_json.close()  

            self.logger.info(time.ctime()+':\t'+"Start time:"+str(self.start_script))
            self.logger.info(time.ctime()+':\t'+"Prepare time:"+str(self.start_registers-self.start_script))
            if len(self.time_register)>0:
                self.logger.info(time.ctime()+':\t'+"Registers time (avg):"+str(sum(self.time_register)/len(self.time_register)))
            self.logger.info(time.ctime()+':\t'+"End time:"+str(self.end_script))
            self.logger.info(time.ctime()+':\t'+"Total time:"+str(self.end_script-self.start_script))
    
    def flujo_decretos(self,input_fecha_inicio,input_fecha_fin):
        parameters=json.load(self.file_json)
        input1=input_fecha_inicio
        input2=input_fecha_fin
        """ input1=tx1
        input2=tx2 """
        self.logger.info(time.ctime()+':\t'+input1)
        self.logger.info(time.ctime()+':\t'+input2)
        """ service = webdriver.ChromeService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT) """

        self.get(const.BASE_URL)

        """ file_output=open("output.txt","a") """

        self.implicitly_wait(10)


        user_element=self.find_element(By.NAME,"usuario")
        pass_element=self.find_element(By.NAME,"senha")

        user_element.send_keys("nprieto")
        pass_element.send_keys("123")

        #self.logger.info(user_element.get_attribute("value"))
        #self.logger.info(pass_element.get_attribute("value"))
        try:
            submit_btn=self.find_element(By.XPATH,parameters["boton_submt"])
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Error al invocar boton de Login")
            sys.exit()

        """ for btn in arr_btn:
            value=btn.get_attribute("VALUE")
            if value=="Iniciar Sesión":
                submit_btn=btn
                break
        """
        #self.logger.info(submit_btn.get_attribute("VALUE"))
        try:
            submit_btn.click()
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Error al presionar boton Login")
            sys.exit()

        """ list_options=self.find_elements(By.TAG_NAME,"li")

        for option in list_options:
            logger.info(option.text)
            if option.text=="Reportes":
                select_option=option
                break

        select_option.click()
        list_options=self.find_elements(By.TAG_NAME,"li")
        for option in list_options:
            if option.text=="Reporte de Decretos":
                select_option=option
                break """
        try:
            select_option=self.find_element(By.XPATH,parameters["opcion_reporte"])
            select_option.click()
            select_option=self.find_element(By.XPATH,parameters["reporte_decretos"])
            select_option.click()
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Error al encontrar elementos de Navegacion")
            sys.exit()


        #list_status=self.find_element(By.ID,"estado")
        try:
            list_status=self.find_element(By.XPATH,parameters["estado_reporte"])
            select_status=Select(list_status)
            select_status.select_by_visible_text("Pendiente")
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"No se puedo encontrar ESTADO")
            sys.exit()

        try:
            fecha_inicio=self.find_element(By.XPATH,parameters["fecha_inicio"])
            fecha_fin=self.find_element(By.XPATH,parameters["fecha_fin"])

            """ fecha_inicio.send_keys("21/01/2024")
            fecha_fin.send_keys("16/02/2024") """
            fecha_inicio.send_keys(input1)
            fecha_fin.send_keys(input2)

            btn_Buscar=self.find_element(By.XPATH,parameters["btn_buscar"])
            btn_Buscar.click()
        except NoSuchElementException:
            self.logger.error(time.ctime()+':\t'+"Problema con ingreso de fechas")
            sys.exit()
            

        self.start_registers=timer()

        #tabla_body=self.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
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

        """ """ 
        # lista_paginas=[]

        # list_paginas=self.find_element(By.ID,"Pagina")
        # select_pagina=Select(list_paginas)
        # list_paginas_options=select_pagina.options
        # # for option in list_paginas_options:
        # #     lista_paginas.append(option.get_attribute("value"))
        # # self.logger.info(lista_paginas[-1])

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
            #tabla_body=self.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
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
                        output_writer.writerow(register_text)
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



            # table_header=driver.find_element(By.CLASS_NAME,"provido_lista").find_elements(By.TAG_NAME,"th")
            # header_text=""
            # for header in table_header:
            #     header_text+=header.text+"|"
            # self.logger.info(header_text)
            # # table_body=driver.find_element(By.ID,"table1").find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")
            # # for element in table_body:
            # #     values=element.find_elements(By.TAG_NAME,"td")
            # #     value_text=""
            # #     for value in values:
            # #         value_text+=value.text+"|"
            # #     self.logger.info(value_text)


