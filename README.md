# IPv4_Calculate

Este es un proyecto realizado con fines de apoyo y estudio académico dentro del contexto de aprendizaje y practica para Subnetting (Cálculo y división de redes) hecho en base a los siguientes componentes:
- Python: Lenguaje de Programación.
- Customtkinter: Biblioteca de uso para implementar GUI (Interfaz gráfica).
- Visual Studio Code: Entorno de Desarrollo y Prueba.
- Codex: Agente aútonomo utilizado para la realización de pruebas prácticas, correción de errores y desarrollo de código.
- Photopea y Canva: Plataformas de diseño y edición utilizadas para generar las imagenes de GUI e icono de aplicación.

## Objetivo

Implementar una herramienta simple de usar que cálcule y proporcione los siguientes datos:

- Máscara de subred.
- Dirección de red.
- Broadcast de red.
- Número de subredes.
- Número de hosts utilizables.
- Lista de subredes.
- Rango de uso de subred.
- Broadcast de subred.

Esto mediante el ingreso de la dirección IP y de un prefijo por parte del usuario.

## Estado actual

El proyecto se encuentra en una fase de desarrollo completa (estando abierta a la correción de errores) integrando el uso de una interfaz gráfica para el uso y experiencia de usuario junto a la implementación de lógica de programación para realización de calculos y obtención de valores.

Características de Interfaz Gráfica:
1. Realizada en base a la biblioteca integrada **Customtkinter**, en conjunto con otras bibliotecas (principalmente **Pillow** y **Pathlib**).
2. Imagenes gráficas realizas en la plataforma **Canva**.
3. Implementación de: Etiquetas, Campos de entrada y Salidas, Mensajes de advertencia y suceción de eventos.
4. Uso de botones de acción para disparar la ejecución de funciones.

## Pasos para ejecución

1. Instalar las dependencias externas desde la raíz del proyecto:
   ```bash
   python -m pip install -r requirements.txt
   ```
De no usar este metodo, instalar dependencias de forma manual desde CLI:
   ```bash
   python -m pip install Pillow
   ```
   ```bash
   python -m pip install customtkinter
   ```
2. Ejecutar el módulo principal de la interfaz en la la raíz del proyecto::
   ```bash
   python pantalla_principal.py
   ``` 
3. Ingresar la Dirección IP y el Prefijo en los campos correspondientes de la pantalla principal.

4. Ejecutar la acción de cálculo disponible desde el botón con título **Calcular Valores** para obtener los resultados.

## Estructura de repositorio

**Aplicación de Uso (Raíz de repositorio)**
- **pantalla_principal**: Pantalla principal de la aplicación con campos de entrada necesarios (Dirección IP y Prefijo) y botones de ejecución (Calcular Valores, Limpiar Campos y Lista de Subredes).
- **ventana_lista_subredes**: Pantalla que muestra una tabla que contiene la lista de subredes generadas en base al calculo de valores de una dirección IP ingresada.
- **calculos_ipv4**: Calculo de datos particulares de datos particulares de Dirección IP en el objetivo del proyecto en base al uso de librerias externas y lógica interna. 
- [recursos_graficos](recursos_graficos): Contiene las imágenes utilizadas para la interfaz gráfica de la aplicación (Pantalla principal y pantalla de subredes.).

**Prototipo de GUI (/tkinter_prototipo)**
- [tkinter_prototipo](tkinter_prototipo): Carpeta almacenadora de scripts en Python e imagenes de uso para interfaz.
- **prueba_pantalla_principal**: Muestra de pantalla principal de la aplicación con los campos de entrada necesarios (Dirección IP y Prefijo).
- **pantalla_lista_subredes**: Apertura de pantalla de menor medida que muestra la lista de subredes calculadas en base a la Dirección IP ingresada.
- **a_clasificacion_inicial_ip**: Clasificación de Clase de Dirección IP y validación de valor de prefijo.
- **b_clasificacion_caracteristicas_ip**: Cálculo de datos particulares de Dirección IP establecidos en el objetivo del proyecto. Retorna los mismos en una lista.
- **c_calculo_valores_subredes**: Cálculo de lista de subredes, rango de uso y broadcast de subred internamente. Retorna los valores en una lista compuesta.
- **d_calculo_binario**: Cálculo números en notación decimal y binario mediante funciones.

**Prototipo (/scripts_prototipo)**
- [scripts_prototipo](scripts_prototipo): Carpeta almacenadora de scripts en Python.
- **1.validacion_inicial_prototipo**: Ingreso y clasificación de Clase de Dirección IP.
- **2.mascara_subred_prototipo**: Cálculo y muestra de máscara de subred de Dirección IP.
- **3.red_broadcast_completos**: Cálculo y muestra de datos particulares de Dirección IP establecidos en el objetivo del proyecto.
- **4.lista_subredes_inicio_broadcast**: Cálculo y muestra de datos particulares, junto con la muestra de: Lista de subredes, Rango de uso y Broadcast de Subred.
- **calculo_binario**: Cálculo de lista de subredes, rango de uso y broadcast de subred. Retorna los mismos mediante listas.
- **calculo_valores_subredes**: Cálculo números en notación decimal y binario mediante funciones..
