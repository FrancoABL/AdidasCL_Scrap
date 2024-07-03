from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3")
#opts.add_argument("--headless")  # Esto sirve para que no abra la interfaz gráfica

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

def pop_pagina():
    pop_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[3]/div/div[5]/div/div/button")
    pop_button.click()
    sleep(3)  # wait for the page to load

def cambiar_pagina():
    #/html/body/div[2]/div/div[1]/div[1]/div/div/div[5]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div[4]/a
    next_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div/div/div[5]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div[4]/a/span")
    next_button.click()
    sleep(3)  # wait for the page to load

def scrollear():
    element = driver.find_element(By.TAG_NAME, 'body')
    veces_pagina_down = 0
    while True:
        element.send_keys(Keys.PAGE_DOWN)
        veces_pagina_down += 1
        sleep(2)
        
        # Verificar si hemos presionado PAGE_DOWN 10 veces
        if veces_pagina_down == 8:
            break

productos = []

driver.get('https://www.adidas.cl/zapatillas-hombre')

sleep(2)
scrollear()
sleep(2)

cambioPag = 35
while True:
    cambioPag= cambioPag-1
    titulos = driver.find_elements(By.XPATH, '//p[@data-auto-id="product-card-title"]')
    precios = driver.find_elements(By.XPATH, '//div[@data-auto-id="gl-price-item"]')

    for titulo, precio in zip(titulos, precios):
        productos.append({"Producto": titulo.text, "Precio": precio.text})
    if cambioPag == 34:
        cambiar_pagina()
        sleep(3)
        pop_pagina()
        sleep(3)
        scrollear()
        sleep(3)

    elif 34 >cambioPag > 0:
        cambiar_pagina()
        sleep(3)
        scrollear()
        sleep(3)
    elif cambioPag == 0:
        break

driver.quit()

# Guardar los resultados en un archivo CSV
with open('productos_adidas.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Producto", "Precio"])
    writer.writeheader()
    for producto in productos:
        writer.writerow(producto)

print("Los datos se han guardado en productos_adidas.csv")