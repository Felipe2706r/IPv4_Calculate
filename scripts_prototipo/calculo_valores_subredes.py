from calculo_binario import calcular_numero_binario, calcular_numero_decimal
import sys

def separar_octetos(conjunto_ingresado):
    caracteres_ip_subred = list(conjunto_ingresado)
    octetos_ip = []
    limite_inicio_ip = 0

    """
    Bucle en donde se separan los octetos de la IP ingresada
    """
    for i in range(4):
        octeto_actual = ""
        for j in range(limite_inicio_ip, len(conjunto_ingresado)):
            if caracteres_ip_subred[j] == ".":
                limite_inicio_ip = j + 1
                octetos_ip.append(int(octeto_actual))
                break
            elif j == (len(conjunto_ingresado) - 1):
                octeto_actual += caracteres_ip_subred[j]
                octetos_ip.append(int(octeto_actual))
                break
            else:
                octeto_actual += caracteres_ip_subred[j]
    return octetos_ip


def calcular_broadcast_red_siguiente(subred_siguiente, prefijo_valor, admision_valores_octeto):
    octetos_ip = []
    #octetos_broadcast_subred = []
    octetos_ip = separar_octetos(subred_siguiente)
    #octetos_broadcast_subred = separar_octetos(broadcast_red)

    """
    Obtención de parámetros de Red Completa
    """
    #Instacia del valor del prefijo ingresado
    bits_restantes_prefijo = prefijo_valor

    #Declaración de variables para los valores buscados
    valor_direccion_red = ""
    valor_red_broadcast = ""

    #Bucle para recorrer los octetos de la IP
    for i in range(4):
        #Se agregara el valor decimal del octeto al resultado final en caso
        #de que el mismo se encuentre en el rango de admisión establecido
        if i < admision_valores_octeto:
            valor_direccion_red += str(octetos_ip[i]) + "."
            valor_red_broadcast = valor_direccion_red

            bits_restantes_prefijo -= 8 #Se restan los bits correspondientes al octeto
        else:
            #Se ejecutara esta sección tras acabarse el rango de admisión de los octetos

            #Se convierte el octeto presente (en valores decimales) a número binario, los cuales se almacenaran el listas.
            #Se almacena en los tres valores que buscamos.
            direccion_octeto_binario = list(calcular_numero_binario(octetos_ip[i]))
            broadcast_red_octeto_binario = list(calcular_numero_binario(octetos_ip[i]))

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
            #Esta sección se ejecutara cuando el prefijo este a punto de acabarse y deba establecerse su límite en el octeto presente
            elif bits_restantes_prefijo < 8 and bits_restantes_prefijo > 0:
                #Se establece el número de bits activos (1) y no activos (0) del octeto
                bits_octeto_actual = bits_restantes_prefijo
                resto_bits_octeto = 8 - bits_octeto_actual
                bits_porcion_subred = bits_octeto_actual

                #Establecemos los bits de la porción de Subred
                # De valor 0 para calcular la red completa
                # De valor 1 para calcular la dirección de broadcast de red y la dirección de subred siguiente
                for j in range(resto_bits_octeto):
                    direccion_octeto_binario[bits_octeto_actual + j] = "0"
                    broadcast_red_octeto_binario[bits_octeto_actual + j] = "1"

                #Convertimos los números binarios calculados en valores decimales, para seguido almacenarlos en sus respectivos valores
                valor_direccion_red += calcular_numero_decimal("".join(direccion_octeto_binario))
                valor_red_broadcast += calcular_numero_decimal("".join(broadcast_red_octeto_binario))
                
                #Se establece en 0 el prefijo en caso de ya haberse establecido todos los bits activos
                bits_restantes_prefijo = 0
            #Esta sección se ejecutara cuando ya se haya pasado el establecimiento del prefijo
            else:
                #Los bits no activos (0) ocuparan todo el octeto mediante su respectiva variable
                bits_octeto_actual = 0
                resto_bits_octeto = 8

                #Repetimos nuevamente el establecimiento des bits de la porción de Subred
                # Aquí se hara para todo el octeto con los bits de sus valores respectivos
                for j in range(resto_bits_octeto):
                    direccion_octeto_binario[j] = "0"
                    broadcast_red_octeto_binario[j] = "1"

                valor_direccion_red += calcular_numero_decimal("".join(direccion_octeto_binario))
                valor_red_broadcast += calcular_numero_decimal("".join(broadcast_red_octeto_binario))

            #Condición para agregar un punto entre los valores de los octetos
            if i < 3: 
                valor_direccion_red += "."
                valor_red_broadcast += "."
    return valor_red_broadcast

