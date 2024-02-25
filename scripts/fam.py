from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

def scrape_and_save_data(url, familia):
    # Configurar el navegador
    driver = webdriver.Chrome() 
    driver.get(url)
    
    # Lista para almacenar los datos
    datos = []

    try:
        while True:
            # Espera un breve momento para asegurarse de que la página se haya cargado completamente
            time.sleep(2)

            # Obtén los elementos de las columnas
            codigos = driver.find_elements(By.XPATH, '//*[@id="dt_productos"]/tbody/tr/th[1]')
            nombres = driver.find_elements(By.XPATH, '//*[@id="dt_productos"]/tbody/tr/th[2]')
            pdfs = driver.find_elements(By.XPATH, '//*[@id="dt_productos"]/tbody/tr/th[5]')

            # Itera sobre los elementos y guarda los datos en la lista
            for codigo, nombre, pdf in zip(codigos, nombres, pdfs):
                datos.append({
                    'Código': codigo.text,
                    'Nombre': nombre.text,
                    'PDF':f'{pdf.get_attribute("href")}' if pdf.get_attribute("href") else 'No disponible',
                    'Familia': familia 
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
        print(f"Error durante el scraping: {e}")

    finally:
        # Cierra el navegador al finalizar
        driver.quit()

        # Convierte la lista de datos en un DataFrame
        if datos:
            df = pd.DataFrame(datos)

            # Intenta guardar el DataFrame en un archivo CSV
            try:
                # Guarda el archivo CSV con el nombre de la familia en el nombre del archivo
                df.to_csv(f'{familia}_piñones.csv', index=False)
                print(f"Datos guardados correctamente en '{familia}_piñones.csv'")
            except Exception as e:
                print(f"Error al escribir el archivo CSV: {e}")

def scrape_for_each_family(familias_urls):
    for familia_url in familias_urls:
        familia_nombre = familia_url.split('/')[-2]  # Obtén el nombre de la familia de la URL
        scrape_and_save_data(familia_url, familia_nombre)

# Llamada a la función con la lista de URL de familias
familias_urls = ['https://tracensl.com/familia/7/PI%C3%91ONES-DE-CADENA-DIN8187-NORMA-ISO',
                  'https://tracensl.com/familia/101/PI%C3%91ONES-DE-CADENA-DIN-8188-NORMA-ASA',
                  'https://tracensl.com/familia/15/PI%C3%91ONES-DE-CADENA-',
                  "https://tracensl.com/familia/13/PI%C3%91ONES-DE-CADENA-",
                  "https://tracensl.com/familia/14/PI%C3%91ONES-DE-CADENA-",
                  "https://tracensl.com/familia/16/PI%C3%91ONES-",
                  "https://tracensl.com/familia/1/DISCOS-DE-CADENA",
                  "https://tracensl.com/familia/12/PI%C3%91ONES-TENSORES",
                  "https://tracensl.com/familia/10/RUEDAS-DE-FUNDICI%C3%93N",
                  "https://tracensl.com/familia/31/CORONAS-PARA-DOS-CADENAS-SIMPLES"]

scrape_for_each_family(familias_urls)
