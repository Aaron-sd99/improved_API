            API de Ejemplo

Este proyecto implementa una API que permite consultar tato la información de usuarios como productos.

Funcionalidades

- Permite registrar nuevos usuarios
- Manejo de productos con CRUD
- Respuestas en formato JSON

Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload