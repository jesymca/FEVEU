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

    driver = None  # Inicializamos la variable 'driver' para evitar UnboundLocalError
    try:
        # 1. Inicializar el navegador
        print("Abriendo el navegador...")
        driver = webdriver.Firefox()

        # 2. Navegar a la página de login
        print("Navegando a la URL de login: https://fveu.nervana-consulting.com/#/")
        driver.get("https://fveu.nervana-consulting.com/#/")

        # 3. Pausa para login manual
        # Se solicita al usuario que inicie sesión manualmente.
        print("\n--- ¡PAUSA PARA EL LOGIN MANUAL! ---")
        print("Por favor, inicia sesión en el navegador con tus credenciales.")
        print("Una vez que hayas iniciado sesión y veas la página principal, presiona 'Enter' en esta terminal para continuar...")
        input("Presiona ENTER para continuar...")
        print("Continuando con la automatización...")

        wait = WebDriverWait(driver, 20)

        # 4. Leer los datos del archivo CSV
        df = pd.read_csv(CSV_FILE)
        print(f"Se encontraron {len(df)} usuarios en el archivo {CSV_FILE}.")

        # 5. Iterar sobre cada fila (usuario) del DataFrame
        for index, row in df.iterrows():
            # Volver a la página de registro después de cada usuario
            driver.get(REGISTRATION_URL)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Número de Cédula"]')))

            # Datos del Paso 1
            cedula = str(row['cedula'])
            nombres = row['nombres']
            apellidos = row['apellidos']
            telefono = str(row['telefono'])
            correo = row['correo']

            # Datos del Paso 2
            sede = row['sede']
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

                # --- SELECCIONAR EL ESTADO POR POSICIÓN (7mo elemento) ---
                print("Haciendo clic para abrir el menú del estado...")
                estado_field_control = driver.find_element(By.CSS_SELECTOR, '.q-field__control-container input[aria-label="Estado"]').find_element(By.XPATH, '..')
                estado_field_control.click()

                # Esperar a que los elementos del menú estén presentes y seleccionar el 7mo
                estado_options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.q-list--padding .q-item__label')))
                if len(estado_options) >= 7:
                    estado_options[6].click()  # [6] corresponde a la 7ma posición (índice 0)
                    print("Séptimo estado seleccionado con éxito.")
                else:
                    print("Error: No se encontraron suficientes opciones para el estado.")

                # --- HACER CLIC EN EL BOTÓN SIGUIENTE ---
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Siguiente')]]")))
                next_button.click()
                print("Haciendo clic en 'Siguiente'...")
                time.sleep(2) # Espera para la transición a la siguiente página/sección

                # --- PASO 2: Llenar la segunda parte del formulario ---
                print("Llenando la información académica (Paso 2)...")
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Sede"]')))

                sede_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Sede"]')
                carrera_select_field = driver.find_element(By.CSS_SELECTOR, '.q-field__control-container input[aria-label="Carrera"]').find_element(By.XPATH, '..')
                anio_semestre_select_field = driver.find_element(By.CSS_SELECTOR, '.q-field__control-container input[aria-label="Año o Semestre"]').find_element(By.XPATH, '..')
                materia1_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Materia 1"]')
                materia2_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Materia 2"]')

                # Limpiar y rellenar los campos
                sede_input.clear()
                sede_input.send_keys(sede)

                # SELECCIONAR LA CARRERA POR POSICIÓN (7mo elemento)
                carrera_select_field.click()
                carrera_options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.q-list--padding .q-item__label')))
                if len(carrera_options) >= 7:
                    carrera_options[6].click()
                    print("Séptima carrera seleccionada con éxito.")
                else:
                    print("Error: No se encontraron suficientes opciones para la carrera.")

                # SELECCIONAR EL AÑO O SEMESTRE POR POSICIÓN (7mo elemento)
                anio_semestre_select_field.click()
                anio_semestre_options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.q-list--padding .q-item__label')))
                if len(anio_semestre_options) >= 7:
                    anio_semestre_options[6].click()
                    print("Séptimo año/semestre seleccionado con éxito.")
                else:
                    print("Error: No se encontraron suficientes opciones para el año/semestre.")

                # Rellenar las materias
                materia1_input.clear()
                materia1_input.send_keys(materia1)
                materia2_input.clear()
                materia2_input.send_keys(materia2)

                # 7. Encontrar y hacer clic en el botón 'Guardar' para finalizar.
                save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Guardar')]]")))
                save_button.click()

                print("Formulario finalizado y enviado. Esperando la respuesta...")

                # 8. Esperar por la confirmación de registro
                time.sleep(3)
                print("Procesamiento del usuario completado.")

            except Exception as e:
                print(f"Ocurrió un error al procesar el usuario {correo}: {e}")
                continue

    except FileNotFoundError:
        print(f"Error: El archivo '{CSV_FILE}' no se encontró. Asegúrate de que existe en el mismo directorio que el script.")
    except Exception as e:
        print(f"Ocurrió un error general: {e}")
    finally:
        # 9. Cerrar el navegador al finalizar
        print("\nProceso de registro finalizado. Cerrando el navegador.")
        if driver:
            driver.quit()

if __name__ == "__main__":
    automate_registration()
