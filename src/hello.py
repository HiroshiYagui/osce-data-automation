#hello.py
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import math
 

driver=webdriver.Chrome()

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

driver.get("https://easprep.osce.gob.pe/portaltribunal-uiwd-pub/Logout")
service = webdriver.ChromeService(service_args=['--log-level=ALL'], log_output=subprocess.STDOUT)

file_output=open("output.txt","a")

driver.implicitly_wait(10)

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

fecha_inicio.send_keys("01/01/2024")
fecha_fin.send_keys("09/02/2024")

btn_Buscar=driver.find_element(By.ID,"Buscar")
btn_Buscar.click()


tabla_body=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
lista_cabecera=tabla_body.find_elements(By.TAG_NAME,"th")
cabecera_text=""
for cabecera in lista_cabecera:
    if cabecera.text != "":
        cabecera_text+=cabecera.text+","
file_output.write(cabecera_text+"\n")

register_quantity=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]/tbody/tr[32]/td/b')
quantity=register_quantity.text[register_quantity.text.find(": ")+2:]
quantity=int(quantity)
quantity=math.ceil(2723/30)
print(quantity)

# lista_paginas=[]

# list_paginas=driver.find_element(By.ID,"Pagina")
# select_pagina=Select(list_paginas)
# list_paginas_options=select_pagina.options
# # for option in list_paginas_options:
# #     lista_paginas.append(option.get_attribute("value"))
# # print(lista_paginas[-1])
for number_option in range(1,quantity):
    list_paginas=driver.find_element(By.ID,"Pagina")
    select_pagina=Select(list_paginas)
    select_pagina.select_by_value(str(number_option))
    tabla_body=driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div/div/table/tbody/tr[2]/td/table[3]')
    tabla_registers=tabla_body.find_elements(By.TAG_NAME,"tr")
    for register in tabla_registers:
        tabla_data=register.find_elements(By.TAG_NAME,"td")
        register_text=""
        for data in tabla_data:
            if not "total de registros" in data.text and not "Pagina" in data.text:
                register_text+=data.text+','
        print(register_text)
        if register_text != "":
            file_output.write(register_text+"\n")


file_output.close()        

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



