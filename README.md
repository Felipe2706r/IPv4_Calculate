# IPv4_Calculate

Este es un proyecto realizado con fines de apoyo y estudio académico dentro del contexto de aprendizaje y practica para Subnetting (Cálculo y división de redes) hecho en base a los siguientes componentes:
- Python: Lenguaje de Programación.
- Tkinter: Biblioteca de uso para implementar GUI (Interfaz gráfica).
- Visual Studio Code: Entorno de Desarrollo y Prueba.
- Codex: Agente aútonomo utilizado para la realización de pruebas prácticas, correción de errores y desarrollo de código.

## Objetivo

Implementar una herramienta simple de usar que cálcule y proporcione los siguientes datos:

- Máscara de subred.
- Dirección de red.
- Broadcast de red.
- Número de subredes.
- Número de hosts
- Lista de subredes.
- Rango de uso de subred.
- Broadcast de subred.

Esto mediante el ingreso de la dirección IP y de un prefijo por parte del usuario.

## Estado actual

El proyecto se encuentra en fase de prototipo funcional de cálculo con una interfaz gráfica simple realizada con el proposito de funcionar como boceto para la versión final.

Características de Interfaz Gráfica:
1. Realizada en base a la biblioteca integrada **Tkinter**.
2. Implementación de etiquetas, campos de entrada y mensajes de advertencia.
3. Uso de botones de acción para disparar la ejecución de funciones.

## Pasos para ejecución

1. Instalar las dependencias externas desde la raíz del proyecto:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Ejecutar el módulo principal de la interfaz:
   ```bash
   python tkinter_prototipo/prueba_pantalla_principal.py
   ```
3. Ingresar la Dirección IP y el Prefijo en los campos correspondientes de la pantalla principal.

4. Ejecutar la acción de cálculo disponible desde el botón con título **Calcular** para obtener los resultados.

## Estructura de repositorio

**Prototipo de GUI (/tkinter_prototipo)**
- [tkinter_prototipo](tkinter_prototipo): Carpeta almacenadora de scripts en Python e imagenes de uso para interfaz.
- **prueba_pantalla_principal**: Muestra de pantalla principal de la aplicación con campos de entrada necesarios (Dirección IP y Prefijo).
- **pantalla_lista_subredes**: Apertura de pantalla de menor medida que muestra la lista de subredes calculadas en base a Dirección IP ingresada.
- **a_clasificacion_inicial_ip**: Clasificación de Clase de Dirección IP y validación de valor de prefijo.
- **b_clasificacion_caracteristicas_ip**: Cálculo de datos particulares de datos particulares de Dirección IP en el objetivo del proyecto y retorno de los mismos en una lista.
- **c_calculo_valores_subredes**: Cálculo de lista de subredes, rango de uso y broadcast de subred y retorno de los valores en una lista compuesta.
- **d_calculo_binario**: Cálculo números en notación decimal y binario.

**Prototipo (/scripts_prototipo)**
- [scripts_prototipo](scripts_prototipo): Carpeta almacenadora de scripts en Python.
- **1.validacion_inicial_prototipo**: Ingreso y clasificación de Clase de Dirección IP.
- **2.mascara_subred_prototipo**: Cálculo y muestra de máscara de subred de Dirección IP.
- **3.red_broadcast_completos**: Cálculo y muestra de datos particulares de Dirección IP en el objetivo del proyecto.
- **4.lista_subredes_inicio_broadcast**: Cálculo y muestra de datos particulares junto con muestra de lista de subredes, rango de uso y broadcast de subred.
- **calculo_binario**: Cálculo de lista de subredes, rango de uso y broadcast de subred.
- **calculo_valores_subredes**: Cálculo números en notación decimal y binario.
