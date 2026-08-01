"""Ventana secundaria para mostrar la lista de subredes."""

from pathlib import Path

import customtkinter as ctk
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
FONDO_SUBREDES = BASE_DIR / "recursos_graficos" / "Fondo_PantallaListaSubredes.png"
ICONO_APLICACION = BASE_DIR / "Logo_IPv4Calculate.ico"

COLOR_BORDE = "#073b4c"
COLOR_DIVISIONES = "#118ab2"
COLOR_ENTRADA = "#118ab2"
COLOR_RESULTADO = "#f1f6f8"
COLOR_TEXTO = "#143b49"

ANCHO_TABLA = 1000
ANCHO_COLUMNAS = (350, 550, 350)
ALTURA_FILA = 52


class VentanaListaSubredes(ctk.CTkToplevel):
    """Ventana modal que presenta los datos de cada subred calculada."""

    def __init__(self, ventana_padre, lista_subredes: list[dict[str, str]]) -> None:
        super().__init__(ventana_padre)

        self.ventana_padre = ventana_padre
        self.lista_subredes = lista_subredes
        self.anchos_columnas = self._calcular_anchos_columnas()
        self.title("Lista de Subredes Disponibles")
        self.geometry("1080x864")
        self.iconbitmap(str(ICONO_APLICACION))
        self.resizable(False, False)
        self.attributes("-fullscreen", False)
        self.transient(ventana_padre)

        self.imagen_original = Image.open(FONDO_SUBREDES)
        self.imagen_fondo = ctk.CTkImage(
            light_image=self.imagen_original,
            dark_image=self.imagen_original,
            size=(1080, 864),
        )
        self.fondo = ctk.CTkLabel(
            self,
            text="",
            image=self.imagen_fondo,
            anchor="nw",
        )
        self.fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._crear_contador()
        self._crear_tabla()
        self._crear_divisores_verticales()

        self.bind("<Configure>", self._redimensionar_fondo)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self.after_idle(self._ajustar_area_disponible)
        self.grab_set()
        self.focus_force()

    def _crear_contador(self) -> None:
        self.contador = ctk.CTkLabel(
            self,
            text=str(len(self.lista_subredes)),
            fg_color=COLOR_ENTRADA,
            bg_color=COLOR_ENTRADA,
            text_color="#ffffff",
            corner_radius=0,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
        )
        self.contador.place(relx=0.918, rely=0.045, relwidth=0.037, relheight=0.070)

    def _crear_tabla(self) -> None:
        self.tabla = ctk.CTkScrollableFrame(
            self,
            width=ANCHO_TABLA,
            height=558,
            corner_radius=0,
            border_width=0,
            bg_color=COLOR_BORDE,
            fg_color=COLOR_RESULTADO,
            scrollbar_fg_color=COLOR_RESULTADO,
            scrollbar_button_color=COLOR_ENTRADA,
            scrollbar_button_hover_color=COLOR_BORDE,
        )
        self.tabla.place(relx=0.037, rely=0.312, relwidth=0.959, relheight=0.646)
        # El espacio fijo mantiene la barra dentro de su marco y deja 1000 px
        # estables para las tres columnas de datos.
        self.tabla._scrollbar.configure(width=32)

        if not self.lista_subredes:
            mensaje = ctk.CTkLabel(
                self.tabla,
                text="No hay subredes para mostrar.",
                fg_color=COLOR_RESULTADO,
                text_color=COLOR_TEXTO,
                font=ctk.CTkFont(family="Segoe UI", size=20),
            )
            mensaje.pack(fill="x", padx=2, pady=2)
            return

        for subred in self.lista_subredes:
            self._crear_fila(subred)

    def _crear_divisores_verticales(self) -> None:
        """Refuerza las dos divisiones de columnas y el limite del scrollbar."""
        acumulado = 0
        posiciones = []
        for ancho in self.anchos_columnas:
            acumulado += ancho
            posiciones.append(0.037 + (acumulado / 1080))
        posiciones.append(0.037 + (ANCHO_TABLA / 1080))

        for relx in posiciones:
            divisor = ctk.CTkFrame(
                self,
                fg_color=COLOR_DIVISIONES,
                corner_radius=0,
                width=4,
            )
            divisor.place(
                relx=relx,
                rely=0.312,
                relwidth=0.004,
                relheight=0.646,
            )

    def _crear_fila(self, subred: dict[str, str]) -> None:
        fila = ctk.CTkFrame(
            self.tabla,
            width=ANCHO_TABLA,
            height=ALTURA_FILA,
            fg_color=COLOR_RESULTADO,
            corner_radius=0,
        )
        fila.pack(fill="x", padx=0, pady=0)
        fila.pack_propagate(False)
        fila.grid_propagate(False)
        fila.grid_rowconfigure(0, minsize=ALTURA_FILA, weight=0)

        for columna, ancho in enumerate(self.anchos_columnas):
            fila.grid_columnconfigure(
                columna,
                minsize=ancho,
                weight=0,
            )

        valores = (
            subred["direccion_red"],
            subred["rango_usable"],
            subred["broadcast"],
        )
        for columna, (valor, ancho) in enumerate(zip(valores, self.anchos_columnas)):
            campo = ctk.CTkLabel(
                fila,
                width=ancho,
                height=ALTURA_FILA,
                text=valor,
                fg_color=COLOR_RESULTADO,
                text_color=COLOR_TEXTO,
                border_width=2,
                border_color=COLOR_BORDE,
                corner_radius=0,
                font=ctk.CTkFont(family="Segoe UI", size=17),
                anchor="center",
                justify="center",
                wraplength=ancho - 20,
            )
            campo.grid(row=0, column=columna, sticky="nsew")

    def _calcular_anchos_columnas(self):
        """Normaliza los anchos solicitados sin permitir que una celda crezca."""
        suma_solicitada = sum(ANCHO_COLUMNAS)
        if suma_solicitada <= 0:
            raise ValueError("Los anchos de las columnas deben ser mayores que cero.")

        escala = ANCHO_TABLA / suma_solicitada
        anchos = [max(round(ancho * escala), 1) for ancho in ANCHO_COLUMNAS]
        anchos[-1] += ANCHO_TABLA - sum(anchos)

        tupla_anchos = tuple(anchos)
        return tupla_anchos

    def _ajustar_area_disponible(self) -> None:
        """Limita la ventana al area visible del padre sin tapar la barra de tareas."""
        self.update_idletasks()
        escala_widget = ctk.ScalingTracker.get_widget_scaling(self)
        ancho_padre = max(round(self.ventana_padre.winfo_width() / escala_widget), 1)
        alto_padre = max(round(self.ventana_padre.winfo_height() / escala_widget), 1)
        ancho = min(1080, ancho_padre)
        alto = min(864, alto_padre)
        x_padre = round(self.ventana_padre.winfo_rootx() / escala_widget)
        y_padre = round(self.ventana_padre.winfo_rooty() / escala_widget)
        posicion_x = x_padre + max((ancho_padre - ancho) // 2, 0)
        posicion_y = y_padre + max((alto_padre - alto) // 2, 0)
        self.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")

    def _redimensionar_fondo(self, evento) -> None:
        if evento.widget is not self or evento.width < 2 or evento.height < 2:
            return
        escala_widget = ctk.ScalingTracker.get_widget_scaling(self)
        ancho = max(round(evento.width / escala_widget), 1)
        alto = max(round(evento.height / escala_widget), 1)
        self.imagen_fondo.configure(size=(ancho, alto))

    def _cerrar(self) -> None:
        self.grab_release()
        self.destroy()
