from calculo_binario import calcular_numero_binario, calcular_numero_decimal

octetos_ip = []
valor_ip = ""

#Bucle en donde se ingresaran los valores de los octetos de IP
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

        #Ingreso y validación del prefijo
        prefijo_valor = int(input("Ingresa el prefijo necesario: "))
        while prefijo_valor < 0:
                print("El prefijo no puede ser negativo")
                prefijo_valor = int(input("Ingresa un valor valido para el prefijo: "))

        break
    except ValueError as e:
        #Validación para entradas no númericas
        print(f"Error, no puedes ingresar valores no númericos")

print("-----------------------------------------------------------------------")

#Instacia del valor del prefijo ingresado
bits_restantes_prefijo = prefijo_valor
valor_mascara_subred = ""

#Bucle para calcular la Máscara de Subred
for i in range(4):
    octeto_presente = ""

    #Condición que se ejecutara si el prefijo es mayor a 8
    if bits_restantes_prefijo >= 8:
        #Está variable se usa para determinar el número de bits (1) del octeto presente
        bits_octeto_actual = 8

        #Se le restara 8 al prefijo para determinar que ya se ha establecido un octeto 
        #de la máscara
        bits_restantes_prefijo -= 8

        #Está variable se usa para determinar el número de bits no activos (0) de un octeto
        resto_bits_octeto = 0
    
    #Condición que se ejecutara si el prefijo es menor a 8 luego de habersele restado 
    #bits en la primera condición
    elif bits_restantes_prefijo < 8 and bits_restantes_prefijo > 0:
        #Se establece el número de bits activos (1) y no activos (0) del octeto presente
        bits_octeto_actual = bits_restantes_prefijo
        resto_bits_octeto = 8 - bits_octeto_actual

        #Se establece en 0 el prefijo en caso de ya haberse establecido todos los bits asctivos
        bits_restantes_prefijo = 0

    #Condición que se ejecutara si el prefijo es 0, luego de haberse acabado los bits activos
    else:
        #Los bits no activos (0) ocuparan todo el octeto mediante su respectiva variable
        bits_octeto_actual = 0
        resto_bits_octeto = 8

    #Formación del octeto presente según los bits disponibles
    for j in range(bits_octeto_actual):
        octeto_presente += "1"
    for k in range(resto_bits_octeto):
        octeto_presente += "0"

    #Conversión del octeto a número decimal
    valor_mascara_subred += calcular_numero_decimal(octeto_presente)
    if i < 3: 
        valor_mascara_subred += "."

print(f"Máscara de Subred: {valor_mascara_subred}")
