# Pruebas de integración

Verificación realizada el 31 de octubre de 2026 en Streamlit y MongoDB Atlas. PRU-001 se creó exclusivamente para la prueba y se eliminó con autorización del responsable.

## Casos reales ejecutados

| Caso | Procedimiento | Resultado observado |
| --- | --- | --- |
| P01 Conexión | Abrir Streamlit con los secretos configurados | Conectado a MongoDB Atlas; 30 productos; 630 unidades |
| P03 Registro | Comprobar ausencia de PRU-001; registrarlo en Cuadernos con precio 2.50, stock 10 y mínimo 3 | Mensaje de éxito; 31 productos |
| P04 Consulta | Buscar PRU-001 | Un producto con los datos registrados |
| P05 Actualización | Cambiar stock de PRU-001 de 10 a 2 | Mensaje de éxito; stock 2 y estado Stock bajo |
| P06 Persistencia remota | Consultar PRU-001 desde Data Explorer | precio_centimos 250, stock 2 y version 2 |
| P10 Eliminación | Con autorización, confirmar PRU-001 y eliminar desde Streamlit | Mensaje de éxito; 30 productos; Atlas devuelve cero resultados para ese código |
| P11 Acceso | Observar antes y después del ingreso del responsable | Visitante antes del ingreso; Administrador después |
| P13 Publicación | Abrir repositorio y aplicación y revisar acceso configurado | Repositorio público; Make this app public activo en Streamlit |

## Pruebas automatizadas

La suite local de 13 pruebas y la primera ejecución de GitHub Actions pasaron. Cubren validación, códigos únicos, dinero, filtros, CSV, CRUD, conflictos de versión y acceso de administrador con MongoDB simulado. Véase RESULTADOS_LOCALES.md.

## Ampliaciones opcionales no ejecutadas contra Atlas

- P02 Repetir la carga inicial y comprobar que conserve ediciones.
- P07 Intentar registrar un duplicado.
- P08 Enviar campos inválidos.
- P09 Eliminar con confirmación incorrecta.
- P12 Descargar y comprobar un CSV filtrado.
- P14 Editar simultáneamente desde dos sesiones.

No se presentan estas ampliaciones como pruebas manuales aprobadas. Varias de sus reglas están cubiertas por la suite automatizada. No se ejecutó el script local test_atlas.py con credenciales reales.
