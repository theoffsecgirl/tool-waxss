# tool-waxss

Herramienta ofensiva en Python para **detección de WAF** y **pruebas de XSS** sobre formularios web.  
Pensada para bug bounty, pentesting web y laboratorios de seguridad ofensiva.

---

## Características

- Detección de WAF usando `wafw00f`
- Extracción de formularios:
  - HTML estático
  - JS renderizado (`requests-html`)
  - formatos mixtos (inputs, textarea, select)
- Pruebas de XSS:
  - payloads básicos
  - payloads específicos según WAF
- CLI profesional
- Modo verbose
- Control de timeout
- Banner minimalista estilo herramienta ofensiva

---

## Requisitos

### Sistema

- Python 3.x  
- Linux recomendado

### Dependencias Python

```bash
pip install requests requests-html beautifulsoup4 colorama
```

### Dependencia externa

```bash
apt install wafw00f
```

o

```bash
pip install wafw00f
```

---

## Instalación

```bash
git clone https://github.com/theoffsecgirl/tool-waxss.git
cd tool-waxss
chmod +x waxss.py
```

(Repositorios privados/entornos virtuales recomendados para pruebas.)

---

## Uso con CLI 

### Ejecución básica

```bash
python3 waxss.py -u https://example.com
```

### Opciones

| Flag | Descripción |
|------|-------------|
| `--skip-waf` | No ejecutar detección de WAF |
| `--no-js` | No renderizar JavaScript (rápido, menos profundo) |
| `--timeout 30` | Cambiar timeout de peticiones |
| `-v` | Modo verbose |

### Ejemplos

```bash
python3 waxss.py -u https://example.com --skip-waf
python3 waxss.py -u https://example.com --no-js -v
python3 waxss.py -u https://example.com --timeout 40
```

---

## Casos de uso

- Detectar XSS reflejado rápidamente
- Identificar puntos de entrada para pentesting web
- Validar comportamiento del WAF ante payloads
- Automatizar una primera fase de análisis antes de manual

---

## Limitaciones

- No gestiona autenticación, CSRF ni cookies complejas
- Renderizado JS limitado por `requests-html`
- Puede dar falsos positivos/negativos
- No sustituye validación manual

---

## Uso ético

Úsala solo con:

- permiso explícito  
- tus propios sistemas  
- programas de bug bounty autorizados  

El uso indebido es ilegal.

---

## Licencia

MIT License (incluida en el archivo `LICENSE.md`)

---

## Autora

Desarrollado por **TheOffSecGirl**

- GitHub: https://github.com/theoffsecgirl  
- Web: https://www.theoffsecgirl.com  
- Academia: https://www.northstaracademy.io