def calcular_valores_subred(subred_ingresada, broadcast_red, broadcast_completo, prefijo_usado, paso_dado):
    if paso_dado == False:    
        octetos_ip = []
        octetos_broadcast_subred = []
        octetos_ip = separar_octetos(subred_ingresada)
        octetos_broadcast_subred = separar_octetos(broadcast_red)

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

        #Switch para determinar la Clase y los valores minimos del prefijo
        match tipo_clase_ip:
            case "A":
                admision_valores_octeto = 1
            case "B":
                admision_valores_octeto = 2
            case "C":
                admision_valores_octeto = 3
            case _:
                print("Clase no admitida")
                sys.exit()

        #Ingreso y validación del prefijo ingresado (Tipo y Valor)
        prefijo_valor = prefijo_usado

        """
        Obtención de parámetros de Red Completa
        """
        #Instacia del valor del prefijo ingresado
        bits_restantes_prefijo = prefijo_valor

        #Declaración de variables para los valores buscados
        valor_direccion_red = ""
        valor_red_broadcast = ""
        valor_subred_siguiente = ""
        valor_direccion_puerta_enlace = ""
        valor_direccion_ultima_utilizable = ""

        #Bucle para recorrer los octetos de la IP
        for i in range(4):
            #Se agregara el valor decimal del octeto al resultado final en caso
            #de que el mismo se encuentre en el rango de admisión establecido
            if i < admision_valores_octeto:
                valor_direccion_red += str(octetos_ip[i]) + "."
                valor_red_broadcast = valor_direccion_red
                valor_subred_siguiente = valor_direccion_red
                valor_direccion_puerta_enlace = valor_direccion_red
                valor_direccion_ultima_utilizable = valor_direccion_red

                bits_restantes_prefijo -= 8 #Se restan los bits correspondientes al octeto
            else:
                #Se ejecutara esta sección tras acabarse el rango de admisión de los octetos

                #Se convierte el octeto presente (en valores decimales) a número binario, los cuales se almacenaran el listas.
                #Se almacena en los tres valores que buscamos.
                direccion_octeto_binario = list(calcular_numero_binario(octetos_ip[i]))
                broadcast_red_octeto_binario = list(calcular_numero_binario(octetos_ip[i]))
                red_siguiente_octeto_binario = str(octetos_broadcast_subred[i])

                octeto_final_puerta_enlace = list(calcular_numero_binario(octetos_ip[i]))
                octeto_final_ultima_red_utilizable = list(calcular_numero_binario(octetos_ip[i]))

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
                    valor_subred_siguiente = valor_direccion_red
                    valor_direccion_puerta_enlace = valor_direccion_red
                    valor_direccion_ultima_utilizable = valor_direccion_red
                #Esta sección se ejecutara cuando el prefijo este a punto de acabarse y deba establecerse su límite en el octeto presente
                elif bits_restantes_prefijo < 8 and bits_restantes_prefijo > 0:
                    #Se establece el número de bits activos (1) y no activos (0) del octeto
                    bits_octeto_actual = bits_restantes_prefijo
                    resto_bits_octeto = 8 - bits_octeto_actual

                    #Establecemos los bits de la porción de Subred
                    # De valor 0 para calcular la red completa
                    # De valor 1 para calcular la dirección de broadcast de red y la dirección de subred siguiente
                    for j in range(resto_bits_octeto):
                        direccion_octeto_binario[bits_octeto_actual + j] = "0"
                        broadcast_red_octeto_binario[bits_octeto_actual + j] = "1"
                        octeto_final_puerta_enlace[bits_octeto_actual + j] = "0"
                        octeto_final_ultima_red_utilizable[bits_octeto_actual + j] = "1"

                        if j == (resto_bits_octeto - 1) and i == 3:
                            octeto_final_puerta_enlace[bits_octeto_actual + j] = "1"
                            octeto_final_ultima_red_utilizable[bits_octeto_actual + j] = "0"
                            
                    if i < 3:
                        if octetos_broadcast_subred[i + 1] == 255:
                            red_siguiente_octeto_binario = str(int(red_siguiente_octeto_binario) + 1)

                            if red_siguiente_octeto_binario == "255":
                                red_siguiente_octeto_binario = "0"
                    else:
                        if octetos_broadcast_subred[i] == 255:
                            pass
                        else:
                            red_siguiente_octeto_binario = str(int(red_siguiente_octeto_binario) + 1)

                    #Convertimos los números binarios calculados en valores decimales, para seguido almacenarlos en sus respectivos valores
                    valor_direccion_red += calcular_numero_decimal("".join(direccion_octeto_binario))
                    valor_red_broadcast += calcular_numero_decimal("".join(broadcast_red_octeto_binario))
                    valor_subred_siguiente += red_siguiente_octeto_binario

                    valor_direccion_puerta_enlace += calcular_numero_decimal("".join(octeto_final_puerta_enlace))
                    valor_direccion_ultima_utilizable += calcular_numero_decimal("".join(octeto_final_ultima_red_utilizable))

                    #Se establece en 0 el prefijo en caso de ya haberse establecido todos los bits activos
                    bits_restantes_prefijo = 0
                #Esta sección se ejecutara cuando ya se haya pasado el establecimiento del prefijo
                else:
                    #Los bits no activos (0) ocuparan todo el octeto mediante su respectiva variable
                    bits_octeto_actual = 0
                    resto_bits_octeto = 8

                    #Repetimos nuevamente el establecimiento des bits de la porción de Subred
                    # Aquí se hara para todo el octeto con los bits de sus valores respectivos
                    for j in range(resto_bits_octeto):
                        direccion_octeto_binario[j] = "0"
                        broadcast_red_octeto_binario[j] = "1"
                        octeto_final_puerta_enlace[j] = "0"
                        octeto_final_ultima_red_utilizable[j] = "1"

                        if j == (resto_bits_octeto - 1) and i == 3:
                            octeto_final_puerta_enlace[j] = "1"
                            octeto_final_ultima_red_utilizable[j] = "0"

                    if octetos_broadcast_subred[i] == 255:
                        red_siguiente_octeto_binario = "0"
                    else:
                        red_siguiente_octeto_binario = str(int(red_siguiente_octeto_binario) + 1)

                    valor_direccion_red += calcular_numero_decimal("".join(direccion_octeto_binario))
                    valor_red_broadcast += calcular_numero_decimal("".join(broadcast_red_octeto_binario))
                    valor_direccion_puerta_enlace += calcular_numero_decimal("".join(octeto_final_puerta_enlace))
                    valor_direccion_ultima_utilizable += calcular_numero_decimal("".join(octeto_final_ultima_red_utilizable))
                    valor_subred_siguiente += red_siguiente_octeto_binario

                #Condición para agregar un punto entre los valores de los octetos
                if i < 3: 
                    valor_direccion_red += "."
                    valor_red_broadcast += "."
                    valor_subred_siguiente += "."
                    valor_direccion_puerta_enlace += "."
                    valor_direccion_ultima_utilizable += "."
        valor_subred_siguiente_broadcast = calcular_broadcast_red_siguiente(valor_subred_siguiente, prefijo_valor, admision_valores_octeto)
        
        print("-----------------------------------------------------------------------")
        print("Dirección de Red:", subred_ingresada)
        print("Rango de Hosts Utilizables:", valor_direccion_puerta_enlace, "-", valor_direccion_ultima_utilizable)
        print("Dirección de Broadcast de Red:", valor_red_broadcast)

        
        if broadcast_red == broadcast_completo:
            calcular_valores_subred(valor_subred_siguiente, valor_subred_siguiente_broadcast, broadcast_completo, prefijo_usado, paso_dado=True)
        else:
            calcular_valores_subred(valor_subred_siguiente, valor_subred_siguiente_broadcast, broadcast_completo, prefijo_usado, paso_dado=False)