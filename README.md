# Inventario Escolar

Aplicación académica para gestionar productos de una tienda de útiles escolares con **Python, Streamlit y MongoDB Atlas**. Implementa registro, consulta, actualización y eliminación (CRUD).

**Estado:** código publicado y aplicación desplegada en Streamlit. La aplicación pública funciona en **modo demostración** mientras se completan las credenciales privadas de MongoDB. En Atlas ya existe `inventario_escolar.productos` con 30 documentos. La integración entre la aplicación y Atlas sigue pendiente de verificación.

**Aplicación:** https://inventario-escolar-jeferson.streamlit.app/

**Repositorio:** https://github.com/jeferson1802a/inventario-escolar

## Problema

Una tienda que utiliza cuadernos o archivos separados tiene dificultades para conocer existencias, mantener precios e identificar productos por reponer. La aplicación centraliza el inventario y muestra alertas de stock bajo y productos agotados.

## Funciones

- Listado, búsqueda por código o nombre y filtros por categoría y estado.
- CRUD con validación, código único y confirmación para eliminar.
- Consulta pública; escritura en Atlas protegida con clave de administrador.
- Indicadores de productos, unidades, reposición y valor a precio de venta.
- Exportación de resultados CSV y descarga de la muestra original.
- Carga inicial de 30 productos sin sobrescribir registros existentes.
- Fechas UTC y control de versión para evitar sobrescribir cambios simultáneos.

## Probar en Windows

Abre PowerShell en esta carpeta. Requiere Python 3.11 o superior; se recomienda 3.12.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Abre la dirección local que muestra Streamlit. Sin `MONGODB_URI` se abre **modo demostración**: cada sesión tiene datos temporales e independientes. Al perder la sesión se pierden los cambios; no se guarda nada en Atlas. Con una URI configurada, un fallo de conexión muestra un error y no activa una base de datos alternativa.

## Conectar y publicar

Sigue [la guía paso a paso](docs/GUIA_PASO_A_PASO.md): Atlas → secretos locales → GitHub → Streamlit Community Cloud → pruebas y capturas.

No pegues contraseñas en el chat, los archivos Python, los cuadernos ni el repositorio. `.streamlit/secrets.toml` está excluido de Git. Los cuadernos originales se conservan localmente y se excluyen de la publicación porque no han sido auditados para detectar credenciales.

## Datos y diseño

`data/productos.csv` contiene **30 productos sintéticos**, creados exclusivamente para esta actividad. Los precios y existencias no proceden de una tienda real. Hay seis categorías y casos de stock disponible, bajo y agotado. No contiene datos personales.

Flujo: navegador → aplicación Streamlit → PyMongo con TLS → MongoDB Atlas → base `inventario_escolar` → colección `productos`.

| Campo en MongoDB | Tipo y finalidad |
| --- | --- |
| `_id` | ObjectId generado por MongoDB |
| `codigo` | Texto único, de 3 a 20 caracteres; no cambia al editar |
| `nombre` | Texto de 2 a 100 caracteres |
| `categoria` | Una de las seis categorías permitidas |
| `precio_centimos` | Entero; 850 equivale a S/ 8.50 y evita errores decimales |
| `stock` | Entero no negativo |
| `stock_minimo` | Entero no negativo; alerta si stock ≤ mínimo |
| `creado_en`, `actualizado_en` | Fechas UTC |
| `version` | Entero incrementado al actualizar; detecta cambios concurrentes |

## Verificación

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas incluyen reglas, dinero, duplicados, filtros, CRUD y concurrencia en memoria y con MongoDB simulado, más interacción con Streamlit mediante AppTest. Una simulación **no prueba Atlas**.

Después de configurar secretos, verifica la conexión real:

```powershell
.\.venv\Scripts\python.exe -m scripts.test_atlas
```

Este comando crea una colección temporal `prueba_crud_<identificador>`, ejecuta CRUD y carga inicial, y elimina únicamente esa colección al terminar. No modifica `productos`. Registra la salida real en el informe.

## Entrega

- Informe editable: `docs/INFORME.md` y, si está disponible, su versión Word.
- Pruebas manuales: `docs/PLAN_DE_PRUEBAS.md`.
- Capturas reales: instrucciones en `docs/capturas/README.md`.
- URL Streamlit: https://inventario-escolar-jeferson.streamlit.app/ (modo demostración hasta configurar secretos).
- URL GitHub: https://github.com/jeferson1802a/inventario-escolar

La clave compartida de administrador es una protección básica apropiada para esta demostración académica; una implementación comercial necesita usuarios individuales, controles de acceso y auditoría.
