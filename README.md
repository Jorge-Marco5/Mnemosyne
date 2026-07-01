# Mnemosyne

Herramienta CLI para poder realizar operaciones como copias de seguridad y restauracion de multiples bases de datos

Soporta multiples gestores de base de datos, asi como distintas formas de almacenamiento de los archivos como Google Cloud, S3, etc

Avisos por notificacion a traves de diversas aplicaciones y registro de logs para actividades de auditorias.

## Instalacion

Clona el repositorio de Github

```
git clone https://github.com/Jorge-Marco5/Mnemosyne.git
cd Mnemosyne
```

Inicio de entorno e instalacion de dependencias

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configuracion de variables de entorno

```
cp .env.example .env
```

Iniciar el proyecto

```
python main.py
ó
./mnemosyne.sh
```

## Uso

### Ayuda

Muestra los multiples comandos y operaciones disponibles

```
./mnemosyne.sh --help
```

### Ayuda con comandos especificos

Musestra los distintos valores para un comando especifico

```
./mnemosyne.sh [comando] --help
```

### Listado

Muestra las diferentes configuraciones guardadas de las bases de datos o de una en especifico

```
./mnemosyne.sh list -a [alias]
```

### Guardado

Guarda la configuracion de una base de datos para backups

datos: obligatorios

- motor de base de datos
- alias (nombre identificador)
- host
- puerto
- usuario
- contraseña
- nombre de la base de datos

```
./mnemosyne.sh save
```

### Actualizar

Actualiza la informacion de la configuracion de una base de datos

```
./mnemosyne.sh save -a [alias]
```

### Eliminar

Elimina el registro de la configuracion de una base de datos

```
./mnemosyne.sh delete -a [alias]
```

### Copia de seguridad

Inicia el proceso de copia de seguridad para una base de datos.

```
./mnemosyne.sh backup -a [alias]
```

### Restauracion

Inicia el proceso de restauracion de una base de datos.

```
# por alias
./mnemosyne.sh restore -a [alias]

# por fecha
./mnemosyne.sh restore -d [fecha]
```
