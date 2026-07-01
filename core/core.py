from core.data_service import DataService
from simple_term_menu import TerminalMenu
from core.connection.databaseChecker import DatabaseConnectionChecker
from core.backups.databaseChecker import DatabaseBackupChecker
from core.restore.databaseRestoreHandler import DatabaseRestoreHandler
from core.encrypt import encriptText, decriptText
import uuid

opciones=['postgresql','mysql','sqlite']

data_service = DataService()
database_checker = DatabaseConnectionChecker()
database_backup_checker = DatabaseBackupChecker()
database_restore_handler = DatabaseRestoreHandler()

def saveConfig(args):
    """
    Guarda una nueva configuracion de base de datos en el sistema
    """
    try:
        engine_menu = TerminalMenu(opciones, title="Selecciona el motor de base de datos: ")
        engine_index = engine_menu.show()
        # TerminalMenu.show() may return None, an int, or a tuple (for multi-select).
        if engine_index is None:
            print("Operación cancelada.")
            return 1
        if isinstance(engine_index, tuple):
            if len(engine_index) == 0:
                print("Operación cancelada.")
                return 1
            engine_index = engine_index[0]
        engine = opciones[int(engine_index)]

        print("Gestor seleccionado:", engine)

        if engine in ['postgresql', 'mysql']:
            alias = input("Ingrese el alias de la base de datos: ")
            host = input("Ingrese el host de la base de datos: ")
            port = input("Ingrese el puerto de la base de datos: ")
            user = input("Ingrese el usuario de la base de datos: ")
            password = input("Ingrese la contraseña de la base de datos: ")
            db_name = input("Ingrese el nombre de la base de datos: ")
            data = {
                'id': str(uuid.uuid4()),
                'engine': engine,
                'alias': alias,
                'host': host,
                'port': port,
                'user': user,
                'password': encriptText(password),
                'db_name': db_name
            }
            res = data_service.create_config(data)
            print(res)
            return 0
        elif engine == 'sqlite':
            alias = input("Ingrese el alias de la base de datos: ")
            db_name = input("Ingrese el nombre del archivo de la base de datos: ")
            data = {
                'id': str(uuid.uuid4()),
                'engine': engine,
                'alias': alias,
                'host': '',
                'port': '',
                'user': '',
                'password': encriptText(''), # Encriptar un string vacío por consistencia
                'db_name': db_name
            }
            res = data_service.create_config(data)
            print(res)
            return 0
        else:
            print("Motor de base de datos no soportado.")
            return 1
    except Exception as e:
        print(f"Error al guardar la configuracion: {e}")
        return 1
    
def listConfigs(args):
    """
    Lista todas las configuraciones de base de datos guardadas en el sistema
    """
    if not args.alias:
        list = data_service.show_all()
        if not list:
            print("No hay configuraciones guardadas")
            return 1
        print(list)
    elif args.alias:
        item = data_service.show_one(args.alias)
        if not item:
            print("Sin registros")
            return 1
        print(item)

def updateConfig(args):
    """
    Actualiza una configuracion de base de datos guardada en el sistema
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a actualizar")
        return 1
    elif args.alias:
        item = data_service.show_one(args.alias)
        if not item:
            print("Sin registros para ese alias")
            return 1

        print("Enter para mantener el valor actual\n")
        opciones_update = ['default', 'postgresql', 'mysql', 'sqlite']
        engine_menu = TerminalMenu(opciones_update, title="Actualizar el motor de base de datos (" + item[1] + "): ")
        engine_index = engine_menu.show()
        # TerminalMenu.show() may return None, an int, or a tuple (for multi-select).
        if engine_index is None:
            print("Operación cancelada.")
            return 1
        if isinstance(engine_index, tuple):
            if len(engine_index) == 0:
                print("Operación cancelada.")
                return 1
            engine_index = engine_index[0]
        new_engine = opciones_update[int(engine_index)]

        new_alias = input(f"actualizar el alias de la base de datos ({item[2]}): ")
        new_host = input(f"actualizar el host de la base de datos ({item[3]}): ")
        new_port = input(f"actualizar el puerto de la base de datos ({item[4]}): ")
        new_user = input(f"actualizar el usuario de la base de datos ({item[5]}): ")
        new_db_name = input(f"actualizar el nombre de la base de datos ({item[6]}): ")

        data = {
            'id': item[0],
            'engine': new_engine if new_engine != 'default' else item[1],
            'alias': new_alias if new_alias else item[2],
            'host': new_host if new_host else item[3],
            'port': new_port if new_port else item[4],
            'user': new_user if new_user else item[5],
            'db_name': new_db_name if new_db_name else item[6]
        }

        res = data_service.update(data)
        print(res)
        return 0

def deleteConfig(args):
    """
    Elimina una configuracion de base de datos guardada en el sistema
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a eliminar")
        return 1
    elif args.alias:
        print("Eliminando la configuracion con el alias: ", args.alias)
        item = data_service.show_one(args.alias)
        if not item:
            print("No se encontro la configuracion con el alias: ", args.alias)
            return 1
        data_service.delete(str(item[2]))
        print("Configuracion de (", item[2], ") eliminada con exito")
        return 0

