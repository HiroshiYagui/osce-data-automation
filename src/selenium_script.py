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



def end_Execute():
    end_script=timer()
    file_output.close()     
    driver.close()
    file_json.close()  

    logger.info(time.ctime()+':\t'+"Start time:"+str(start_script))
    logger.info(time.ctime()+':\t'+"Prepare time:"+str(start_registers-start_script))
    if len(time_register)>0:
        logger.info(time.ctime()+':\t'+"Registers time (avg):"+str(sum(time_register)/len(time_register)))
    logger.info(time.ctime()+':\t'+"End time:"+str(end_script))
    logger.info(time.ctime()+':\t'+"Total time:"+str(end_script-start_script))

def start_execute():
    driver=webdriver.Firefox()
    #driver=webdriver.Chrome()
    service = webdriver.FirefoxService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)
    logger=logging.getLogger('service')
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    logger.info("Inicio")
    file_output=open('output.csv','w',newline='')
    file_json=open("xpath.json",'r')
    output_writer=csv.writer(file_output,delimiter='|',
                            quotechar="'", quoting=csv.QUOTE_MINIMAL)

    return driver,service,output_writer,file_output,logger,file_json




driver,service,output_writer,file_output,logger,file_json=start_execute()
parameters=json.load(file_json)
input1=sys.argv[1]
input2=sys.argv[2]
""" input1=tx1
input2=tx2 """
logger.info(time.ctime()+':\t'+input1)
logger.info(time.ctime()+':\t'+input2)
""" service = webdriver.ChromeService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT) """

driver.get("https://easprep.osce.gob.pe/portaltribunal-uiwd-pub/Logout")

""" file_output=open("output.txt","a") """

driver.implicitly_wait(10)

start_script=timer()
end_script=0.0
start_registers=0.0
time_register=[]


user_element=driver.find_element(By.NAME,"usuario")
pass_element=driver.find_element(By.NAME,"senha")

user_element.send_keys("nprieto")
pass_element.send_keys("123")

#logger.info(user_element.get_attribute("value"))
#logger.info(pass_element.get_attribute("value"))
try:
    submit_btn=driver.find_element(By.XPATH,parameters["boton_submt"])
except NoSuchElementException:
    logger.error(time.ctime()+':\t'+"Error al invocar boton de Login")
    end_Execute()
    sys.exit()

""" for btn in arr_btn:
    value=btn.get_attribute("VALUE")
    if value=="Iniciar Sesión":
        submit_btn=btn
        break
"""
#logger.info(submit_btn.get_attribute("VALUE"))
try:
    submit_btn.click()
except NoSuchElementException:
    logger.error(time.ctime()+':\t'+"Error al presionar boton Login")
    end_Execute()
    sys.exit()

""" list_options=driver.find_elements(By.TAG_NAME,"li")

for option in list_options:
    logger.info(option.text)
    if option.text=="Reportes":
        select_option=option
        break

select_option.click()
list_options=driver.find_elements(By.TAG_NAME,"li")
for option in list_options:
    if option.text=="Reporte de Decretos":
        select_option=option
        break """
try:
    select_option=driver.find_element(By.XPATH,parameters["opcion_reporte"])
    select_option.click()
    select_option=driver.find_element(By.XPATH,parameters["reporte_decretos"])
    select_option.click()
except NoSuchElementException:
    logger.error(time.ctime()+':\t'+"Error al encontrar elementos de Navegacion")
    end_Execute()
    sys.exit()


#list_status=driver.find_element(By.ID,"estado")
try:
    list_status=driver.find_element(By.XPATH,parameters["estado_reporte"])
    select_status=Select(list_status)
    select_status.select_by_visible_text("Pendiente")
except NoSuchElementException:
    logger.error(time.ctime()+':\t'+"No se puedo encontrar ESTADO")
    end_Execute()
    sys.exit()

