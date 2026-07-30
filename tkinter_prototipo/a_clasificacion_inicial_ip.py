from b_clasificacion_caracteristicas_ip import clasificacion_caracteristicas_ip
from tkinter import *
from tkinter import messagebox

octetos_ip = []

def procesamiento_direccion_ip(lista_octetos_ip, valor_prefijo):
    """
    Bucle en donde se ingresaran los valores de los octetos de IP
    """
    octetos_ip.clear()
    valor_ip = ""

    while True:
        try: 
            indice = 0
            for campo in lista_octetos_ip:
                valor_octeto = int(campo.get())

                #Validación de que el valor ingresado sea positivo
                if valor_octeto < 0:
                    messagebox.showwarning(title="Error - Valor númerico de Dirección IP",message="Ningún octeto de la dirección IP puede ser negativo.")
                    valor_ip = None
                    break
                elif indice == 0 and valor_octeto == 0:
                    messagebox.showwarning(title="Error - Valor númerico de Dirección IP",message="El primer octeto de la dirección IP debe ser mayor a 0.")
                    valor_ip = None
                    break
                else:
                    #Almacenamiento de valores de los octetos de IP
                    octetos_ip.append(valor_octeto)

                    #Generación de IP completa (contiendo sus cuatro octetos)
                    valor_ip += str(valor_octeto)
                    if indice < 3: 
                        valor_ip += "."
                indice += 1
            break
        except ValueError:
            #Validación para entradas no númericas
            messagebox.showwarning(title="Error - Valores de Dirección IP",message="No puedes ingresar valores no númericos ni octetos vacíos.")
            valor_ip = None
            break

    if valor_ip != None:
        #Clasificación de Clase de IP
        if octetos_ip[0] < 128:
            tipo_clase_ip = "A"
        elif octetos_ip[0] >= 128 and octetos_ip[0] < 192:
            tipo_clase_ip = "B"
        elif octetos_ip[0] >= 192 and octetos_ip[0] < 224:
            tipo_clase_ip = "C"
        else:
            tipo_clase_ip = "Clase no admitida"

        """
        Clasificación de IP
        """
        #Esta variable se usa para determinar los ocetos en donde no deben haber cambios respectos a los bits
        admision_valores_octeto = 0
        #Declaración de los valores máximo y mínimo que debe tener el prefijo de la IP
        valor_minimo_prefijo = 0
        valor_maximo_prefijo = 32 

        #Switch para determinar la Clase y los valores minimos del prefijo
        match tipo_clase_ip:
            case "A":
                admision_valores_octeto = 1
                valor_minimo_prefijo = 8
            case "B":
                admision_valores_octeto = 2
                valor_minimo_prefijo = 16
            case "C":
                admision_valores_octeto = 3
                valor_minimo_prefijo = 24
            case _:
                messagebox.showwarning(title="Error - Tipo de Dirección IP ingresada",message="Solo puede ingresar direcciones IP de clases: A - B - C. (Rango: 1.0.0.0 - 233.255.255.255).")

        if tipo_clase_ip != "Clase no admitida":
            #Ingreso y validación del prefijo ingresado (Tipo y Valor)
            while True:
                try:
                    prefijo_valor = int(valor_prefijo.get())

                    if prefijo_valor < 0:
                        messagebox.showwarning(title="Error - Valor de prefijo",message="El prefijo no puede ser negativo.")
                        break
                    elif prefijo_valor < valor_minimo_prefijo:
                        messagebox.showwarning(title="Error - Valor de prefijo",message=f"El prefijo mínimo para una IP clase {tipo_clase_ip} es de {valor_minimo_prefijo}.")
                        break
                    elif prefijo_valor > valor_maximo_prefijo:
                        messagebox.showwarning(title="Error - Valor de prefijo",message=f"El valor máximo para el prefijo es de {valor_maximo_prefijo}.")
                        break
                    else:
                        return clasificacion_caracteristicas_ip(octetos_ip, admision_valores_octeto, prefijo_valor)

                except ValueError:
                    #Validación para entradas no númericas
                    messagebox.showwarning(title="Error - Valor ingresado para prefijo",message="No puedes ingresar valores no númericos ni vacíos para el prefijo.")
                    break