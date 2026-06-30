import os
import subprocess
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from core.compress import compressHandler

class DBBackupStrategy(ABC):
    @abstractmethod
    def backup(self, alias, host: str, port: int, user: str, password: str, database: str, backup_type: str = "full") -> str:
        """
        Abstract method to perform a database backup.
        """
        pass