def checkConnection(args):
    """
    Verifica la conexion de una base de datos
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a verificar")
        return 1
    elif args.alias:
        item = data_service.show_info_by_alias(args.alias) # Necesitaremos un nuevo método en DataService
        if not item:
            print("Sin registros para ese alias")
            return 1
        print(f"Verificando la conexion con {item[1]} ({args.alias})...")
    passw = decriptText(item[6])
    status = database_checker.verify(item[1], item[3], item[4], item[5], passw, item[7])
    if status:
        print("Conexion exitosa")
        return 0
    else:
        print("Conexion fallida")
    return 1

def showHistory(args):
    """
    Muestra el historial de copias de seguridad de base de datos
    """
    if args.alias and args.status:
        print(f"Mostrando el historial de la configuración '{args.alias}' con estado '{args.status}'")
    elif args.alias:
        print(f"Mostrando el historial de la configuración '{args.alias}'")
    elif args.status:
        print(f"Mostrando el historial con estado '{args.status}'")
    else:
        print("Mostrando el historial completo")
    return data_service.show_logs(args.alias, args.status)


def startBackup(args):
    """
    Inicia una copia de seguridad de base de datos
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a utilizar")
        return 1
    elif args.alias:
        check = checkConnection(args)
        if check != 0:
            print("Conexion fallida")
            return 1
        print("\nIniciando copia de seguridad de la configuracion con el alias: ", args.alias)
        data = data_service.show_info_by_alias(args.alias) # Reutilizamos el nuevo método
        passw = decriptText(data[6])
        check = database_backup_checker.verify(args.alias, data[1], data[3], data[4], data[5], passw, data[7])
        print(f"\nCopia de seguridad de {args.alias} creada con exito.\nArchivo guardado en: ",check)
        return 0

def restoreBackup(args):
    """
    Restaura una copia de seguridad de base de datos en base a su ID o alias
    """
    if not args.alias:
        print("Se requiere el alias de la configuración para la restauración.")
        return 1

    # 1. Buscar el backup más reciente y exitoso para el alias dado
    print(f"Buscando el último backup exitoso para el alias '{args.alias}'...")
    # Usamos un nuevo método en DataService para esto
    backup_log = data_service.get_latest_successful_backup(args.alias)
    print(backup_log)
    if not backup_log:
        print(f"No se encontraron backups exitosos para el alias '{args.alias}'.")
        return 1

    print(f"Backup encontrado: ID {backup_log[0]} del {backup_log[2]}")
    print(f"Archivo: {backup_log[9]}")

    # 2. Obtener los detalles de la conexión para ese alias
    config_data = data_service.show_info_by_alias(args.alias)
    if not config_data:
        print(f"Error: No se encontró la configuración para el alias '{args.alias}'.")
        return 1

    # 3. Pedir confirmación al usuario (¡MUY IMPORTANTE!)
    print("\nADVERTENCIA: Esta operación sobreescribirá la base de datos actual.")
    confirm = input(f"¿Estás seguro de que quieres restaurar la base de datos '{config_data[7]}' usando el backup del {backup_log[2]}? (s/N): ")
    if confirm.lower() != 's':
        print("Restauración cancelada.")
        return 1

    # 4. Ejecutar la restauración
    try:
        password = decriptText(config_data[6])
        success = database_restore_handler.restore(
            engine=config_data[1],
            host=config_data[3],
            port=config_data[4],
            user=config_data[5],
            password=password,
            database=config_data[7],
            backup_file=backup_log[9]
        )
        if success:
            print("\n¡Restauración completada con éxito!")
            return 0
    except Exception as e:
        print(f"\nError durante la restauración: {e}")
        return 1
