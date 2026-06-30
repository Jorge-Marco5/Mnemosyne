from core.data_service import DataService
from simple_term_menu import TerminalMenu
from core.encrypt import encriptText
import uuid

opciones=['postgresql','mysql','sqlite']

dataService = DataService()

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
            res = dataService.create_config(data)
            print(res)
            return 0
        elif engine == 'sqlite':
            alias = input("Ingrese el alias de la base de datos: ")
            db_name = input("Ingrese el nombre del archivo de la base de datos: ")
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
        list = dataService.show_all()
        if not list:
            print("No hay configuraciones guardadas")
            return 1
        print(list)
    elif args.alias:
        item = dataService.show_one(args.alias)
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
        item = dataService.show_one(args.alias)
        if not item:
            print("Sin registros para ese alias")
            return 1

        print("Enter para mantener el valor actual\n")
        engine_menu = TerminalMenu(opciones, title="Actualizar el motor de base de datos (" + item[1] + "): ")
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
        new_engine = opciones[int(engine_index)]

        new_alias = input(f"actualizar el alias de la base de datos ({item[2]}): ")
        new_host = input(f"actualizar el host de la base de datos ({item[3]}): ")
        new_port = input(f"actualizar el puerto de la base de datos ({item[4]}): ")
        new_user = input(f"actualizar el usuario de la base de datos ({item[5]}): ")
        new_db_name = input(f"actualizar el nombre de la base de datos ({item[6]}): ")

        data = {
            'id': item[0],
            'engine': new_engine if new_engine else item[1],
            'alias': new_alias if new_alias else item[2],
            'host': new_host if new_host else item[3],
            'port': new_port if new_port else item[4],
            'user': new_user if new_user else item[5],
            'db_name': new_db_name if new_db_name else item[6]
        }

        res = dataService.update(data)
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
        item = dataService.show_one(args.alias)
        if not item:
            print("No se encontro la configuracion con el alias: ", args.alias)
            return 1
        dataService.delete(str(item[2]))
        print("Configuracion de (", item[2], ") eliminada con exito")
        return 0


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
    return dataService.show_logs(args.alias, args.status)


def startBackup(args):
    """
    Inicia una copia de seguridad de base de datos
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a utilizar")
        return 1
    elif args.alias:
        print("Iniciando copia de seguridad de la configuracion con el alias: ", args.alias)
        dataService.add_log(args.alias, "postgresql", "full", 10, 5000, "success", "/backups", "local", None)

def restoreBackup(args):
    """
    Restaura una copia de seguridad de base de datos en base a su ID o alias
    """
    if not args.id and not args.alias:
        print("Ingresa el ID o el alias de la copia de seguridad a restaurar")
        return 1
    elif args.id:
        print("Restaurando la copia de seguridad con el ID: ", args.id)
        return 0
    elif args.alias:
        print("Restaurando la copia de seguridad con el alias: ", args.alias)
        return 0
