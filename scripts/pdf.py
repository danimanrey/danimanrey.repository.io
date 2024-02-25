from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


def scrape_and_save_data(url):
    # Configurar el navegador
    driver = webdriver.Chrome()  # o el navegador de tu elección
    driver.get(url)

    # Lista para almacenar los datos
    datos = []

    try:
        while True:
            # Espera un breve momento para asegurarse de que la página se haya cargado completamente
            time.sleep(1)

            # Obtén los elementos de las columnas
            codigos = driver.find_elements(By.XPATH, '//*[@id="dt_productos"]/tbody/tr/td[1]')
            nombres = driver.find_elements(By.XPATH, '//*[@id="dt_productos"]/tbody/tr/td[2]')
            pdfs = driver.find_elements(By.XPATH, '//*[@id="dt_productos"]/tbody/tr/td[5]/a')

            # Itera sobre los elementos y guarda los datos en la lista
            for codigo, nombre, pdf in zip(codigos, nombres, pdfs):
                datos.append({
                    'Código': codigo.text,
                    'Nombre': nombre.text,
                    'PDF': f'{pdf.get_attribute("href")}' if pdf.get_attribute("href") else 'No disponible'
                })

            try:
                # Intenta encontrar el botón de siguiente y verificar si está deshabilitado
                boton_siguiente = driver.find_element(By.XPATH, '//*[@id="dt_productos_next"]')
                if 'disabled' in boton_siguiente.get_attribute('class'):
                    break  # Sale del bucle si el botón de siguiente está deshabilitado
                else:
                    boton_siguiente.click()
            except NoSuchElementException:
                break  # Sale del bucle si no se encuentra el botón de siguiente

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cierra el navegador al finalizar
        driver.quit()

        # Convierte la lista de datos en un DataFrame y guárdalo en un archivo CSV
        if datos:
            df = pd.DataFrame(datos)
            df.to_csv('discos.csv', index=False)

# Llamada a la función con la URL de la página web
url_pagina_web = "https://tracensl.com/familia/1/DISCOS-DE-CADENA"
scrape_and_save_data(url_pagina_web)
