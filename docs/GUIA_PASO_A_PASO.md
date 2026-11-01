# Configuración y despliegue

## Requisitos

- Python 3.11 o superior; se recomienda 3.12.
- Un clúster de MongoDB Atlas para guardar datos de forma persistente.
- Un usuario de base de datos con permiso readWrite limitado a la base del proyecto.

## Conectar con MongoDB Atlas

1. Crea un clúster y un usuario de base de datos en Atlas.
2. Autoriza en Network Access la IP de salida del equipo o servidor donde se ejecutará la aplicación.
3. En Connect → Drivers → Python, copia la cadena de conexión y completa sus credenciales. Codifica los caracteres reservados de la contraseña para una URL.
4. Copia la plantilla local:

```powershell
Copy-Item -LiteralPath '.streamlit/secrets.toml.example' -Destination '.streamlit/secrets.toml'
```

5. Edita el archivo privado con tus valores:

```toml
MONGODB_URI = "mongodb+srv://USUARIO:CLAVE_CODIFICADA@TU_CLUSTER.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DATABASE = "inventario_escolar"
ADMIN_PASSWORD = "TU_CLAVE_PRIVADA_DE_ADMINISTRADOR"
```

También se pueden proporcionar las mismas claves como variables de entorno. El archivo real secrets.toml no se publica en GitHub. La contraseña del usuario de MongoDB y la clave de administrador de la aplicación cumplen funciones diferentes.

## Iniciar y cargar la muestra

Ejecuta los comandos de instalación del README. Cuando aparezca Conectado a MongoDB Atlas, ingresa como administrador y abre Cargar productos de ejemplo → Cargar los 30 productos. Se añaden únicamente los códigos faltantes; los productos existentes se conservan.

Sin MONGODB_URI se activa el modo de demostración. Sus cambios se guardan solo en la sesión. Si la URI está configurada y falla la conexión, la aplicación muestra un error y no sustituye la base remota por datos temporales.

## Publicar en Streamlit Community Cloud

1. Conecta tu cuenta de GitHub en Streamlit Community Cloud.
2. Crea una aplicación desde tu repositorio, rama main y archivo app.py.
3. Selecciona Python 3.12 en las opciones avanzadas.
4. Introduce los valores privados en Secrets y despliega la aplicación.
5. Comprueba que Atlas autorice la conexión desde el servidor remoto; autorizar la IP de tu PC no autoriza automáticamente al servidor.

La consulta puede ser pública mientras las modificaciones requieren la clave de administrador. Para una instalación comercial, incorpora usuarios individuales, controles de acceso y auditoría.

## Prueba opcional con Atlas

Después de configurar los secretos locales o las variables de entorno:

```powershell
.\.venv\Scripts\python.exe -m scripts.test_atlas
```

El script crea una colección temporal prueba_crud_<identificador>, prueba registro, consulta, actualización, eliminación y carga inicial, y elimina únicamente esa colección. No modifica la colección productos.

## Resolver problemas

| Síntoma | Revisión |
| --- | --- |
| Aparece modo demostración | Falta MONGODB_URI o está vacía |
| No conecta a Atlas | URI, contraseña codificada, usuario, clúster activo y acceso de red |
| No permite crear el índice | Permiso readWrite sobre la base configurada |
| Tabla vacía | Cargar los productos desde el panel de administrador |
| No permite modificar datos | Configurar ADMIN_PASSWORD e ingresar desde el panel lateral |
| Detecta un cambio simultáneo | Actualizar datos y revisar el producto antes de reenviar |

Documentación oficial: [conexión a Atlas](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/) y [secretos de Streamlit](https://docs.streamlit.io/deploy/concepts/secrets).
