from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from a_clasificacion_inicial_ip import procesamiento_direccion_ip
from pantalla_lista_subredes import iniciar_ventana_subredes
import os

ventana_principal = Tk()

class VentanaGrafica:
    def __init__(self, root):
        self.root = root
        # 1. Maximizar la ventana desde el inicio
        self.root.state('zoomed')
        self.root.resizable(False,False)
        self.root.title("IPv4 Calculate")
        
        # 2. Cargar la imagen original con Pillow
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        base_foto = os.path.join(BASE_DIR, "f_boceto_fondo.png")
        self.imagen_fondo = Image.open(base_foto)
        
        # 3. Crear el contenedor de la imagen
        self.label_fondo = Label(self.root)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 4. Vincular el evento de cambio de tamaño
        self.root.bind('<Configure>', self.redimensionar_fondo)

        # 5. Crear elementos de uso en la pantalla
        self.elementos_graficos()

    def redimensionar_fondo(self, event):
            # Evitar redimensionar si el evento proviene de un widget interno
            if event.widget == self.root:
                ancho = event.width
                alto = event.height
                
                # Redimensionar la imagen original al nuevo tamaño de la ventana
                imagen_redimensionada = self.imagen_fondo.resize((ancho, alto), Image.Resampling.LANCZOS)
                self.foto_tk = ImageTk.PhotoImage(imagen_redimensionada)
                
                # Actualizar el Label con la nueva imagen
                self.label_fondo.config(image=self.foto_tk)

    def elementos_graficos(self):
        # 1. Crear títulos de campos de ingreso (IP y Prefijo)
        self.texto_direccion = Label(ventana_principal,text="Dirección IP",font=("Helvetica",25),fg="#fcfcfc",bg="#313038")
        self.texto_direccion.place(x=415, y=200)
        self.texto_prefijo = Label(ventana_principal,text="Prefijo",font=("Helvetica",25),fg="#fcfcfc",bg="#313038")
        self.texto_prefijo.place(x=995, y=200)

        # 2. Crear campos de entrada para los octetos de IP
        self.entrada_n1 = Entry()
        self.entrada_n2 = Entry()
        self.entrada_n3 = Entry()
        self.entrada_n4 = Entry()
        self.lista_campos_ip = [self.entrada_n1, self.entrada_n2, self.entrada_n3, self.entrada_n4]

        pixeles_posicion = 320
        for campo in self.lista_campos_ip:
            campo.config(font=("Helvetica",27),width=3)
            campo.place(x=pixeles_posicion, y=255)
            pixeles_posicion += 100

        # 3. Crear campo de entrada para el prefijo
        self.entrada_prefijo = Entry()
        self.entrada_prefijo.config(font=("Helvetica",27))
        self.entrada_prefijo.place(x=833, y=255)

        # 4. Crear botón para realizar los calculos 
        self.boton_calcular = Button(ventana_principal,command=lambda: obtener_mostrar_resultados(self.lista_campos_ip, self.entrada_prefijo, self.lista_campos_muestra),text="Calcular",)
        self.boton_calcular.config(font=("Arial",20),fg="#fcfcfc",bg="#49ab53")
        self.boton_calcular.config(activebackground="#3c805a")
        self.boton_calcular.place(x=560, y=400)

        # 5. Crear botón para limpiar los campos de texto
        self.boton_limpiar = Button(ventana_principal,command=lambda: limpiar_campos(self.lista_campos_ip, self.entrada_prefijo, self.lista_campos_muestra),text="Limpiar",)
        self.boton_limpiar.config(font=("Arial",20),fg="#fcfcfc",bg="#bd5050")
        self.boton_limpiar.config(activebackground="#98467e")
        self.boton_limpiar.place(x=705, y=400)

        # 6. Crear botón para limpiar los campos de texto
        self.boton_lista_subredes = Button(ventana_principal,command=lambda: abrir_ventana_subredes(self.boton_lista_subredes),text="Lista de Subredes",)
        self.boton_lista_subredes.config(font=("Arial",20),fg="#fcfcfc",bg="#cac866")
        self.boton_lista_subredes.config(activebackground="#bb8c4f")
        self.boton_lista_subredes.place(x=840, y=400)

        # 6. Títulos de los datos a mostrarse
        self.texto_direccion = Label(ventana_principal,text="Máscara de Subred",font=("Helvetica",25),fg="#fcfcfc",bg="#4d4faf")
        self.texto_direccion.place(x=165, y=577)
        self.texto_prefijo = Label(ventana_principal,text="Dirección de Red",font=("Helvetica",25),fg="#fcfcfc",bg="#4d4faf")
        self.texto_prefijo.place(x=177.5, y=740)
        self.texto_direccion = Label(ventana_principal,text="Broadcast de Red",font=("Helvetica",25),fg="#fcfcfc",bg="#4d4faf")
        self.texto_direccion.place(x=810, y=577)
        self.texto_prefijo = Label(ventana_principal,text="Número de Host",font=("Helvetica",25),fg="#fcfcfc",bg="#4d4faf")
        self.texto_prefijo.place(x=810, y=740)

        # 7. Bloques de Campos de datos que se mostrarán
        self.campo_mascara_subred = Entry()
        self.campo_direccion_Red = Entry()
        self.campo_broadcast = Entry()
        self.campo_num_host = Entry()
        self.lista_campos_muestra = [self.campo_mascara_subred, self.campo_direccion_Red, self.campo_broadcast, self.campo_num_host]

        self.campo_mascara_subred.config(font=("Helvetica",27),width=14)
        self.campo_mascara_subred.place(x=480, y=577)

        self.campo_direccion_Red.config(font=("Helvetica",27),width=14)
        self.campo_direccion_Red.place(x=480, y=740)

        self.campo_broadcast.config(font=("Helvetica",27),width=14)
        self.campo_broadcast.place(x=1135, y=577)

        self.campo_num_host.config(font=("Helvetica",27),width=14)
        self.campo_num_host.place(x=1135, y=740)

