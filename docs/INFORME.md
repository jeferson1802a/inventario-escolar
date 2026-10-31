# Aplicación web de inventario escolar con MongoDB Atlas

Informe de diseño desarrollo y verificación

Estudiante: [Completar nombre y apellidos]
Curso y sección: [Completar]
Docente: [Completar]
Fecha: 31 de octubre de 2026

El proyecto propone centralizar el inventario de una tienda de útiles escolares mediante una aplicación web con operaciones CRUD. El código y los datos de demostración están preparados y se han validado localmente. La conexión real a MongoDB Atlas, la publicación y sus evidencias se completarán con las cuentas del estudiante antes de presentar este informe como entrega final.

## 1 Problemática y objetivo

Una pequeña tienda registra sus productos en cuadernos y archivos separados. Esta práctica dificulta conocer las existencias, mantener precios actualizados e identificar productos que requieren reposición. También favorece registros duplicados y consultas lentas.

El objetivo es desarrollar una aplicación accesible desde un navegador que permita registrar, consultar, actualizar y eliminar productos, centralizando la información en MongoDB Atlas. El alcance comprende un inventario de una sola tienda; no incluye ventas, facturación ni gestión de múltiples almacenes.

## 2 Diseño de la solución

La interfaz se implementa con Streamlit y las reglas de negocio con Python. PyMongo comunica la aplicación con una base alojada en MongoDB Atlas mediante una conexión cifrada. GitHub almacena el código y Streamlit Community Cloud se utilizará para publicar la interfaz.

Arquitectura: navegador → Streamlit → reglas y repositorio PyMongo → MongoDB Atlas.

La base propuesta es `inventario_escolar` y la colección es `productos`. Cada documento contiene código, nombre, categoría, precio en céntimos, stock, stock mínimo, fechas de creación y actualización, y versión. MongoDB genera el identificador `_id`. Un índice único sobre `codigo` impide duplicados. El precio se almacena como entero: 850 representa S/ 8.50.

## 3 Datos utilizados

Se creó el archivo `data/productos.csv` con 30 productos sintéticos de seis categorías: Cuadernos, Escritura, Arte, Papelería, Accesorios y Organización. Incluye existencias normales, bajas y agotadas para comprobar las alertas. Los datos no representan una tienda real ni contienen información personal; su finalidad es académica.

La carga inicial valida cada fila y agrega únicamente los códigos que aún no existen. Al repetirla se conservan los cambios realizados sobre los productos existentes.

<!-- pagebreak -->

## 4 Desarrollo y funcionamiento

La aplicación organiza las operaciones en cuatro pestañas. En Consultar inventario se muestra la tabla y se aplican búsquedas por código o nombre, filtros por categoría y filtros por disponibilidad. También se permite descargar los resultados en CSV.

En Registrar producto se solicitan los datos y se rechazan códigos inválidos, nombres vacíos, precios negativos y cantidades no enteras. En Actualizar producto se modifican nombre, categoría, precio y existencias; el código permanece fijo. La eliminación requiere escribir el código exacto como confirmación.

El resumen muestra productos registrados, unidades disponibles, productos por reponer y valor del inventario a precio de venta. Un producto se considera agotado cuando su stock es cero y con stock bajo cuando sus existencias son positivas y menores o iguales al mínimo. El valor mostrado no representa costo ni utilidad.

## 5 Seguridad y persistencia

Las credenciales se leen de secretos privados o variables de entorno y se excluyen del repositorio. Se utiliza un usuario de MongoDB limitado a la base del proyecto. La consulta es pública y las operaciones de escritura en Atlas requieren una clave de administrador.

Las actualizaciones y eliminaciones comprueban la versión del documento para detectar cambios simultáneos. Los errores de conexión muestran mensajes sin revelar la cadena de conexión. Esta clave compartida es una protección básica para la actividad; un sistema comercial necesitaría usuarios individuales y auditoría.

Sin credenciales, el programa ofrece un modo de demostración con datos temporales por sesión. Este modo está identificado en pantalla y no acredita integración con Atlas. Si existe una URI pero falla la conexión, el programa muestra el error sin sustituir Atlas por almacenamiento temporal.

## 6 Verificación realizada

Se ejecutaron 13 pruebas automatizadas locales con resultado satisfactorio. Se verificaron la muestra de 30 productos, validación y normalización, dinero en céntimos, filtros, estados de stock, exportación CSV, duplicados, CRUD, código inmutable y conflictos de versión. También se comprobó la interacción con Streamlit y el acceso de administrador usando MongoDB simulado.

Las pruebas de repositorio utilizaron memoria y `mongomock`; las de interfaz utilizaron AppTest. Estos resultados demuestran el comportamiento local, pero no verifican todavía conectividad, autenticación ni persistencia real en Atlas.

La prueba real se ejecutará con `python -m scripts.test_atlas`. El script crea una colección temporal, verifica CRUD y carga sin duplicados, y elimina únicamente esa colección. El plan manual complementario está en `docs/PLAN_DE_PRUEBAS.md`.

Resultado de integración real con Atlas: PENDIENTE DE EJECUCIÓN.

<!-- pagebreak -->

## 7 Publicación y enlaces de entrega

Repositorio público de GitHub: [PENDIENTE insertar URL real].

Aplicación pública de Streamlit: [PENDIENTE insertar URL real].

La publicación requiere crear el repositorio, subir los archivos de la aplicación, configurar los secretos en Streamlit Community Cloud y autorizar el acceso de red del servidor en Atlas. Antes de entregar, ambos enlaces deben abrirse desde una ventana privada y la aplicación debe indicar conexión a MongoDB Atlas.

## 8 Evidencias de funcionamiento

Las siguientes evidencias se incorporarán después de la conexión y publicación. Deben ser capturas reales y ocultar credenciales, cadenas de conexión y datos personales de la cuenta.

- Figura 1 Clúster de MongoDB Atlas disponible. [PENDIENTE insertar captura].
- Figura 2 Base inventario_escolar y colección productos con documentos. [PENDIENTE insertar captura].
- Figura 3 Aplicación pública conectada a Atlas con tabla y URL visibles. [PENDIENTE insertar captura].
- Figura 4 Registro y consulta del producto PRU-001. [PENDIENTE insertar captura].
- Figura 5 Actualización del stock y comprobación del documento en Atlas. [PENDIENTE insertar captura].
- Figura 6 Eliminación confirmada y verificación de ausencia. [PENDIENTE insertar captura].

## 9 Conclusiones y estado de entrega

La solución implementada permite gestionar el inventario mediante CRUD y añade filtros, alertas y exportación. La separación entre interfaz, reglas de negocio y repositorio facilita la verificación y el mantenimiento. Los datos sintéticos permiten reproducir los casos de prueba sin depender de una fuente externa.

El código pasó las pruebas locales. Para completar la actividad faltan la integración real con Atlas, las pruebas de persistencia, las URLs públicas y las capturas. Este documento es una base editable y deberá actualizarse con esos resultados antes de su entrega.

## 10 Referencias

- MongoDB. Connect to an Atlas Cluster. https://www.mongodb.com/docs/atlas/connect-to-database-deployment/
- MongoDB. Configure Database Users. https://www.mongodb.com/docs/atlas/security-add-mongodb-users/
- Streamlit. File organization for your Community Cloud app. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization
- Streamlit. Managing secrets when deploying your app. https://docs.streamlit.io/deploy/concepts/secrets