try:
    fecha_inicio=driver.find_element(By.XPATH,parameters["fecha_inicio"])
    fecha_fin=driver.find_element(By.XPATH,parameters["fecha_fin"])

    """ fecha_inicio.send_keys("21/01/2024")
    fecha_fin.send_keys("16/02/2024") """
    fecha_inicio.send_keys(input1)
    fecha_fin.send_keys(input2)

    btn_Buscar=driver.find_element(By.XPATH,parameters["btn_buscar"])
    btn_Buscar.click()
except NoSuchElementException:
    logger.error(time.ctime()+':\t'+"Problema con ingreso de fechas")
    end_Execute()
    sys.exit()
    

start_registers=timer()

#tabla_body=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
try:
    lista_cabecera=driver.find_elements(By.XPATH,parameters["tabla_cabecera"])
    cabecera_text=[]
    for cabecera in lista_cabecera:
        if cabecera.text != "":
            cabecera_text.append(cabecera.text)
    output_writer.writerow(cabecera_text)
except NoSuchElementException:
    logger.error(time.ctime()+':\t'+"No se encontro cabecera")
    end_Execute()
    sys.exit()


try:
    register_quantitys=driver.find_elements(By.XPATH,parameters["linea_cantidadReg"])
    register_quantity=driver.find_element(By.XPATH,parameters["linea_cantidadReg"]+'['+str(len(register_quantitys))+']/td/b')
    quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
    quantity=int(quantity)
    num_pages=math.ceil(quantity/30)
except NoSuchElementException:
    logger.info(time.ctime()+':\t'+"Registros < 31")

""" """ 
# lista_paginas=[]

# list_paginas=driver.find_element(By.ID,"Pagina")
# select_pagina=Select(list_paginas)
# list_paginas_options=select_pagina.options
# # for option in list_paginas_options:
# #     lista_paginas.append(option.get_attribute("value"))
# # logger.info(lista_paginas[-1])

index=1

while index<=num_pages:
    try:
        list_paginas=driver.find_element(By.XPATH,parameters["select_pagina"])
        select_pagina=Select(list_paginas)
        select_pagina.select_by_value(str(index))
        time.sleep(2)
    except NoSuchElementException:
        logger.info(time.ctime()+':\t'+"Registros No tienen más de 1 pagina")
    tabla_registers=[]
    #tabla_body=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
    try:
        tabla_registers=driver.find_elements(By.XPATH,parameters["tabla_registro"])
        first_register=int(tabla_registers[0].find_elements(By.XPATH,"td")[0].text)
        while first_register!=30*(index-1)+1:
            time.sleep(0.5)
            tabla_registers=driver.find_elements(By.XPATH,parameters["tabla_registro"])
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
                logger.info(time.ctime()+':\t'+"Registro:"+register_text[0]+"/"+str(quantity))
                output_writer.writerow(register_text)
    except Exception:
        logger.error("No se encuentran los registros/valores",exc_info=True)
        end_Execute()
        sys.exit()
    try:
        register_quantitys=driver.find_elements(By.XPATH,parameters["linea_cantidadReg"])
        register_quantity=driver.find_element(By.XPATH,parameters["linea_cantidadReg"]+'['+str(len(register_quantitys))+']/td/b')
        quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
        quantity=int(quantity)
        num_pages=math.ceil(quantity/30)
    except NoSuchElementException:
        logger.info(time.ctime()+':\t'+"terminado")
    logger.info(time.ctime()+':\t'+"pagina:"+str(index))
    index+=1
    register_time_end=timer()
    time_register.append(register_time_end-register_time_start)

logger.info(time.ctime()+':\t'+"Terminado con Exito")
end_Execute()


    # table_header=driver.find_element(By.CLASS_NAME,"provido_lista").find_elements(By.TAG_NAME,"th")
    # header_text=""
    # for header in table_header:
    #     header_text+=header.text+"|"
    # logger.info(header_text)
    # # table_body=driver.find_element(By.ID,"table1").find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")
    # # for element in table_body:
    # #     values=element.find_elements(By.TAG_NAME,"td")
    # #     value_text=""
    # #     for value in values:
    # #         value_text+=value.text+"|"
    # #     logger.info(value_text)