lista_valores_direccion_ip = None
lista_valores_subredes = None

def obtener_mostrar_resultados(lista_campos_octetos_ip, campo_prefijo, lista_campos_mostrar):
    indice = 0
    global lista_valores_direccion_ip
    global lista_valores_subredes
    lista_valores_direccion_ip, lista_valores_subredes = procesamiento_direccion_ip(lista_campos_octetos_ip, campo_prefijo)

    # validar retorno de la función externa
    if not lista_valores_direccion_ip or not isinstance(lista_valores_direccion_ip, (list, tuple)):
        return

    for campo in lista_campos_mostrar:
        if indice >= len(lista_valores_direccion_ip):
            break

        campo.delete(0, END)
        campo.insert(0, lista_valores_direccion_ip[indice])
        indice += 1

def limpiar_campos(lista_campos_ip, campo_prefijo, lista_campos_mostrar):
    global lista_valores_direccion_ip
    global lista_valores_subredes
    respuesta_mensaje = messagebox.askquestion("Limpieza de Campos", "¿Desea dejar vacío todos los campos presentes (Esta acción no se puede deshacer)?")

    if respuesta_mensaje == "yes":
        for campo in lista_campos_ip:
            campo.delete(0, END)
        campo_prefijo.delete(0, END)

        for campo in lista_campos_mostrar:
            campo.delete(0, END)
    lista_valores_direccion_ip = None
    lista_valores_subredes = None

def abrir_ventana_subredes(boton_subredes):
    global lista_valores_subredes
    if lista_valores_subredes is None:
        messagebox.showwarning(title="Error - Lista de Subredes no realizada",message="Debe calcular los valores de una dirección IP primero.")
    else:
        if boton_subredes is None or not boton_subredes.winfo_exists():
            iniciar_ventana_subredes(ventana_principal, lista_valores_subredes)
            return

        boton_subredes.config(state="disabled")
        try:
            iniciar_ventana_subredes(boton_subredes.winfo_toplevel(), lista_valores_subredes)
        finally:
            if boton_subredes.winfo_exists():
                boton_subredes.config(state="normal")

if __name__ == "__main__":
    AppPrincipal = VentanaGrafica(ventana_principal)
    ventana_principal.mainloop()
