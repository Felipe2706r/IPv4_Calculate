"""Calculos puros para la pantalla principal de IPv4 Calculate."""

from ipaddress import IPv4Address, IPv4Network


MAXIMO_SUBREDES_MUESTRA = 4096


def calcular_valores_ipv4(direccion_ip: str, prefijo: str) -> dict[str, str]:
    """Valida una direccion IPv4 y devuelve los valores mostrados en pantalla."""
    partes_ip = direccion_ip.strip().split(".")
    if any(not parte for parte in partes_ip):
        raise ValueError("Completa los cuatro octetos de la direccion IP.")
    if len(partes_ip) != 4 or any(
        not parte.isascii() or not parte.isdigit() for parte in partes_ip
    ):
        raise ValueError("Los octetos de la direccion IP solo admiten numeros.")

    prefijo_limpio = prefijo.strip()
    if not prefijo_limpio:
        raise ValueError("Ingresa un prefijo; el campo no puede quedar vacio.")
    if not prefijo_limpio.isascii() or not prefijo_limpio.isdigit():
        raise ValueError("El prefijo solo admite numeros, sin letras ni simbolos.")

    try:
        ip = IPv4Address(direccion_ip.strip())
    except ValueError:
        raise ValueError("Cada octeto debe estar entre 0 y 255.") from None
    valor_prefijo = int(prefijo_limpio)

    primer_octeto = int(str(ip).split(".")[0])
    clase_ip, prefijo_minimo = _obtener_clase_ip(primer_octeto)

    if valor_prefijo < prefijo_minimo:
        raise ValueError(
            f"El prefijo minimo para una IP clase {clase_ip} es /{prefijo_minimo}."
        )
    if valor_prefijo > 32:
        raise ValueError("El prefijo maximo permitido es /32.")

    red = IPv4Network(f"{ip}/{valor_prefijo}", strict=False)
    bits_subred = _obtener_bits_subred(valor_prefijo)
    bits_host = 32 - valor_prefijo

    return {
        "mascara_subred": str(red.netmask),
        "direccion_red": str(red.network_address),
        "broadcast_red": str(red.broadcast_address),
        "numero_subredes": str(2**bits_subred),
        "numero_hosts": str(max(2**bits_host - 2, 0)),
        "clase_ip": clase_ip,
    }


def generar_lista_subredes(direccion_ip: str, prefijo: str) -> list[dict[str, str]]:
    """Genera las subredes usando la convencion de los prototipos."""
    calcular_valores_ipv4(direccion_ip, prefijo)

    ip = IPv4Address(direccion_ip.strip())
    valor_prefijo = int(prefijo.strip())
    prefijo_base = _obtener_prefijo_base_subred(valor_prefijo)
    red_base = IPv4Network(f"{ip}/{prefijo_base}", strict=False)
    cantidad_subredes = 2 ** _obtener_bits_subred(valor_prefijo)

    if cantidad_subredes > MAXIMO_SUBREDES_MUESTRA:
        raise ValueError(
            "La lista supera las 4096 subredes y no puede mostrarse completa."
        )

    if valor_prefijo == prefijo_base:
        subredes = [red_base]
    else:
        subredes = list(red_base.subnets(new_prefix=valor_prefijo))

    lista_subredes: list[dict[str, str]] = []
    for subred in subredes:
        if subred.num_addresses > 2:
            primer_host = subred.network_address + 1
            ultimo_host = subred.broadcast_address - 1
        else:
            primer_host = subred.network_address
            ultimo_host = subred.broadcast_address

        lista_subredes.append(
            {
                "direccion_red": str(subred.network_address),
                "rango_usable": f"{primer_host} - {ultimo_host}",
                "broadcast": str(subred.broadcast_address),
            }
        )

    return lista_subredes


def _obtener_bits_subred(prefijo: int) -> int:
    """Obtiene los bits del octeto parcial segun la logica del prototipo."""
    return prefijo % 8


def _obtener_prefijo_base_subred(prefijo: int) -> int:
    """Obtiene el prefijo completo anterior al octeto parcial."""
    return prefijo - _obtener_bits_subred(prefijo)


def _obtener_clase_ip(primer_octeto: int) -> tuple[str, int]:
    """Devuelve la clase tradicional y su prefijo de red base."""
    if primer_octeto < 128:
        return "A", 8
    if primer_octeto < 192:
        return "B", 16
    if primer_octeto < 224:
        return "C", 24
    raise ValueError("Solo se admiten direcciones IPv4 de clases A, B o C.")
