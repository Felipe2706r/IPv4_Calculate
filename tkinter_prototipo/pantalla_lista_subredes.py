from tkinter import *
from PIL import Image, ImageTk
import os

class FondoDinamico:
    def __init__(self, root, lista_subredes):
        self.root = root
        # 1. Establecer el tamaño de la ventana
        pantalla_pc_altura = self.root.winfo_screenheight()
        self.root.geometry(f"1080x{pantalla_pc_altura}")
        self.root.resizable(False,False)
        self.root.title("Lista de Subredes Disponibles")
        
        # 2. Cargar la imagen original con Pillow
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        base_foto = os.path.join(BASE_DIR, "f_Boceto_PantallaSubredes.png")
        self.imagen_fondo = Image.open(base_foto)
        
        # 3. Crear el contenedor de la imagen
        self.label_fondo = Label(self.root)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 4. Vincular el evento de cambio de tamaño
        self.root.bind('<Configure>', self.redimensionar_fondo)
        self.root.bind("<Unmap>", self.prevent_minimize)
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        # 5. Crear elementos de uso en la pantalla
        self.elementos_graficos(root, lista_subredes)

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

    def prevent_minimize(self, event=None):
        if self.root.state() == 'iconic':
                    # Instantly force the window back to its normal state
                    self.root.deiconify()

    def cerrar_ventana(self):
        self.root.destroy()

    def elementos_graficos(self, ventana, lista_valores_subredes):
        #Cálculo de Escala
        #La escala se usa para determinar el tamaño de la tabla de los campos
        ancho_imagen, alto_imagen = self.imagen_fondo.size
        ancho_ventana = 1080
        alto_ventana = ventana.winfo_screenheight()
        escala_x = ancho_ventana / ancho_imagen
        escala_y = alto_ventana / alto_imagen

        #Área de la Tabla
        inicio_x = int(42 * escala_x)
        inicio_y = int(267 * escala_y)
        ancho_area = int(996 * escala_x)
        alto_area = int(558 * escala_y)

        #Configuración de Barra de Navegación
        alto_fila = max(1, int(52 * escala_y))
        posicion_x_barra = int(1045 * escala_x)
        ancho_barra = max(16, int(20 * escala_x))

        #Establecimiento del total de filas de campos que habra
        cantidad_filas = len(lista_valores_subredes)

        #Creación de Canvas con Scroll
        #El mismo almacenara los campos de texto y las barra de navegación
        self.canvas_subredes = Canvas(
            ventana,
            bg="#ffffff",
            highlightthickness=0,
            bd=0,
            yscrollincrement=alto_fila
        )
        self.canvas_subredes.place(x=inicio_x, y=inicio_y, width=ancho_area, height=alto_area)

        #Creación de Barra de Navegación
        self.barra_subredes = Scrollbar(
            ventana,
            orient=VERTICAL,
            command=self.canvas_subredes.yview
        )
        self.barra_subredes.place(x=posicion_x_barra, y=inicio_y, width=ancho_barra, height=alto_area)
        self.canvas_subredes.configure(yscrollcommand=self.barra_subredes.set)

        #Frame interno de Canvas
        #Dentro del mismo se crean los campos de texto
        #El proposito es permitir crear múltiples filas y determinar el espacio total desplazable
        self.marco_campos_subredes = Frame(self.canvas_subredes, bg="#ffffff")
        self.canvas_subredes.create_window(
            (0, 0),
            window=self.marco_campos_subredes,
            anchor="nw",
            width=ancho_area
        )

        self.texto_num_redes = Label(ventana,text=cantidad_filas,font=("Helvetica",25),fg="#fcfcfc",bg="#4d4faf")
        self.texto_num_redes.place(x=965, y=45)

        #Listas que almacenaran todos los campos que sean creados
        self.lista_campos_direccion_red = []
        self.lista_campos_rango_uso = []
        self.lista_campos_broadcast = []

        #Posiciones de Eje X para los campos de cada columna
        posiciones_x = {
            "direccion_red": int(20 * escala_x),
            "rango_uso": int(355 * escala_x),
            "broadcast": int(690 * escala_x)
        }

        #Separadores de columnas (Barras negras horizontales)
        alto_total_campos = cantidad_filas * alto_fila
        for separador_x in (int(327 * escala_x), int(662 * escala_x)):
            separador = Label(self.marco_campos_subredes, bg="#000000")
            separador.place(x=separador_x, y=0, width=int(8 * escala_x), height=alto_total_campos)

        #Bucle de creación principal
        for fila in range(cantidad_filas):
            posicion_y = fila * alto_fila

            #Campo de Dirección de Red
            campo_direccion_red = Entry(self.marco_campos_subredes)
            campo_direccion_red.config(font=("Helvetica", 27), width=14)
            campo_direccion_red.place(
                x=posiciones_x["direccion_red"],
                y=posicion_y,
                height=alto_fila
            )
            campo_direccion_red.delete(0, END)
            campo_direccion_red.insert(0, lista_valores_subredes[fila][0])
            self.lista_campos_direccion_red.append(campo_direccion_red)

            #Campo de Rango Utilizable
            campo_rango_uso = Entry(self.marco_campos_subredes)
            campo_rango_uso.config(font=("Helvetica", 27), width=14)
            campo_rango_uso.place(
                x=posiciones_x["rango_uso"],
                y=posicion_y,
                height=alto_fila
            )
            campo_rango_uso.delete(0, END)
            campo_rango_uso.insert(0, lista_valores_subredes[fila][1])
            self.lista_campos_rango_uso.append(campo_rango_uso)

            #Campo de Dirección de Broadcast
            campo_broadcast = Entry(self.marco_campos_subredes)
            campo_broadcast.config(font=("Helvetica", 27), width=14)
            campo_broadcast.place(
                x=posiciones_x["broadcast"],
                y=posicion_y,
                height=alto_fila
            )
            campo_broadcast.delete(0, END)
            campo_broadcast.insert(0, lista_valores_subredes[fila][2])
            self.lista_campos_broadcast.append(campo_broadcast)

        #
        self.campo_direccion_red = self.lista_campos_direccion_red[0]
        self.campo_rango_uso = self.lista_campos_rango_uso[0]
        self.campo_broadcast = self.lista_campos_broadcast[0]

        #Configuración para mover la lista de campos con la rueda del mouse
        self.marco_campos_subredes.config(width=ancho_area, height=alto_total_campos)
        self.canvas_subredes.configure(scrollregion=(0, 0, ancho_area, alto_total_campos))
        self.canvas_subredes.bind("<MouseWheel>", self.mover_scroll_subredes)
        ventana.bind("<MouseWheel>", self.mover_scroll_subredes)

    def mover_scroll_subredes(self, event):
        #Esta función permite hacer uso de la barra de nevegación con la barra del mouse
        self.canvas_subredes.yview_scroll(int(-1 * (event.delta / 120)), "units")

def iniciar_ventana_subredes(ventana_padre, lista_subredes):
    ventana_subredes = Toplevel(ventana_padre)
    ventana_subredes.transient(ventana_padre)
    ventana_subredes.grab_set()
    AppSubredes = FondoDinamico(ventana_subredes, lista_subredes)
    ventana_subredes.wait_window()
