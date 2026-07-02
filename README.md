# Mnemosyne

Herramienta CLI potente y robusta escrita en Python para gestionar copias de seguridad (backups) y restauraciones de múltiples bases de datos con soporte para almacenamiento local y servicios en la nube.

Mnemosyne destaca por aplicar estrategias optimizadas según el motor de base de datos (tanto lógicas como físicas e incrementales) e integrar notificaciones y auditoría completa del historial.

---

## 🚀 Características Principales

- **Múltiples Motores**: Soporte completo para **PostgreSQL**, **MySQL** y **SQLite**.
- **Estrategias de Backup Inteligentes**:
  - **PostgreSQL**: Backups físicos y unificación de cadenas de copias mediante `pg_combinebackup` (PostgreSQL 18+).
  - **MySQL**: Copias de seguridad lógicas avanzadas y replicación incremental usando binlogs.
  - **SQLite**: Generación optimizada de diferencias binarias a nivel de página (formato propio `.patch` de páginas modificadas) y su correspondiente reconstrucción diferencial.
- **Almacenamiento en la Nube**: Carga directa y segura a **AWS S3** y **Azure Blob Storage** con autolimpieza local.
- **Restauración en la Nube Automatizada**: Si se solicita la restauración de un backup remoto que no existe localmente, Mnemosyne lo descarga de forma automática, aplica la restauración y elimina de forma segura el archivo temporal del disco local.
- **Interfaz de Usuario Premium**: Tablas estilizadas en consola y resúmenes interactivos mediante [Rich](https://github.com/Textualize/rich) y [colorama](https://pypi.org/project/colorama/).
- **Historial de Auditoría**: Base de datos SQLite integrada (`data/data.db`) para auditar la duración, tamaño, estado (SUCCESS/FAILED) y errores detallados de cada backup.

---

## 📦 Instalación

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/Jorge-Marco5/Mnemosyne.git
    cd Mnemosyne
    ```

2.  **Configura el entorno virtual e instala las dependencias:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configura las variables de entorno:**

    ```bash
    cp .env.example .env
    ```

    _Edita el archivo `.env` para ingresar la llave maestra de encriptación (`BACKUP_MASTER_KEY`), credenciales de nubes (AWS/Azure) o Webhooks de notificaciones (Slack/Discord)._

4.  **Otorga permisos de ejecución al script:**
    ```bash
    chmod +x mnemosyne.sh
    ```

---

## 🛠️ Guía de Uso y Comandos

### 1. Ayuda General

Muestra la lista de comandos disponibles:

```bash
./mnemosyne.sh --help
```

O de un comando en específico:

```bash
./mnemosyne.sh [comando] --help
```

---

### 2. Guardar Configuración (`save`)

Registra las credenciales de conexión de una base de datos. La contraseña es encriptada localmente de forma segura.

```bash
./mnemosyne.sh save
```

- **Datos obligatorios:** Motor de base de datos (`postgresql`, `mysql`, `sqlite`), alias único, host, puerto, usuario, contraseña y nombre de la base de datos.

---

### 3. Listar Configuraciones (`list`)

Muestra las bases de datos registradas en el sistema.

```bash
# Listar todas
./mnemosyne.sh list

# Consultar por alias específico
./mnemosyne.sh list -a [alias]
```

---

### 4. Verificar Conexión (`check`)

Realiza una prueba de conexión en vivo con la base de datos asociada a un alias:

```bash
./mnemosyne.sh check -a [alias]
```

---

### 5. Actualizar Configuración (`update`)

Modifica los parámetros de conexión de una base de datos registrada:

```bash
./mnemosyne.sh update -a [alias]
```

- _Nota: Presiona ENTER sobre cualquier campo para mantener su valor actual._

---

### 6. Eliminar Configuración (`delete`)

Remueve una configuración de base de datos del sistema:

```bash
./mnemosyne.sh delete -a [alias]
```

---

### 7. Ejecutar Copia de Seguridad (`start`)

Realiza una copia de seguridad y opcionalmente la sube a almacenamiento externo.

```bash
# Guardar backup de forma local
./mnemosyne.sh start -a [alias]

# Crear backup y subir a AWS S3
./mnemosyne.sh start -a [alias] -u aws-s3

# Crear backup y subir a Azure Storage
./mnemosyne.sh start -a [alias] -u azure-storage
```

---

### 8. Restaurar Copia de Seguridad (`restore`)

Restaura una base de datos a partir de su historial de backups.
_Si el backup está en la nube y no existe de forma local, el sistema lo descargará de manera automática y limpiará el archivo al terminar._

```bash
# Restaurar el último backup exitoso
./mnemosyne.sh restore -a [alias]

# Restaurar el último backup exitoso antes de una fecha
./mnemosyne.sh restore -a [alias] -d [AAAA-MM-DD]
```

---

### 9. Historial de Auditoría (`history` y `delete-history`)

```bash
# Consultar el historial de auditoría de todos los backups
./mnemosyne.sh history

# Limpiar todo el registro de auditoría
./mnemosyne.sh delete-history
```

- _Eliminar el historial no borra los backups locales ni en la nube_
- _no podra realizar un backup con este programa si no está registrado_

---

## ☁️ Almacenamiento Soportado

- **AWS S3**: Agrega tus credenciales en `.env` (`AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `AWS_REGION`, `AWS_BUCKET_NAME`, `AWS_FOLDER_NAME`).
- **Azure Blob Storage**: Configura tu cuenta y contenedor en `.env` (`AZURE_STORAGE_ACCOUNT`, `AZURE_STORAGE_KEY`, `AZURE_CONTAINER_NAME`).
