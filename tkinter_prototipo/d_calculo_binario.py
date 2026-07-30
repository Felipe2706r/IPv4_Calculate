def calcular_numero_binario(num_decimal):
    lista_valores_decimales = [128, 64, 32, 16, 8, 4, 2, 1]
    resultado_binario = ""
    suma_total = 0

    for i in range(len(lista_valores_decimales)):
        if lista_valores_decimales[i] > num_decimal or suma_total == num_decimal:
            resultado_binario += "0"
        elif suma_total + lista_valores_decimales[i] > num_decimal:
            resultado_binario += "0"
        else:
            suma_total += lista_valores_decimales[i]
            resultado_binario += "1"

    return resultado_binario

def calcular_numero_decimal(num_binario):
    lista_valores_decimales = [128, 64, 32, 16, 8, 4, 2, 1]
    num_decimal = 0
    i = 0

    #Navegación a travéz del número en estado binario
    for num in num_binario:
        valor_num = int(num)

        #Comprobación del número actual (0 o 1)
        if valor_num == 1:
            #Suma del valor correspondiente de la lista de decimales
            num_decimal += lista_valores_decimales[i]
        i += 1

    return str(num_decimal)