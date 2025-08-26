# -*- coding: utf-8 -*-
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- CONFIGURACIÓN ---
# La ruta de la web de registro
REGISTRATION_URL = "https://fveu.nervana-consulting.com/#/registrar"
# La ruta de tu archivo CSV
CSV_FILE = "usuarios.csv"

# Aquí se define el formato de los datos en el CSV.
# El archivo usuarios.csv debe tener estas columnas.
# Ejemplo de contenido de 'usuarios.csv' con los nuevos campos:
"""
cedula,nombres,apellidos,telefono,correo,estado,sede,carrera,anio_semestre,materia1,materia2
12345678,Juan,Perez,04121234567,juan.perez@email.com,Distrito Capital,Sede A,Ingeniería de Sistemas,2do Semestre,Materia A,Materia B
87654321,Maria,Garcia,04147654321,maria.garcia@email.com,Miranda,Sede B,Medicina,4to Año,Materia C,Materia D
"""

def automate_registration():
    """
    Automatiza el proceso de registro de usuarios leyendo datos desde un CSV.
    """
    print("Iniciando la automatización de registro...")

    try:
        # 1. Leer los datos del archivo CSV
        df = pd.read_csv(CSV_FILE)
        print(f"Se encontraron {len(df)} usuarios en el archivo {CSV_FILE}.")

        # 2. Inicializar el navegador
        print("Abriendo el navegador...")
        # Usa el Geckodriver para Firefox.
        driver = webdriver.Firefox()

        # 3. Navegar a la página de registro
        driver.get(REGISTRATION_URL)
        print(f"Navegando a la URL: {REGISTRATION_URL}")

        # 4. Esperar a que la página cargue y el formulario del paso 1 esté visible.
        wait = WebDriverWait(driver, 20)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Número de Cédula"]')))
            print("El formulario del Paso 1 está visible.")
        except Exception:
            print("¡Error! No se pudo encontrar el formulario del Paso 1. Verifica los selectores.")
            driver.quit()
            return

        # 5. Iterar sobre cada fila (usuario) del DataFrame
        for index, row in df.iterrows():
            # Datos del Paso 1
            cedula = str(row['cedula'])
            nombres = row['nombres']
            apellidos = row['apellidos']
            telefono = str(row['telefono'])
            correo = row['correo']
            estado = row['estado']

            # Datos del Paso 2
            sede = row['sede']
            carrera = row['carrera']
            anio_semestre = row['anio_semestre']
            materia1 = row['materia1']
            materia2 = row['materia2']

            print(f"\nProcesando usuario {index + 1}: {nombres} {apellidos} ({correo})")

            try:
                # --- PASO 1: Llenar la primera parte del formulario ---
                cedula_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Número de Cédula"]')
                nombres_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Nombres"]')
                apellidos_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Apellidos"]')
                telefono_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Teléfono Celular"]')
                correo_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Correo Electrónico"]')

                cedula_input.clear()
                cedula_input.send_keys(cedula)
                time.sleep(2) # Espera a que el sitio web valide la cédula y active los campos

                nombres_input.send_keys(nombres)
                apellidos_input.send_keys(apellidos)
                telefono_input.send_keys(telefono)
                correo_input.send_keys(correo)

                # Seleccionar el estado del menú desplegable
                estado_select = driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Estado"]')
                estado_select.click()
                estado_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'q-item__label') and contains(text(), '{estado}')]")))
                estado_option.click()

                # Hacer clic en el botón para avanzar al siguiente paso
                # Nota: Asumo que existe un botón 'Siguiente' o 'Continuar'.
                # Si no existe y el avance es automático al llenar los campos, se omite este paso.
                # Basado en tu HTML, el botón de guardado está deshabilitado. Se buscará el botón que lo habilita.
                # Si hay un botón "Siguiente", usaría:
                # next_button = driver.find_element(By.XPATH, "//button[span[contains(text(), 'Siguiente')]]")
                # next_button.click()
                # De momento, el script asume que los campos del Paso 2 se habilitan en la misma página.

                # --- PASO 2: Llenar la segunda parte del formulario ---
                print("Llenando la información académica (Paso 2)...")
                # Esperar a que el campo 'Sede' esté visible antes de continuar
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Sede"]')))

                sede_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Sede"]')
                carrera_select = driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Carrera"]')
                anio_semestre_select = driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Año o Semestre"]')
                materia1_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Materia 1"]')
                materia2_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Materia 2"]')

                # Limpiar y rellenar los campos
                sede_input.clear()
                sede_input.send_keys(sede)

                # Seleccionar la Carrera
                carrera_select.click()
                carrera_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'q-item__label') and contains(text(), '{carrera}')]")))
                carrera_option.click()

                # Seleccionar el Año o Semestre
                anio_semestre_select.click()
                anio_semestre_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'q-item__label') and contains(text(), '{anio_semestre}')]")))
                anio_semestre_option.click()

                # Rellenar las materias
                materia1_input.clear()
                materia1_input.send_keys(materia1)
                materia2_input.clear()
                materia2_input.send_keys(materia2)

                # 7. Encontrar y hacer clic en el botón 'Guardar' para finalizar.
                # El botón de guardar se habilitará una vez que todos los campos estén llenos.
                # Se espera a que el botón ya no esté deshabilitado.
                save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Guardar')]]")))
                save_button.click()

                print("Formulario finalizado y enviado. Esperando la respuesta...")

                # 8. Esperar por la confirmación de registro
                time.sleep(3)
                print("Procesamiento del usuario completado.")

            except Exception as e:
                print(f"Ocurrió un error al procesar el usuario {correo} en el paso 2: {e}")
                continue

    except FileNotFoundError:
        print(f"Error: El archivo '{CSV_FILE}' no se encontró. Asegúrate de que existe en el mismo directorio que el script.")
    except Exception as e:
        print(f"Ocurrió un error general: {e}")
    finally:
        # 9. Cerrar el navegador al finalizar
        print("\nProceso de registro finalizado. Cerrando el navegador.")
        driver.quit()

if __name__ == "__main__":
    automate_registration()
