from abc import ABC, abstractmethod
import subprocess
import os
import sqlite3

class DBConnectionStrategy(ABC):
    @abstractmethod    
    def check_connection(self, host: str, port: int, user: str, password: str, database: str) -> bool:
        """
        Abstract method to check the connection to a database.
        """
        pass