# tool-waxss

Herramienta en Python para detectar WAF y probar vulnerabilidades de Cross-Site Scripting (XSS) en formularios web.

`tool-waxss` está pensada para entornos de bug bounty, pentesting web y laboratorios de seguridad, donde se necesita:

- identificar si un sitio está protegido por un WAF,
- extraer formularios web (incluyendo los generados dinámicamente),
- probar diferentes payloads de XSS sobre esos formularios,
- registrar los resultados de forma clara y repetible.

---

##  Características

- Detección de WAF mediante `wafw00f`.
- Extracción de formularios HTML:
  - formularios estáticos,
  - formularios generados por JavaScript (mediante `requests-html`),
  - iframes.
- Pruebas de XSS sobre los campos detectados.
- Payloads básicos y avanzados.
- Salida clara en consola con `colorama`.

---

## Requisitos

### Sistema

- Python 3.x
- Linux recomendado
- Dependencias instaladas

### Dependencias de Python

```bash
pip install requests requests-html beautifulsoup4 colorama
```

### Herramienta externa: wafw00f

```bash
apt install wafw00f
```

o

```bash
pip install wafw00f
```

---

##  Instalación

```bash
git clone https://github.com/theoffsecgirl/tool-waxss.git
cd tool-waxss
```

(Opcional)

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests requests-html beautifulsoup4 colorama wafw00f
```

---

## Uso básico

```bash
python3 waxss.py
```

Introduce la URL objetivo cuando se solicite.

---

## Casos de uso

- Comprobar XSS reflejado rápidamente.
- Validar comportamiento del WAF.
- Identificar puntos de entrada para pruebas manuales.
- Apoyo para flujos de bug bounty.

---

## Limitaciones

- No detecta todos los tipos de XSS.
- Puede generar falsos positivos/negativos.
- No gestiona CSRF ni autenticación avanzada.
- No sustituye revisión manual.

---

## Uso ético

Solo en sistemas propios, con permiso o en programas de bug bounty autorizados.

---

## Licencia

Incluida en el archivo `LICENSE`.

---

## Autora

Desarrollado por **TheOffSecGirl**

- GitHub: https://github.com/theoffsecgirl
- Web técnica: https://www.theoffsecgirl.com
- Academia: https://www.northstaracademy.io
