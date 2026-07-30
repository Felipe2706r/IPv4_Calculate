from calculo_binario import calcular_numero_binario, calcular_numero_decimal
import sys

octetos_ip = []
valor_ip = ""

"""
Bucle en donde se ingresaran los valores de los octetos de IP
"""
while True:
    try: 
        for ite in range(4):
            valor_octeto = int(input(f"Ingresa el Octeto N°{ite+1} de la IP: "))

            #Validación de que el valor ingresado sea positivo
            while valor_octeto < 0:
                print("El valor no puede ser negativo")
                valor_octeto = int(input("Ingresa un valor valido: "))
            
            octetos_ip.append(valor_octeto)
            #Generación de IP completa (contiendo sus cuatro octetos)
            valor_ip += str(octetos_ip[ite])
            if ite < 3: 
                valor_ip += "."

        break
    except ValueError as e:
        #Validación para entradas no númericas
        print(f"Error, no puedes ingresar valores no númericos")

print("-----------------------------------------------------------------------")

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
        print("Clase no admitida")
        sys.exit()

#Ingreso y validación del prefijo ingresado (Tipo y Valor)
while True:
    try:
        prefijo_valor = int(input("Ingresa el prefijo necesario: "))

        if prefijo_valor < 0:
            print("El prefijo no puede ser negativo")
        elif prefijo_valor < valor_minimo_prefijo:
            print(f"El prefijo mínimo para una IP clase {tipo_clase_ip} es de {valor_minimo_prefijo}")
        elif prefijo_valor > valor_maximo_prefijo:
            print(f"El valor máximo para cualquier prefijo es de {valor_maximo_prefijo}")
        else:
            break

    except ValueError as e:
        #Validación para entradas no númericas
        print(f"Error, no puedes ingresar valores no númericos")

print("-----------------------------------------------------------------------")

"""
Obtención de parámetros de Red Completa
"""
#Instacia del valor del prefijo ingresado
bits_restantes_prefijo = prefijo_valor

#Declaración de variables para los valores buscados
valor_mascara_subred = ""
valor_direccion_red = ""
valor_red_broadcast = ""
valor_broadcast_completo = ""
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
            valor_red_broadcast += calcular_numero_decimal("".join(broadcast_red_octeto_binario))
            valor_broadcast_completo += calcular_numero_decimal("".join(broadcast_completo_octeto_binario))

        #Condición para agregar un punto entre los valores de los octetos
        if i < 3:
            valor_direccion_red += "."
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
#Calculo del número de subredes y número de hosts
num_subredes = 2 ** bits_porcion_subred
num_hosts = 2 ** bits_porcion_host - 2

print(f"Máscara de Subred: {valor_mascara_subred}")
print("Dirección de Red Completa:", valor_direccion_red)
print("Dirección de Broadcast:", valor_red_broadcast)
print("Dirección de Broadcast de Red Completa:", valor_broadcast_completo)
print("Número de Subredes:", num_subredes)
print("Número de Hosts:", num_hosts)