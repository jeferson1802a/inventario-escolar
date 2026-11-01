# Modelo de datos

Base predeterminada: `inventario_escolar`. Colección: `productos`.

| Campo | Tipo y función |
| --- | --- |
| `_id` | ObjectId generado por MongoDB |
| `codigo` | Texto único de 3 a 20 caracteres; permanece fijo al editar |
| `nombre` | Texto de 2 a 100 caracteres |
| `categoria` | Cuadernos, Escritura, Arte, Papelería, Accesorios u Organización |
| `precio_centimos` | Entero; 850 equivale a S/ 8.50 |
| `stock` | Entero no negativo |
| `stock_minimo` | Entero no negativo usado en la alerta de reposición |
| `creado_en` | Fecha de creación en UTC |
| `actualizado_en` | Fecha de la última modificación en UTC |
| `version` | Entero incrementado al actualizar; evita sobrescribir cambios simultáneos |

## Reglas

- El índice `codigo_unico` impide registrar dos productos con el mismo código.
- Los códigos se normalizan a mayúsculas y admiten letras, números y guiones.
- Precio, stock y mínimo deben estar entre cero y un millón. El precio admite dos decimales.
- El precio se guarda en céntimos para evitar errores de representación decimal.
- Stock cero: **Agotado**. Stock positivo menor o igual al mínimo: **Stock bajo**. En otro caso: **Disponible**.
- Las actualizaciones y eliminaciones requieren que coincida la versión del documento consultado.
- La carga inicial agrega los códigos que faltan y conserva los productos existentes.

Los datos de `data/productos.csv` son sintéticos y no corresponden a una tienda real.
