# Guía de conexión y publicación

## 1 Ejecutar la aplicación sin cuentas

En PowerShell, abre la carpeta del proyecto y ejecuta los comandos de instalación del README. Ejecuta `python -m streamlit run app.py` con el Python de `.venv`. Verás un aviso amarillo de **modo demostración** y 30 productos. Prueba el registro, los filtros, la actualización y la eliminación. Esta etapa no cumple todavía el requisito de Atlas.

## 2 Crear MongoDB Atlas

1. Entra en [MongoDB Atlas](https://cloud.mongodb.com/) y crea o inicia tu cuenta.
2. Crea un proyecto llamado `InventarioEscolar`.
3. Crea un clúster. Si la cuenta ofrece la opción gratuita, selecciónala y verifica el costo antes de confirmar. No es necesario elegir un plan de pago para la actividad.
4. En **Database Access** o **Database & Network Access**, crea un **usuario de base de datos**, distinto de tu cuenta Atlas. Nombre sugerido: `inventario_app`.
5. Asigna el rol `readWrite` únicamente a la base `inventario_escolar`. Guarda una contraseña larga en tu gestor de contraseñas. La aplicación crea la colección y su índice utilizando ese rol.
6. En **Network Access**, agrega tu IP pública actual para las pruebas locales.
7. En el clúster selecciona **Connect → Drivers → Python**. Copia la URI privada.
8. Reemplaza el usuario y la contraseña de la plantilla. Si la contraseña contiene caracteres reservados, codifícalos para una URL. Puedes usar localmente `urllib.parse.quote_plus`; no publiques la clave ni su versión codificada.

Los rótulos pueden variar entre versiones de Atlas. Consulta la [guía oficial de conexión](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/) y los [roles de usuarios](https://www.mongodb.com/docs/atlas/security-add-mongodb-users/).

## 3 Guardar secretos locales

En PowerShell:

```powershell
Copy-Item -LiteralPath '.streamlit/secrets.toml.example' -Destination '.streamlit/secrets.toml'
notepad .streamlit/secrets.toml
```

Completa estos valores en el archivo privado:

```toml
MONGODB_URI = "TU_URI_REAL_PRIVADA"
MONGODB_DATABASE = "inventario_escolar"
ADMIN_PASSWORD = "TU_CLAVE_PRIVADA_DE_ADMINISTRADOR"
```

La contraseña de administrador controla la edición en la aplicación; la contraseña incluida en la URI pertenece al usuario de MongoDB. Pueden y deben ser diferentes. No compartas ninguna en el repositorio o en capturas.

Reinicia Streamlit. Debe aparecer **Conectado a MongoDB Atlas**. La tabla estará vacía al principio. Ingresa como administrador y, en el panel lateral, abre **Cargar productos de ejemplo → Cargar los 30 productos**. La carga puede repetirse: agrega solamente códigos que falten y no sobrescribe ediciones.

En Atlas abre **Browse Collections / Data Explorer**. Verifica `inventario_escolar → productos` y los 30 documentos. El archivo CSV no se sube automáticamente a Atlas: la carga se realiza desde el panel de la aplicación para validar y convertir los datos.

## 4 Verificar CRUD real

Ejecuta:

```powershell
.\.venv\Scripts\python.exe -m scripts.test_atlas
```

Completa además el [plan de pruebas manuales](PLAN_DE_PRUEBAS.md). Guarda resultados y capturas. No marques como aprobado un caso que todavía no has ejecutado.

## 5 Publicar el código en GitHub

1. Entra en [GitHub](https://github.com/) y crea un repositorio **público** llamado `inventario-escolar`.
2. Para usar los comandos siguientes, créalo vacío, sin README, licencia ni `.gitignore` automáticos.
3. Desde la carpeta del proyecto ejecuta:

```powershell
git init
git branch -M main
git add .gitignore README.md app.py inventory.py requirements.txt requirements-dev.txt INICIAR_APP.bat .streamlit/config.toml .streamlit/secrets.toml.example data docs tests scripts .github
git diff --cached --name-only
```

4. Revisa esa lista. **No debe incluir `secrets.toml`, `.venv` ni los cuadernos originales.** El archivo `secrets.toml.example` contiene únicamente una plantilla y sí puede publicarse.
5. Completa el commit y el envío, reemplazando `TU_USUARIO`:

```powershell
git commit -m "Aplicación de inventario escolar con Streamlit y MongoDB"
git remote add origin https://github.com/TU_USUARIO/inventario-escolar.git
git push -u origin main
```

Git puede abrir el inicio de sesión de GitHub. Si solicita nombre y correo para el commit, configura tus propios datos; puedes usar el correo privado de GitHub. No inventes identidad ni escribas tokens en el código.

También puedes usar **Add file → Upload files** en GitHub, conservando la estructura de carpetas y revisando la misma lista de exclusiones. Publica solo los archivos de la aplicación.

## 6 Publicar en Streamlit Community Cloud

1. Abre [Streamlit Community Cloud](https://share.streamlit.io/) e inicia sesión con GitHub.
2. Autoriza el acceso al repositorio que acabas de crear.
3. Selecciona **Create app / New app** y el repositorio `inventario-escolar`.
4. Rama: `main`. Archivo principal: `app.py`. Selecciona Python 3.12 en opciones avanzadas si está disponible.
5. En **Advanced settings → Secrets**, pega el contenido real del archivo privado `.streamlit/secrets.toml`. Los secretos se guardan en la configuración del despliegue, no en GitHub.
6. Publica y espera a que se instalen las dependencias. Copia la URL pública que realmente te asigne Streamlit; no uses una URL de ejemplo como enlace final.
7. Atlas también debe permitir la IP de salida del servidor de Streamlit. La IP de tu PC no autoriza el servidor remoto. Verifica en la documentación vigente de tu alojamiento si proporciona IPs de salida para agregarlas.
8. Si el alojamiento no ofrece IP fija y necesitas una demostración académica, Atlas permite `0.0.0.0/0`. Esto admite intentos de conexión desde cualquier IP: úsalo solo con datos sintéticos, TLS, contraseña robusta y usuario limitado a esta base. Revoca esa regla cuando termine la evaluación o migra a alojamiento con salida fija. Nunca expongas credenciales para resolver un error de red.
9. Comprueba la página desde una ventana privada. Debe mostrar **Conectado a MongoDB Atlas**; consulta sin clave y prueba edición con administrador. Recargar debe conservar los cambios.

Consulta la documentación oficial de [organización de archivos](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization) y [secretos de despliegue](https://docs.streamlit.io/deploy/concepts/secrets).

## 7 Completar el informe

1. Abre `docs/INFORME.md` o su versión Word.
2. Completa tus datos académicos y las URLs reales de GitHub y Streamlit.
3. Actualiza la sección de resultados de Atlas con las pruebas ejecutadas.
4. Inserta las capturas indicadas en `docs/capturas/README.md`. Oculta credenciales y datos de cuenta.
5. Exporta el informe final a PDF si el docente lo requiere.
6. Comprueba ambos enlaces desde una ventana privada y entrega el informe.

## Solución de problemas

| Síntoma | Revisión |
| --- | --- |
| Aparece modo demostración en la URL pública | Falta `MONGODB_URI` en Secrets o está vacío |
| No conecta a Atlas | Clúster activo, URI, contraseña codificada, usuario y lista de IPs |
| Conecta pero no permite crear colección o índice | Rol `readWrite` sobre `inventario_escolar` |
| No permite editar | Ingresa la clave `ADMIN_PASSWORD` desde el panel lateral |
| Tabla vacía | Administrador → cargar los 30 productos |
| Cambios concurrentes | Pulsa Actualizar datos y revisa antes de reenviar |
| Streamlit no instala módulos | `requirements.txt` debe estar en la raíz junto a `app.py` |
| Se publicó una contraseña | Rótala en Atlas y en Secrets; borrarla del último commit no la elimina del historial |
