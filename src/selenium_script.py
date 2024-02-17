#hello.py
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import math
import timeit


'''
Control de errores (que no se desplome y muestre en que página se cayó)
Log de detalles
Input MES a MES
Plantilla de XPATH (HTML de ejemplo), lo cargamos , cuando se hace la referencia
Archivo de configuración:
    tabla_login:/html/body/div[1]/div/div/div[7]/div/div/div/div/div/div[2]/div[3]/div/article/article[1]/p[14]
    tabla_decretos:/html/body/div[1]/div/div/div[7]/div/div/div/div/div/div[2]/div[3]/div/article/article[1]/p[13]
Ya no cargarlo a TXT sino CSV
'''






# driver.get("https://www.selenium.dev/selenium/web/web-form.html")
# driver.get("https://www.selenium.dev/selenium/web/linked_image.html")
# service = webdriver.ChromeService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)
# title = driver.title
# driver.implicitly_wait(10)


# Retrieves the text of the element
#text = driver.find_element(By.NAME, "my-select").find_elements(By.TAG_NAME,"option")

# text = driver.find_element(By.NAME,"my-readonly").get_attribute("value")
# print(text)
# button=driver.find_element(By.TAG_NAME,"button")
# button.click()
# text = driver.find_element(By.ID,"message").text
# print(text)
driver=webdriver.Chrome()
#driver=webdriver.Firefox()
driver.get("https://easprep.osce.gob.pe/portaltribunal-uiwd-pub/Logout")
#service = webdriver.ChromeService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)
service = webdriver.FirefoxService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)
file_output=open("output.txt","a")

driver.implicitly_wait(10)

start_script=timeit.timeit()

user_element=driver.find_element(By.NAME,"usuario")
pass_element=driver.find_element(By.NAME,"senha")

user_element.send_keys("nprieto")
pass_element.send_keys("123")

#print(user_element.get_attribute("value"))
#print(pass_element.get_attribute("value"))

arr_btn=driver.find_elements(By.TAG_NAME,"INPUT")

for btn in arr_btn:
    value=btn.get_attribute("VALUE")
    if value=="Iniciar Sesión":
        submit_btn=btn
        break

#print(submit_btn.get_attribute("VALUE"))
submit_btn.click()

list_options=driver.find_elements(By.TAG_NAME,"li")

for option in list_options:
    print(option.text)
    if option.text=="Reportes":
        select_option=option
        break

select_option.click()
list_options=driver.find_elements(By.TAG_NAME,"li")
for option in list_options:
    if option.text=="Reporte de Decretos":
        select_option=option
        break

select_option.click()


list_status=driver.find_element(By.ID,"estado")
select_status=Select(list_status)
select_status.select_by_visible_text("Pendiente")

fecha_inicio=driver.find_element(By.NAME,"FE_REGISTRO_INICIO")
fecha_fin=driver.find_element(By.NAME,"FE_REGISTRO_FIN")

fecha_inicio.send_keys("01/02/2024")
fecha_fin.send_keys("09/02/2024")

btn_Buscar=driver.find_element(By.ID,"Buscar")
btn_Buscar.click()

start_registers=timeit.timeit()
time_register=[]

tabla_body=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
lista_cabecera=tabla_body.find_elements(By.TAG_NAME,"th")
cabecera_text=""
for cabecera in lista_cabecera:
    if cabecera.text != "":
        cabecera_text+=cabecera.text+","
file_output.write(cabecera_text+"\n")
try:
    register_quantitys=driver.find_elements(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]/tbody/tr')
    print(len(register_quantitys))
    register_quantity=driver.find_elements(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]/tbody/tr['+len(register_quantitys)+']/td/b')
    quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
    quantity=int(quantity)
    quantity=math.ceil(quantity/30)
    print(quantity)
except NoSuchElementException:
    print("Alejo")

""" 
# lista_paginas=[]

# list_paginas=driver.find_element(By.ID,"Pagina")
# select_pagina=Select(list_paginas)
# list_paginas_options=select_pagina.options
# # for option in list_paginas_options:
# #     lista_paginas.append(option.get_attribute("value"))
# # print(lista_paginas[-1])

index=1
while index<=quantity:
    list_paginas=driver.find_element(By.ID,"Pagina")
    select_pagina=Select(list_paginas)
    select_pagina.select_by_value(str(index))
    tabla_body=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
    tabla_registers=tabla_body.find_elements(By.TAG_NAME,"tr")
    register_time_start=timeit.timeit()
    for register in tabla_registers:
        tabla_data=register.find_elements(By.TAG_NAME,"td")
        register_text=""
        for data in tabla_data:
            if not "total de registros" in data.text and not "Pagina" in data.text:
                register_text+=data.text+','
        print(register_text)
        if register_text != "":
            file_output.write(register_text+"\n")
    try:
        register_quantity=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]/tbody/tr[32]/td/b')
        quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
        quantity=int(quantity)
        quantity=math.ceil(quantity/30)
    except NoSuchElementException:
        print("terminado")
    index+=1
    register_time_end=timeit.timeit()
    time_register.append(register_time_end-register_time_start)

end_script=timeit.timeit()
file_output.close()       

print("Start time:",start_script)
print("Prepare time:",start_registers-start_script)
print("Registers time (avg):",sum(time_register)/len(time_register))
print("End time:" , end_script)
print("Total time:", end_script-start_script)

# table_header=driver.find_element(By.CLASS_NAME,"provido_lista").find_elements(By.TAG_NAME,"th")
# header_text=""
# for header in table_header:
#     header_text+=header.text+"|"
# print(header_text)
# # table_body=driver.find_element(By.ID,"table1").find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")
# # for element in table_body:
# #     values=element.find_elements(By.TAG_NAME,"td")
# #     value_text=""
# #     for value in values:
# #         value_text+=value.text+"|"
# #     print(value_text)



 """