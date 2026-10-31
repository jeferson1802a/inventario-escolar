# Resultados de verificación local

Fecha de referencia del proyecto: 31 de octubre de 2026.

Comando ejecutado:

```text
python -m unittest discover -s tests -v
```

Resultado de la ejecución final después de los ajustes de interfaz:

```text
Ran 13 tests in 2.767s
OK
```

## Cobertura

- Cinco pruebas de validación, datos sintéticos, dinero, filtros y exportación CSV.
- Tres pruebas del repositorio de demostración: CRUD y duplicados, código inmutable, carga sin sobrescribir.
- Dos pruebas del repositorio MongoDB con `mongomock`: CRUD y conflictos de versión, código inmutable.
- Tres pruebas de interfaz con AppTest: consulta y búsqueda, registro actualización eliminación, acceso y cierre de sesión de administrador con MongoDB simulado.

Entorno probado: Python 3.12, Streamlit 1.66.1, PyMongo 4.19.0, dnspython 2.9.1 y mongomock 4.3.0.

Streamlit emite avisos de contexto al ejecutarse mediante AppTest y de una futura deprecación interna de pandas en el gráfico; no causaron fallos. El entorno restringido de Windows también emite un aviso de permisos al limpiar una carpeta temporal después de terminar las pruebas; la suite devolvió código 0.

## Estado al finalizar la primera etapa local

En la primera etapa, `python -m scripts.test_atlas` se detuvo con el mensaje de configuración pendiente, porque no se proporcionaron credenciales locales. Ese script no se ejecutó después con credenciales reales.

Posteriormente se publicaron GitHub y Streamlit, y se verificó el CRUD real desde la aplicación y Data Explorer de Atlas. Los resultados de esa etapa están en PLAN_DE_PRUEBAS.md e INFORME.md. Esta sección conserva la distinción entre pruebas locales simuladas y pruebas reales en la nube.
