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
print(f"Dirección IP: {valor_ip}")

#Clasificación de Clase de IP
if octetos_ip[0] < 128:
    tipo_clase_ip = "A"
elif octetos_ip[0] >= 128 and octetos_ip[0] < 192:
    tipo_clase_ip = "B"
elif octetos_ip[0] >= 192 and octetos_ip[0] < 224:
    tipo_clase_ip = "C"
else:
    tipo_clase_ip = "Clase no admitida"
print(f"Tipo de Clase: {tipo_clase_ip}")