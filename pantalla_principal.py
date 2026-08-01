"""Pantalla principal de IPv4 Calculate"""

#Librerías utilizadas para obtener el tamaño del monitor
# y así ajustar el tamaño de la ventana al abrirse.
import ctypes
import sys

#Librerías utilizadas para la configuración de elementos gráficos.
from pathlib import Path
import customtkinter as ctk
from PIL import Image

#Importaciones del resto de archivos que componen la aplicación.
from calculos_ipv4 import calcular_valores_ipv4, generar_lista_subredes
from ventana_lista_subredes import VentanaListaSubredes

BASE_DIR = Path(__file__).resolve().parent
FONDO_PRINCIPAL = BASE_DIR / "recursos_graficos" / "Fondo_PantallaPrincipal.png"
ICONO_APLICACION = BASE_DIR / "Logo_IPv4Calculate.ico"

COLOR_ENTRADA = "#168daf"
COLOR_BORDE = "#073b4c"
COLOR_RESULTADO = "#f1f6f8"
COLOR_TEXTO_RESULTADO = "#143b49"
COLOR_ESTADO = "#ffffff"
COLOR_ESTADO_ERROR = "#ef476f"


class PantallaPrincipal(ctk.CTk):
    """Ventana principal con los controles sobre el fondo del diseño final."""

    def __init__(self) -> None:
        super().__init__()

        self.title("IPv4 Calculate")
        self.geometry("1280x720")
        self.iconbitmap(str(ICONO_APLICACION))
        self.minsize(1100, 620)
        self.resizable(False, False)
        self.attributes("-fullscreen", False)
        self.configure(fg_color="#06d6a0")

        self.imagen_original = Image.open(FONDO_PRINCIPAL)
        self.imagen_fondo = ctk.CTkImage(
            light_image=self.imagen_original,
            dark_image=self.imagen_original,
            size=(1280, 720),
        )

        self.fondo = ctk.CTkLabel(
            self,
            text="",
            image=self.imagen_fondo,
            anchor="nw",
        )
        self.fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._crear_entradas()
        self._crear_acciones()
        self._crear_resultados()
        self._crear_estado()
        self.direccion_ip_actual: str | None = None
        self.prefijo_actual: str | None = None

        self.bind("<Configure>", self._redimensionar_fondo)
        self.after_idle(self._iniciar_ventana_maximizada)

    def _iniciar_ventana_maximizada(self) -> None:
        """Ocupa el area de trabajo y conserva visible la barra de tareas."""
        self.attributes("-fullscreen", False)
        if sys.platform == "win32" and not self._usar_area_trabajo_windows():
            self.state("zoomed")
        elif sys.platform != "win32":
            self.state("zoomed")
        self.after_idle(self._actualizar_fondo)

    def _usar_area_trabajo_windows(self) -> bool:
        """Configura la ventana con el rectangulo del monitor sin la barra de tareas."""
        class Rect(ctypes.Structure):
            _fields_ = [
                ("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long),
            ]

        class MonitorInfo(ctypes.Structure):
            _fields_ = [
                ("cb_size", ctypes.c_ulong),
                ("monitor", Rect),
                ("work", Rect),
                ("flags", ctypes.c_ulong),
            ]

        user32 = ctypes.windll.user32
        monitor = user32.MonitorFromWindow(self.winfo_id(), 2)
        monitor_info = MonitorInfo()
        monitor_info.cb_size = ctypes.sizeof(MonitorInfo)

        if not monitor or not user32.GetMonitorInfoW(monitor, ctypes.byref(monitor_info)):
            return False

        escala_widget = ctk.ScalingTracker.get_widget_scaling(self)
        area_trabajo = monitor_info.work
        ancho = round((area_trabajo.right - area_trabajo.left) / escala_widget)
        alto = round((area_trabajo.bottom - area_trabajo.top) / escala_widget)
        izquierda = round(area_trabajo.left / escala_widget)
        superior = round(area_trabajo.top / escala_widget)

        self.state("normal")
        self.geometry(f"{ancho}x{alto}+{izquierda}+{superior}")
        return True

    def _crear_entradas(self) -> None:
        self.entradas_ip: list[ctk.CTkEntry] = []

        contenedor_ip = ctk.CTkFrame(
            self,
            bg_color=COLOR_BORDE,
            fg_color=COLOR_ENTRADA,
            corner_radius=8,
            border_width=2,
            border_color=COLOR_BORDE,
        )
        contenedor_ip.place(relx=0.163, rely=0.32, relwidth=0.302, relheight=0.075)

        for indice in range(4):
            contenedor_ip.grid_columnconfigure(indice * 2, weight=1)
            contenedor_ip.grid_columnconfigure(indice * 2 + 1, weight=0)

            entrada = ctk.CTkEntry(
                contenedor_ip,
                width=1,
                height=48,
                corner_radius=8,
                border_width=0,
                fg_color=COLOR_ENTRADA,
                text_color="#ffffff",
                placeholder_text=str(indice + 1),
                placeholder_text_color="#a8c8cf",
                font=ctk.CTkFont(family="Segoe UI", size=23),
                justify="center"
            )
            entrada.grid(row=0, column=indice * 2, sticky="ew", padx=(3, 3), pady=(4))
            self.entradas_ip.append(entrada)

            if indice < 3:
                separador = ctk.CTkLabel(
                    contenedor_ip,
                    text=".",
                    text_color="#ffffff",
                    fg_color=COLOR_ENTRADA,
                    font=ctk.CTkFont(family="Segoe UI", size=23, weight="bold"),
                    width=10,
                )
                separador.grid(row=0, column=indice * 2 + 1)

        self.entrada_prefijo = ctk.CTkEntry(
            self,
            bg_color=COLOR_BORDE,
            height=48,
            corner_radius=12,
            border_width=2,
            border_color=COLOR_BORDE,
            fg_color=COLOR_ENTRADA,
            text_color="#ffffff",
            placeholder_text="Ej. 24",
            placeholder_text_color="#a8c8cf",
            font=ctk.CTkFont(family="Segoe UI", size=23),
            justify="center"
        )
        self.entrada_prefijo.place(relx=0.630, rely=0.32, relwidth=0.115)

        for entrada in self.entradas_ip:
            entrada.bind("<KeyRelease>", self._verificar_longitud)

    def _verificar_longitud(self, evento):
        entrada = evento.widget
        if len(entrada.get()) > 3:
            entrada.delete(3, ctk.END)

    def _crear_acciones(self) -> None:
        self.boton_calcular = self._crear_zona_accion(
            relx=0.228,
            rely=0.469,
            relwidth=0.171,
            command=self._calcular,
            texto="Calcular Valores",
            color="#168daf",
            color_hover="#0f718d",
            color_presionado="#0b5268",
        )
        self.boton_limpiar = self._crear_zona_accion(
            relx=0.417,
            rely=0.469,
            relwidth=0.171,
            command=self._limpiar,
            texto="Limpiar Campos",
            color="#f24370",
            color_hover="#d73560",
            color_presionado="#b72c50",
        )
        self.boton_lista_subredes = self._crear_zona_accion(
            relx=0.605,
            rely=0.469,
            relwidth=0.175,
            command=self._mostrar_estado_subredes,
            texto="Lista de Subredes",
            color="#ffd166",
            color_hover="#e4b652",
            color_presionado="#c39238",
        )

    def _crear_zona_accion(
        self,
        relx: float,
        rely: float,
        relwidth: float,
        command,
        texto: str,
        color: str,
        color_hover: str,
        color_presionado: str,
    ):
        boton = ctk.CTkButton(
            self,
            text=texto,
            fg_color=color,
            hover_color=color_hover,
            text_color="#0b4050" if texto == "Lista de Subredes" else "#ffffff",
            hover=True,
            corner_radius=26,
            font=ctk.CTkFont(family="Segoe UI", size=20),
            command=command,
        )
        boton.place(relx=relx, rely=rely, relwidth=relwidth, relheight=0.115)
        boton.bind(
            "<ButtonPress-1>",
            lambda evento: boton.configure(fg_color=color_presionado),
        )
        boton.bind(
            "<ButtonRelease-1>",
            lambda evento: boton.configure(fg_color=color),
        )
        return boton

    def _crear_resultados(self) -> None:
        campos = (
            ("mascara_subred", 0.237, 0.616),
            ("direccion_red", 0.237, 0.722),
            ("broadcast_red", 0.237, 0.828),
            ("numero_subredes", 0.732, 0.616),
            ("numero_hosts", 0.732, 0.722),
            ("clase_ip", 0.732, 0.828),
        )
        self.resultados: dict[str, ctk.CTkLabel] = {}

        for nombre, relx, rely in campos:
            resultado = ctk.CTkLabel(
                self,
                text="",
                fg_color=COLOR_RESULTADO,
                text_color=COLOR_TEXTO_RESULTADO,
                corner_radius=0,
                font=ctk.CTkFont(family="Segoe UI", size=23, weight="bold"),
            )
            resultado.place(relx=relx, rely=rely, relwidth=0.242, relheight=0.104)
            self.resultados[nombre] = resultado

        # Las lineas se dibujan encima de los campos para mantener visible la
        # separacion entre cada fila de resultados.
        for relx in (0.237, 0.732):
            for rely in (0.719, 0.825):
                separador = ctk.CTkFrame(
                    self,
                    fg_color=COLOR_BORDE,
                    corner_radius=0,
                    height=3,
                )
                separador.place(
                    relx=relx,
                    rely=rely,
                    relwidth=0.242,
                    relheight=0.004,
                )

    def _crear_estado(self) -> None:
        self.estado = ctk.CTkLabel(
            self,
            text="",
            fg_color="transparent",
            text_color=COLOR_ESTADO,
            font=ctk.CTkFont(family="Segoe UI", size=14),
        )
        self.estado.place(relx=0.5, rely=0.945, anchor="center")

    def _calcular(self) -> None:
        direccion_ip = ".".join(entrada.get().strip() for entrada in self.entradas_ip)
        try:
            valores = calcular_valores_ipv4(direccion_ip, self.entrada_prefijo.get())
        except ValueError as error:
            self.direccion_ip_actual = None
            self.prefijo_actual = None
            self._actualizar_estado(str(error), error=True)
            self._limpiar_resultados()
            return

        for nombre, resultado in self.resultados.items():
            resultado.configure(text=valores[nombre])
        self.direccion_ip_actual = direccion_ip
        self.prefijo_actual = self.entrada_prefijo.get().strip()
        self._actualizar_estado("Valores calculados correctamente.")

    def _limpiar(self) -> None:
        indice = 1
        for entrada in self.entradas_ip:
            if entrada._placeholder_text == str(indice):
                if entrada.get() != str(indice) and entrada.get() != "":
                    entrada.delete(0, "end")
            indice += 1

        if self.entrada_prefijo.get() != "":
            self.entrada_prefijo.delete(0, "end")
        self.direccion_ip_actual = None
        self.prefijo_actual = None
        self._limpiar_resultados()
        self._actualizar_estado("Campos limpiados.")

    def _limpiar_resultados(self) -> None:
        for resultado in self.resultados.values():
            resultado.configure(text="")

    def _mostrar_estado_subredes(self) -> None:
        if not self.direccion_ip_actual or not self.prefijo_actual:
            self._actualizar_estado(
                "Calcula una direccion IP antes de consultar sus subredes.",
                error=True,
            )
            return

        try:
            lista_subredes = generar_lista_subredes(
                self.direccion_ip_actual,
                self.prefijo_actual,
            )
        except ValueError as error:
            self._actualizar_estado(str(error), error=True)
            return

        if hasattr(self, "ventana_subredes") and self.ventana_subredes.winfo_exists():
            self.ventana_subredes.focus_force()
            return

        self.ventana_subredes = VentanaListaSubredes(self, lista_subredes)
        self._actualizar_estado("Lista de subredes abierta.")

    def _actualizar_estado(self, mensaje: str, error: bool = False) -> None:
        self.estado.configure(
            text=mensaje,
            text_color=COLOR_ESTADO_ERROR if error else COLOR_ESTADO,
        )

    def _redimensionar_fondo(self, evento) -> None:
        if evento.widget is not self or evento.width < 2 or evento.height < 2:
            return
        self._actualizar_fondo(evento.width, evento.height)

    def _actualizar_fondo(self, ancho: int | None = None, alto: int | None = None) -> None:
        """Ajusta el recurso completo al area real de la ventana."""
        ancho = ancho or self.winfo_width()
        alto = alto or self.winfo_height()
        if ancho < 2 or alto < 2:
            return

        # CTkImage vuelve a aplicar la escala DPI al renderizarse. El evento
        # entrega las dimensiones fisicas, por eso se convierten a unidades
        # logicas antes de actualizar el tamano de la imagen. 
        # Se consulta a ScalingTracker para evitar depender del metodo privado
        # _get_widget_scaling() durante la maximización.
        escala_widget = ctk.ScalingTracker.get_widget_scaling(self)
        ancho_logico = max(round(ancho / escala_widget), 1)
        alto_logico = max(round(alto / escala_widget), 1)
        self.imagen_fondo.configure(size=(ancho_logico, alto_logico))


def crear_aplicacion() -> PantallaPrincipal:
    """Configura CustomTkinter y devuelve la unica ventana principal."""
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    return PantallaPrincipal()


if __name__ == "__main__":
    aplicacion = crear_aplicacion()
    aplicacion.mainloop()
