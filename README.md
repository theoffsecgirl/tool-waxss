# **tool-waxss**

Herramienta ofensiva en Python para detección básica de WAF y pruebas iniciales de XSS en formularios web.
Diseñada para workflows de bug bounty, pentesting web y análisis rápido de superficie de ataque.

---

## **Características**

* Detección de WAF mediante `wafw00f`
* Enumeración de formularios HTML:

  * páginas estáticas
  * contenido dinámico (opcional) mediante `requests-html`
* Pruebas de XSS:

  * payloads genéricos
  * payloads específicos por tipo de WAF
* CLI clara, minimalista y orientada a automatización
* Modo verbose
* Control de timeout

---

## **Requisitos**

### Sistema

* Python 3.x
* macOS / Linux (recomendado)

### Dependencias Python

```bash
pip install requests-html beautifulsoup4 colorama requests lxml_html_clean
```

### Dependencia externa opcional

```bash
pip install wafw00f
```

o

```bash
apt install wafw00f
```

---

## **Instalación**

```bash
git clone https://github.com/theoffsecgirl/tool-waxss.git
cd tool-waxss
chmod +x waxss.py
```

Se recomienda usar un entorno virtual para aislar dependencias:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

---

## **Uso básico**

```bash
python3 waxss.py -u https://example.com
```

Esto ejecuta:

1. Detección de WAF (si procede)
2. Análisis de formularios
3. Pruebas de XSS con payloads base y payloads específicos

---

## **Opciones**

| Flag            | Descripción                                        |
| --------------- | -------------------------------------------------- |
| `-u, --url`     | URL objetivo (obligatorio)                         |
| `--skip-waf`    | Omite la detección de WAF                          |
| `--no-js`       | No renderiza JavaScript (más estable en macOS ARM) |
| `--timeout`     | Ajusta timeout de peticiones                       |
| `-v, --verbose` | Muestra información detallada                      |

---

## **Ejemplos**

Sin renderizado JS (modo recomendado en macOS ARM):

```bash
python3 waxss.py -u https://example.com --no-js
```

Solo formularios + pruebas XSS, sin WAF:

```bash
python3 waxss.py -u https://example.com --skip-waf
```

Verbose + timeout elevado:

```bash
python3 waxss.py -u https://example.com -v --timeout 40
```

---

## **Casos de uso**

* Detección rápida de XSS reflejado
* Identificación de endpoints y campos vulnerables
* Validación inicial del comportamiento del WAF
* Automatización de fases tempranas de análisis en bug bounty

---

## **Limitaciones**

* El renderizado JS depende de `requests-html` y puede fallar en Python 3.13 / macOS ARM
* No gestiona autenticación, sesiones complejas ni CSRF
* No sustituye análisis manual ni pruebas avanzadas
* Puede generar falsos positivos en entornos con filtrado fuerte

---

## **Recomendación técnica**

Para máxima estabilidad:

* Ejecutar con `--no-js`
* Usar Python 3.11 o 3.12 si necesitas renderizado completo
* Integrar la herramienta en tus pipelines de recon

Si deseas una versión sin dependencias “legacy”, se puede migrar a Playwright.

---

## **Uso ético**

Esta herramienta debe utilizarse únicamente en:

* Sistemas propios
* Entornos autorizados
* Programas de bug bounty que lo permitan

El uso no autorizado es ilegal.

---

## Licencia

MIT License (incluida en el archivo `LICENSE.md`)

---

## Autora

Desarrollado por **TheOffSecGirl**

- GitHub: https://github.com/theoffsecgirl  
- Web: https://www.theoffsecgirl.com  
- Academia: https://www.northstaracademy.io
