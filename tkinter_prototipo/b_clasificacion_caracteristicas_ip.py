from d_calculo_binario import calcular_numero_binario, calcular_numero_decimal
from c_calculo_valores_subredes import calcular_valores_subred, calcular_broadcast_red_siguiente
from tkinter import *

valor_ip = ""

def clasificacion_caracteristicas_ip(octetos_ip, admision_valores_octeto, prefijo_valor):
    """
    Obtención de parámetros de Red Completa
    """
    #Instacia del valor del prefijo ingresado
    bits_restantes_prefijo = prefijo_valor

    #Declaración de variables para los valores buscados
    valor_mascara_subred = ""
    valor_direccion_red = ""
    valor_direccion_red_completa = ""

    valor_red_broadcast = ""
    valor_broadcast_completo = ""
    valor_broadcast_red_completa = ""

    num_subredes = 0
    num_hosts = 0

    bits_octeto_actual = 0
    resto_bits_octeto = 0
    #Variables para contar los bits de las porciones de subred y host en uno o más octetos
    bits_porcion_subred = 0
    bits_porcion_host = 0

    #Bucle para recorrer los octetos de la IP
    for i in range(4):
        octeto_presente = ""

        #Se agregara el valor decimal del octeto al resultado final en caso
        #de que el mismo se encuentre en el rango de admisión establecido
        if i < admision_valores_octeto:
            valor_direccion_red += str(octetos_ip[i]) + "."
            valor_direccion_red_completa = valor_direccion_red
            valor_red_broadcast = valor_direccion_red
            valor_broadcast_completo = valor_direccion_red

            bits_octeto_actual = 8
            bits_restantes_prefijo -= 8 #Se restan los bits correspondientes al octeto
        else:
            #Se ejecutara esta sección tras acabarse el rango de admisión de los octetos

            #Se convierte el octeto presente (en valores decimales) a número binario, los cuales se almacenaran el listas.
            #Se almacena en los tres valores que buscamos.
            direccion_octeto_binario = list(calcular_numero_binario(octetos_ip[i]))
            broadcast_red_octeto_binario = list(calcular_numero_binario(octetos_ip[i]))
            broadcast_completo_octeto_binario = list(calcular_numero_binario(octetos_ip[i]))

            #Esta sección se ejecutara en de que el prefijo no afecte la composición del valor del octeto presente
            if bits_restantes_prefijo >= 8:
                #Se determina el número de bits (1) del octeto presente
                bits_octeto_actual = 8

                #Se le restara 8 al prefijo determinando que ya se ha establecido un octeto de la máscara
                bits_restantes_prefijo -= 8

                #Variable para determinar el número de bits no activos (0) de un octeto
                resto_bits_octeto = 0

                #Se agrega el número en decimal al los valores buscados, esto al no tener que modificarlo
                valor_direccion_red += str(octetos_ip[i])
                valor_direccion_red_completa = valor_direccion_red
                valor_red_broadcast = valor_direccion_red
                valor_broadcast_completo = valor_direccion_red
            #Esta sección se ejecutara cuando el prefijo este a punto de acabarse y deba establecerse su límite en el octeto presente
            elif bits_restantes_prefijo < 8 and bits_restantes_prefijo > 0:
                #Se establece el número de bits activos (1) y no activos (0) del octeto
                bits_octeto_actual = bits_restantes_prefijo
                resto_bits_octeto = 8 - bits_octeto_actual
                bits_porcion_subred = bits_octeto_actual
                bits_porcion_host += resto_bits_octeto

                #Establecemos los bits de la porción de Subred
                # De valor 0 para calcular la red completa
                # De valor 1 para calcular la dirección de broadcast de red
                for j in range(resto_bits_octeto):
                    direccion_octeto_binario[bits_octeto_actual + j] = "0"
                    broadcast_red_octeto_binario[bits_octeto_actual + j] = "1"

                #Convertimos los números binarios calculados en valores decimales, para seguido almacenarlos en sus respectivos valores
                valor_direccion_red += calcular_numero_decimal("".join(direccion_octeto_binario))
                valor_direccion_red_completa += "0" #Se añade un 0 al deber estar el octeto libre y comenzar la red completa desde el principio
                valor_red_broadcast += calcular_numero_decimal("".join(broadcast_red_octeto_binario))

                #Establecemos nuevamente los bits de la porción de Subred
                # En este caso, cambiaremos todos los bits del octeto a 1 para calcular el broadcast completo
                for j in range(bits_octeto_actual + resto_bits_octeto):
                    broadcast_completo_octeto_binario[j] = "1"
                valor_broadcast_completo += calcular_numero_decimal("".join(broadcast_completo_octeto_binario))

                #Se establece en 0 el prefijo en caso de ya haberse establecido todos los bits activos
                bits_restantes_prefijo = 0
            #Esta sección se ejecutara cuando ya se haya pasado el establecimiento del prefijo
            else:
                #Los bits no activos (0) ocuparan todo el octeto mediante su respectiva variable
                bits_octeto_actual = 0
                resto_bits_octeto = 8
                bits_porcion_host += resto_bits_octeto

                #Repetimos nuevamente el establecimiento des bits de la porción de Subred
                # Aquí se hara para todo el octeto con los bits de sus valores respectivos
                for j in range(resto_bits_octeto):
                    direccion_octeto_binario[j] = "0"
                    broadcast_red_octeto_binario[j] = "1"
                    broadcast_completo_octeto_binario[j] = "1"
                valor_direccion_red += calcular_numero_decimal("".join(direccion_octeto_binario))
                valor_direccion_red_completa += "0" #Se añade un 0 al deber estar el octeto libre y comenzar la red completa desde el principio
                valor_red_broadcast += calcular_numero_decimal("".join(broadcast_red_octeto_binario))
                valor_broadcast_completo += calcular_numero_decimal("".join(broadcast_completo_octeto_binario))

            #Condición para agregar un punto entre los valores de los octetos
            if i < 3:
                valor_direccion_red += "."
                valor_direccion_red_completa += "."
                valor_red_broadcast += "."
                valor_broadcast_completo += "."

        #Formación del octeto presente de la máscara de subred según los bits disponibles
        for j in range(bits_octeto_actual):
            octeto_presente += "1"
        for k in range(resto_bits_octeto):
            octeto_presente += "0"

        #Conversión del octeto a número decimal
        valor_mascara_subred += calcular_numero_decimal(octeto_presente)
        if i < 3:
            valor_mascara_subred += "."

    valor_broadcast_red_completa = calcular_broadcast_red_siguiente(valor_direccion_red_completa, prefijo_valor, admision_valores_octeto)
    #Calculo del número de subredes y número de hosts
    num_subredes = 2 ** bits_porcion_subred
    num_hosts = 2 ** bits_porcion_host - 2

    lista_valores_direccion_ip = [valor_mascara_subred, valor_direccion_red, valor_red_broadcast, num_hosts] 

    #print("Lista de Subredes Disponibles")
    lista_valores_subredes = calcular_valores_subred(valor_direccion_red_completa, valor_broadcast_red_completa, valor_broadcast_completo, prefijo_valor, False, [])
    return lista_valores_direccion_ip, lista_valores_subredes