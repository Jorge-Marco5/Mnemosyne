import sqlite3
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Ruta del archivo de historial
DATA_PATH = os.getenv("DATA_PATH")
HISTORY_FILE = Path(str(DATA_PATH), "data.db")

class DataService:
    def __init__(self):
        """Inicializa la conexión a la base de datos de historial y crea la tabla si no existe."""
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(HISTORY_FILE))
        self._create_table()

    def _create_table(self):
        """Crea la tabla de historial si no existe."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS configs (
                id TEXT PRIMARY KEY,
                engine TEXT NOT NULL,
                alias TEXT NOT NULL,
                host TEXT NOT NULL,
                port TEXT NOT NULL,
                user TEXT NOT NULL,
                password TEXT NOT NULL,
                db_name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS backup_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_config TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                alias TEXT NOT NULL,--Alias de la configuración asociada
                engine TEXT NOT NULL,--Motor de base de datos asociado
                backup_type TEXT NOT NULL,--Tipo de copia de seguridad(full, incremental, etc)
                duration_seconds REAL NOT NULL,--Duración del respaldo en segundos)
                size_bytes INTEGER,--Tamaño del archivo en bytes
                status TEXT NOT NULL,--Estado del respaldo(success, error, etc)
                file_path TEXT,--Ruta del archivo de respaldo
                storage_destination TEXT,--Destino de almacenamiento del respaldo(local, S3, etc)
                error_message TEXT,--Mensaje de error en caso de respaldo fallido
                FOREIGN KEY (id_config) REFERENCES configs (id)
            );"""
        )
        self.conn.commit()

    #Configuraciones

    def create_config(self, data: dict):
        """Inserta una nueva configuración en la tabla de configuraciones."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO configs (
                id, engine, alias, host, port, user, password, db_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['id'],
            data['engine'],
            data['alias'],
            data['host'],
            data['port'],
            data['user'],
            data['password'],
            data['db_name']
        ))
        self.conn.commit()

        item = self.show_one(data['alias'])
        return item

    def show_all(self):
        """Obtiene todas las configuraciones de la tabla de configuraciones."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, engine, alias, host, port, user, db_name FROM configs")
        return cursor.fetchall()

    def show_one(self, alias: str):
        """Obtiene una configuración específica de la tabla de configuraciones."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, engine, alias, host, port, user, db_name FROM configs WHERE alias = ?",
            (alias,)
        )
        return cursor.fetchone()

    def show_info(self, id: str):
        """Obtiene una configuración específica de la tabla de configuraciones para funciones internas."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, engine, alias, host, port, user, password, db_name FROM configs WHERE id = ?",
            (id,)
        )
        return cursor.fetchone()

    def show_info_by_alias(self, alias: str):
        """Obtiene una configuración completa por alias para funciones internas."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, engine, alias, host, port, user, password, db_name FROM configs WHERE alias = ?",
            (alias,)
        )
        return cursor.fetchone()

    def show_last_info_by_date(self, alias: str, date: str):
        """Obtiene la última configuración creada antes de una fecha específica."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, engine, alias, host, port, user, password, db_name FROM configs WHERE alias = ? AND DATE(created_at) < ? ORDER BY created_at DESC LIMIT 1",
            (alias, date,)
        )
        return cursor.fetchone()

    def update(self, data: dict):
        """Actualiza una configuración existente en la tabla de configuraciones."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE configs SET
                engine = ?,
                alias = ?,
                host = ?,
                port = ?,
                user = ?,
                db_name = ?
            WHERE id = ?
        """, (
            data["engine"],
            data["alias"],
            data["host"],
            data["port"],
            data["user"],
            data["db_name"],
            data["id"]
        ))
        self.conn.commit()

        item = self.show_one(data['alias'])
        return item

    def delete(self, alias: str):
        """Elimina una configuración de la tabla de configuraciones."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM configs WHERE alias = ?", (alias,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar la configuracion: {e}")
            return False


    #Historial
    def add_log(self, alias: str, engine: str, backup_type: str, duration_seconds: float, size_bytes: int | None, status: str, file_path: str | None = None, storage_destination: str | None = None, error_message: str | None = None):
        """Inserta un nuevo registro de actividad de respaldo en el historial."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO backup_history (
                timestamp, alias, engine, backup_type, duration_seconds, 
                size_bytes, status, file_path, storage_destination, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            alias,
            engine,
            backup_type,
            duration_seconds,
            size_bytes,
            status.upper(),
            file_path,
            storage_destination,
            error_message
        ))
        self.conn.commit()

    def show_logs(self, alias: str | None = None, status: str | None = None, limit: int = 50) -> list:
        """Obtiene y filtra los registros del historial."""
        cursor = self.conn.cursor()
        
        query = """
            SELECT id, timestamp, alias, engine, backup_type, duration_seconds, 
                   size_bytes, status, file_path, storage_destination, error_message 
            FROM backup_history 
            WHERE 1=1
        """
        params = []

        if alias:
            query += " AND alias = ?"
            params.append(alias)
        if status:
            query += " AND status = ?"
            params.append(status.upper())

        query += " ORDER BY timestamp DESC LIMIT ?"

        params.append(limit)

        cursor.execute(query, params)
        data = cursor.fetchall()
        #tratar los datos para que sean más legibles
        formatted_data = []
        for row in data:
            formatted_row = list(row)
            # Convertir timestamp a formato legible
            formatted_row[1] = datetime.strptime(formatted_row[1], "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
            # Convertir a tiempo legible en segundos
            formatted_row[5] = f"{formatted_row[5]:.2f} s"
            # Convertir size_bytes a KB, MB o GB según corresponda
            if formatted_row[6] is not None:
                size = formatted_row[6]
                if size < 1024:
                    formatted_row[6] = f"{size} B"
                elif size < 1024**2:
                    formatted_row[6] = f"{size / 1024:.2f} KB"
                elif size < 1024**3:
                    formatted_row[6] = f"{size / (1024**2):.2f} MB"
                else:
                    formatted_row[6] = f"{size / (1024**3):.2f} GB"
            else:
                formatted_row[6] = "N/A"
            formatted_data.append(formatted_row)
        return formatted_data

    def get_latest_successful_backup(self, alias: str):
        """
        Obtiene el registro del último backup exitoso para un alias específico.
        """
        cursor = self.conn.cursor()
        query = """
            SELECT * FROM backup_history 
            WHERE alias = ? AND status = 'SUCCESS'
            ORDER BY timestamp DESC 
            LIMIT 1
        """
        cursor.execute(query, (alias,))
        return cursor.fetchone()

    def clear_history(self):
        """Elimina todos los registros del historial."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM backup_history")
        self.conn.commit()

    def __del__(self):
        """Cierra la conexión al recolectar el objeto."""
        try:
            self.conn.close()
        except Exception:
            pass
