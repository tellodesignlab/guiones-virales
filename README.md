# Matriz de Contenido Viral

Sistema para [Claude Code](https://claude.com/claude-code) que analiza referentes reales de tu nicho en Instagram y TikTok (vistas, hooks, formatos, duración) y usa esos patrones para escribir y simular guiones publicitarios de tu propio negocio — nunca copiando frases, siempre extrayendo estructura y técnica.

No es una herramienta de crecimiento de cuentas ni corre nada automáticamente: se activa a demanda, con dos flujos de trabajo definidos.

## Qué hace

1. **Recolecta** datos reales de tus referentes vía [Apify](https://apify.com) (scraper de Instagram Reels y de TikTok, con transcripción incluida).
2. **Construye una matriz** de contenido viral: qué patrones de hook, tema, formato, duración y emoción rinden por encima o por debajo del promedio de cada cuenta.
3. **Escribe y simula guiones** para tu negocio a partir de esos patrones, con una estimación de qué tan bien podrían rendir — siempre marcada como estimación, no como predicción.

## Prerrequisitos

- [Claude Code](https://claude.com/claude-code) instalado y funcionando.
- Una cuenta de [Apify](https://apify.com) (da $5 USD de crédito gratis por mes, sin tarjeta — de sobra para correr este análisis varias veces).
- El MCP server de Apify conectado en Claude Code (dentro de una sesión, corré `/mcp` y seguí el flujo de autenticación).
- Python 3.9+ y `pip` (solo si querés generar el PDF de la matriz con `scripts/generar_pdf_matriz.py`).

## Instalación

```bash
git clone <url-de-este-repo>
cd <carpeta-del-repo>

# 1. Configurá tu negocio: copiá la plantilla y completá tus datos
cp CLAUDE.example.md CLAUDE.md
# Editá CLAUDE.md: tu rubro, tus referentes, tu tono, tu CTA.

# 2. (Opcional) Dependencias de Python, solo si vas a generar el PDF de la matriz
pip install -r requirements.txt

# 3. Abrí el proyecto con Claude Code
claude
```

Dentro de la sesión de Claude Code, corré `/mcp` una vez para conectar el servidor de Apify con tu cuenta (te pide autenticarte en el navegador). Después de eso, los dos flujos de trabajo quedan disponibles.

`CLAUDE.md` **no se sube a git** (ver `.gitignore`) porque va a contener información específica de tu negocio — cada quien mantiene su propia copia local a partir de `CLAUDE.example.md`.

## Los 2 flujos de trabajo

Todo el comportamiento está definido en `CLAUDE.md` (una vez que lo creaste desde la plantilla). Se activan diciéndoselo directamente a Claude Code en el chat — no hay comandos ni scripts que correr a mano para esto.

### 1. `analiza referentes`

Corre el ciclo completo:

1. **Recolectar** — corre los scrapers de Apify sobre tus referentes (con topes de costo obligatorios y tu aprobación explícita antes de cada corrida), guarda los datos crudos en `fuentes/` y las transcripciones en `transcripciones/`.
2. **Construir la matriz** — genera `matriz/matriz-contenido-viral.md` (una fila por pieza, con su rendimiento real vs. la mediana de esa cuenta) y `matriz/patrones-de-viralidad.md` (qué funciona, qué no, diferencias por red).
3. **Escribir y simular guiones** — 3-5 guiones nuevos para tu negocio, cada uno con su simulación (qué patrones cumple, señales a favor/en contra, estimación y confianza).

### 2. `hagamos un guión`

Para escribir un guion puntual, fuera del ciclo completo. Antes de escribir una sola palabra, Claude te hace un intake corto (objetivo, audiencia, mensaje central, y dónde se va a distribuir — feed, pauta paga, o ambos), elige la estructura más adecuada de `matriz/estructuras-generales.md`, escribe el guion en tu tono con tu CTA, y lo simula contra la matriz real.

## Estructura de carpetas

```
CLAUDE.example.md → plantilla genérica: copiala como CLAUDE.md y completá tus datos
fuentes/          → datos crudos del scraper de Apify (uno por red y creador) — se genera al correr el análisis
transcripciones/  → texto de cada video analizado — se genera al correr el análisis
matriz/           → matriz-contenido-viral.md, patrones-de-viralidad.md, estructuras-generales.md, referencia-para-agente.md — se generan al correr el análisis
guiones/          → guiones escritos, cada uno con su simulación — se generan al pedir un guion
estructuras/      → (opcional) estructuras de guion externas que quieras sumar al sistema
scripts/          → utilidades de Python (ver abajo)
```

Las carpetas de datos (`fuentes/`, `transcripciones/`, `matriz/`, `guiones/`, `estructuras/`) están vacías en este repo — se llenan con tu propio análisis la primera vez que corrés `analiza referentes`. Lo que generes ahí es específico de tu negocio y no se sube a git (ver `.gitignore`).

## Scripts

### `scripts/generar_pdf_matriz.py`

Convierte `matriz/matriz-contenido-viral.md` en un PDF apaisado, fácil de leer (`matriz/matriz-contenido-viral.pdf`). Requiere haber corrido antes el ciclo de análisis.

```bash
pip install -r requirements.txt
python3 scripts/generar_pdf_matriz.py
```

## Costos de referencia

- Instagram Reels (`apify/instagram-reel-scraper`): desde ~$1.00 USD por 1.000 resultados.
- TikTok (`clockworks/tiktok-scraper`): desde ~$1.70 USD por 1.000 resultados.
- Apify da $5 USD de crédito gratis al mes, sin tarjeta — de sobra para correr este análisis varias veces al mes.
- Cada corrida de scraping muestra el costo estimado y pide tu aprobación explícita antes de ejecutarse.

## Notas

- Nunca se inventan métricas ni transcripciones — lo que no viene del scraper se marca `s/d`.
- `fuentes/` nunca se edita a mano, solo se lee.
- Los guiones nunca copian frases literales de las transcripciones de los referentes — la matriz da estructura y técnica, no palabras.
- Toda simulación de guion es una estimación sobre patrones pasados, no una predicción.
