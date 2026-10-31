# Plan de pruebas de integración

Ejecutar sobre Atlas y la URL publicada. **Estado inicial: pendiente de ejecución real.** Usar datos de prueba, no productos existentes, para probar eliminación.

| Caso | Procedimiento | Resultado esperado | Resultado real |
| --- | --- | --- | --- |
| P01 Conexión | Abrir la aplicación con secretos reales | Aviso de conexión a Atlas y colección disponible | Pendiente |
| P02 Carga inicial | Como administrador cargar muestra dos veces | Primera carga 30; segunda 0; sin duplicados | Pendiente |
| P03 Registro | Crear `PRU-001`, Producto de prueba, Escritura, S/ 2.50, stock 10, mínimo 3 | Éxito; documento en Atlas con precio_centimos 250 | Pendiente |
| P04 Consulta | Buscar `PRU-001` | Un producto con los datos registrados | Pendiente |
| P05 Actualización | Cambiar stock de `PRU-001` a 2 | Datos persistidos; estado Stock bajo; versión incrementada | Pendiente |
| P06 Persistencia | Recargar y abrir otra sesión | Stock 2 y mismo producto en Atlas | Pendiente |
| P07 Duplicado | Intentar registrar otra vez `PRU-001` | Error comprensible; sigue existiendo un solo documento | Pendiente |
| P08 Validación | Registrar sin nombre o con código inválido | Rechazo sin insertar documento | Pendiente |
| P09 Confirmación | Intentar eliminar con código distinto | No elimina el producto | Pendiente |
| P10 Eliminación | Eliminar `PRU-001` escribiendo el código correcto | Desaparece de aplicación y Atlas | Pendiente |
| P11 Acceso | Abrir ventana privada sin iniciar administrador | Permite consultar; no muestra formularios de escritura | Pendiente |
| P12 Exportación | Filtrar categoría Arte y descargar CSV | CSV con los productos filtrados y campos correctos | Pendiente |
| P13 Enlaces | Abrir GitHub y Streamlit sin sesión | Repositorio y aplicación accesibles | Pendiente |
| P14 Concurrencia | Dos sesiones editan el mismo producto; guardar primero en A y después en B | B detecta conflicto y pide actualizar; no sobrescribe A | Pendiente |

Guardar fecha, resultado observado y captura para cada caso ejecutado. Las pruebas automatizadas locales se documentan por separado y no sustituyen P01–P14.
