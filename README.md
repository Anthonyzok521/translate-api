# translate-api

Pequeña API de traducción que usa la SDK de Google Generative AI (Gemini).

Este proyecto expone dos endpoints principales:
- `GET /models` — lista los modelos disponibles (si la cuenta/SDK lo permite).
- `POST /` — realiza la traducción solicitada.

## Contenido
- Requisitos
- Variables de entorno
- Instalación y ejecución
- Endpoints
- Ejemplos
- Solución de problemas

## Requisitos
- Python 3.10+ recomendado (probado con 3.11/3.13)
- Virtualenv
- Dependencias en `requirements.txt`:
	- `python-dotenv`
	- `fastapi`
	- `uvicorn`
	- `google-generativeai`

## Variables de entorno
- `GEMINI_API_KEY` (obligatoria): tu API key para Google Generative AI.
- `GEMINI_MODEL_NAME` (opcional): nombre del modelo a usar (por defecto `gemini-2.5`).

Crea un archivo `.env` en la raíz con al menos:

GEMINI_API_KEY=tu_api_key_aqui

Instalación y ejecución (PowerShell)
```powershell
# Crear y activar virtualenv
python -m venv venv
& .\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# (Opcional) exportar variables de entorno en la sesión actual
$Env:GEMINI_API_KEY = 'tu_api_key_aqui'
$Env:GEMINI_MODEL_NAME = 'gemini-2.5'  # opcional

# Ejecutar el servidor
python -m uvicorn api.index:app --reload
```

## Endpoints
- GET /models
	- Descripción: intenta listar modelos disponibles con la SDK y devuelve JSON `{ "models": ["name1", "name2", ...] }`.
	- Nota: si la cuenta o la versión del SDK no permiten `ListModels`, la llamada puede devolver 500 con un mensaje de error detallado.

- POST /
	- Descripción: traduce una frase según los parámetros.
	- Body (JSON):
		- `text`: texto a traducir (string)
		- `from_lang`: idioma origen (string) — actualmente no se usa activamente en el prompt pero se mantiene para compatibilidad
		- `to_lang`: idioma destino (string) — puede ser nombre del idioma (`inglés`, `spanish`) o código (`en`, `es`)
	- Ejemplo de request JSON:
```json
{
	"text": "Manzana",
	"from_lang": "es",
	"to_lang": "en"
}
```
    - Respuesta: texto traducido como `string` en el cuerpo (o JSON con `detail` en caso de error HTTP 500).

## Notas importantes
- Modelos y compatibilidad:
	- El error que motivó cambios en esta repo era `404 models/... is not found for API version v1beta`.
	- No todos los nombres de modelo (`gemini-2.5-flash`, `gemini-2.5-pro`, etc.) están disponibles para todas las cuentas ni para todos los métodos de la API. Usa `GET /models` para ver qué devuelve tu configuración.
	- Si `GET /models` devuelve 500, revisa la salida completa del error en la consola; puede indicar que la cuenta no tiene permisos para `ListModels`.

## Autor
[@Anthonyzok521](https://github.com/Anthonyzok521)