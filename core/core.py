from simple_term_menu import TerminalMenu

opciones=['postgresql','mysql','sqlite']

def saveConfig(args):
    """
    Guarda una nueva configuracion de base de datos en el sistema
    """
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
    elif engine == 'sqlite':
        alias = input("Ingrese el alias de la base de datos: ")
        db_name = input("Ingrese el nombre del archivo de la base de datos: ")
    else:
        print("Motor de base de datos no soportado.")
        return 1
    
def listConfigs(args):
    """
    Lista todas las configuraciones de base de datos guardadas en el sistema
    """
    if not args.alias:
        print("Mostrar todas las configuraciones guardadas")
    elif args.alias:
        print("Mostrar la configuracion guardada con el alias: ", args.alias)

def updateConfig(args):
    """
    Actualiza una configuracion de base de datos guardada en el sistema
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a actualizar")
        return 1
    elif args.alias:
        print("Actualizar la configuracion con el alias: ", args.alias)

def deleteConfig(args):
    """
    Elimina una configuracion de base de datos guardada en el sistema
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a eliminar")
        return 1
    elif args.alias:
        print("Eliminando la configuracion con el alias: ", args.alias)

def showHistory(args):
    """
    Muestra el historial de copias de seguridad de base de datos
    """
    if not args.alias:
        print("Mostrar el historial de copias de seguridad de todas las bases de datos guardadas")
    elif args.alias:
        print("Mostrando el historial de la configuracion con el alias: ", args.alias)

def startBackup(args):
    """
    Inicia una copia de seguridad de base de datos
    """
    if not args.alias:
        print("Ingresa el alias de la configuracion a utilizar")
        return 1
    elif args.alias:
        print("Iniciando copia de seguridad de la configuracion con el alias: ", args.alias)

def restoreBackup(args):
    """
    Restaura una copia de seguridad de base de datos en base a su ID o alias
    """
    if not args.id and not args.alias:
        print("Ingresa el ID o el alias de la copia de seguridad a restaurar")
        return 1
    elif args.id:
        print("Restaurando la copia de seguridad con el ID: ", args.id)
    elif args.alias:
        print("Restaurando la copia de seguridad con el alias: ", args.alias)