from ast import Raise

from core.data_service import DataService
from simple_term_menu import TerminalMenu
from core.connection.databaseChecker import DatabaseConnectionChecker
from core.backups.databaseChecker import DatabaseBackupChecker
from core.restore.databaseRestoreHandler import DatabaseRestoreHandler
from core.service_storage.serviceStorageHandler import ServiceStorageHandler
from core.encrypt import encriptText, decriptText
import os
import uuid
import getpass
import typer
from rich.console import Console
from rich.table import Table
from rich import box
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

console = Console()
app = typer.Typer()

opciones=['postgresql','mysql','sqlite']
storage_services = ["aws-s3", "azure-storage"]

data_service = DataService()
database_checker = DatabaseConnectionChecker()
database_backup_checker = DatabaseBackupChecker()
database_restore_handler = DatabaseRestoreHandler()
service_storage_handler = ServiceStorageHandler()

def saveConfig(args):
    """
    Guarda una nueva configuracion de base de datos en el sistema
    """
    showTitle("Guardando nueva configuración de base de datos")
    try:
        engine_menu = TerminalMenu(opciones, title="Selecciona el motor de base de datos: ")
        engine_index = engine_menu.show()
        if engine_index is None:
            print("Operación cancelada.")
            return 1
        if isinstance(engine_index, tuple):
            if len(engine_index) == 0:
                print("Operación cancelada.")
                return 1
            engine_index = engine_index[0]
        engine = opciones[int(engine_index)]

        print(f"{Fore.YELLOW}{Style.BRIGHT}Gestor seleccionado:", engine)

        if engine in ['postgresql', 'mysql']:
            alias = input(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el alias de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
            host = input(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el host de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
            port = input(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el puerto de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
            user = input(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el usuario de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
            password = getpass.getpass(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese la contraseña de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
            db_name = input(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el nombre de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
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
            alias = input(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el alias de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
            db_name = input(f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el nombre del archivo de la base de datos: {Fore.RESET}{Style.RESET_ALL}")
            data = {
                'id': str(uuid.uuid4()),
                'engine': engine,
                'alias': alias,
                'host': '',
                'port': '',
                'user': '',
                'password': encriptText(''),
                'db_name': db_name
            }
            res = data_service.create_config(data)
            headers = ["ID", "Motor", "Alias", "Host", "Port", "User", "DB Name"]
            printTable(headers, [res], title="Configuración Guardada")
            return 0
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Motor de base de datos no soportado.")
            return 1
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error al guardar la configuracion: {e}")
        return 1
    
def listConfigs(args):
    """
    Lista todas las configuraciones de base de datos guardadas en el sistema
    """
    try:
        if not args.alias:
            list = data_service.show_all()
            if not list:
                print("No hay configuraciones guardadas")
                return 1
            headers = ["ID", "Motor", "Alias", "Host", "Port", "User", "DB Name"]
            printTable(headers, list, title="Configuraciones Guardadas")
        elif args.alias:
            item = data_service.show_one(args.alias)
            if not item:
                print("Sin registros")
                return 1
            headers = ["ID", "Motor", "Alias", "Host", "Port", "User", "DB Name"]
            printTable(headers, [item], title="Configuración Encontrada")
            return 0
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error al listar las configuraciones: {e}")
        return 1

def updateConfig(args):
    """
    Actualiza una configuracion de base de datos guardada en el sistema
    """
    showTitle("Actualizando configuración de base de datos")
    if not args.alias:
        print(f"{Fore.RED}{Style.BRIGHT}Ingresa el alias de la configuracion a actualizar")
        return 1
    elif args.alias:
        item = data_service.show_one(args.alias)
        if not item:
            print(f"{Fore.RED}{Style.BRIGHT}No hay registros para ese alias")
            return 1

        print(f"{Fore.CYAN}{Style.BRIGHT}PULSA ENTER PARA MANTENER EL VALOR ACTUAL \n")
        opciones_update = ['default', 'postgresql', 'mysql', 'sqlite']
        engine_menu = TerminalMenu(opciones_update, title="Actualizar el motor de base de datos (" + item[1] + "): ")
        engine_index = engine_menu.show()
        if engine_index is None:
            print(f"{Fore.RED}{Style.BRIGHT}Operación cancelada.")
            return 1
        if isinstance(engine_index, tuple):
            if len(engine_index) == 0:
                print(f"{Fore.RED}{Style.BRIGHT}Operación cancelada.")
                return 1
            engine_index = engine_index[0]
        new_engine = opciones_update[int(engine_index)]

        new_alias = input(f"{Fore.YELLOW}{Style.BRIGHT}Actualizar el alias de la base de datos ({item[2]}): {Fore.RESET}{Style.RESET_ALL}")
        new_host = input(f"{Fore.YELLOW}{Style.BRIGHT}Actualizar el host de la base de datos ({item[3]}): {Fore.RESET}{Style.RESET_ALL}")
        new_port = input(f"{Fore.YELLOW}{Style.BRIGHT}Actualizar el puerto de la base de datos ({item[4]}): {Fore.RESET}{Style.RESET_ALL}")
        new_user = input(f"{Fore.YELLOW}{Style.BRIGHT}Actualizar el usuario de la base de datos ({item[5]}): {Fore.RESET}{Style.RESET_ALL}")
        new_db_name = input(f"{Fore.YELLOW}{Style.BRIGHT}Actualizar el nombre de la base de datos ({item[6]}): {Fore.RESET}{Style.RESET_ALL}")

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
        headers = ["ID", "Motor", "Alias", "Host", "Port", "User", "DB Name"]
        printTable(headers, [res], title="Configuración Actualizada")
        return 0

def deleteConfig(args):
    """
    Elimina una configuracion de base de datos guardada en el sistema
    """
    showTitle("Eliminando configuración de base de datos")
    if not args.alias:
        print(f"{Fore.RED}{Style.BRIGHT}Ingresa el alias de la configuracion a eliminar")
        return 1
    elif args.alias:
        print(f"{Fore.WHITE}{Style.BRIGHT}Eliminando la configuracion con el alias: {args.alias}")
        item = data_service.show_one(args.alias)
        if not item:
            print(f"{Fore.RED}{Style.BRIGHT}No se encontro la configuracion con el alias: {args.alias}")
            return 1
        data_service.delete(str(item[2]))
        print(f"{Fore.GREEN}{Style.BRIGHT}Configuracion de ({item[2]}) eliminada con exito")
        return 0

def checkConnection(args):
    """
    Verifica la conexion de una base de datos
    """
    if not args.alias:
        print(f"{Fore.RED}{Style.BRIGHT}Ingresa el alias de la configuracion a verificar")
        return 1
    elif args.alias:
        item = data_service.show_info_by_alias(args.alias) # Necesitaremos un nuevo método en DataService
        if not item:
            print(f"{Fore.RED}{Style.BRIGHT}Sin registros para ese alias")
            return 1
        print(f"Verificando la conexion con {item[1]} ({args.alias})...")
    passw = decriptText(item[6])
    status = database_checker.verify(item[1], item[3], item[4], item[5], passw, item[7])
    if status:
        print(f"{Fore.GREEN}{Style.BRIGHT}Conexion exitosa")
        return 0
    else:
        print(f"{Fore.RED}{Style.BRIGHT}Conexion fallida")
    return 1

def showHistory(args):
    """
    Muestra el historial de copias de seguridad de base de datos
    """
    try:
        headers = ["ID", "Fecha", "Alias", "Motor", "Tipo", "Duracion(s)", "Tamaño(B)", "Estado", "Ruta", "Destino", "Error"]
        if args.alias and args.status:
            title = f"Historial de la configuración '{args.alias}' con estado '{args.status}'"
            data =  data_service.show_logs(args.alias, args.status)
            printTable(headers, data, title)
            return 0
        elif args.alias:
            title = f"Mostrando el historial de la configuración '{args.alias}'"
            data = data_service.show_logs(args.alias, None)
            printTable(headers, data, title)
            return 0
        elif args.status:
            title = f"Mostrando el historial con estado '{args.status}'"
            data = data_service.show_logs(None, args.status)
            printTable(headers, data, title)
            return 0
        else:
            title = "Mostrando el historial completo"
            data = data_service.show_logs(None, None)
            printTable(headers, data, title)
            return 0
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error al mostrar el historial: {e}")
        return 1

def deleteHistory(args):
    """
    Elimina el historial de copias de seguridad de base de datos
    """
    showTitle("Eliminando historial de copias de seguridad")
    try:
        validate = input(f"¿Estás seguro de que deseas eliminar todo el historial de copias de seguridad realizadas? (s/N): ")
        if validate.lower() != 's':
            print("Operación cancelada.")
            return 1
        data_service.clear_history()
        print("Historial de copias de seguridad eliminado con éxito.")
        return 0
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error al eliminar el historial: {e}")
        return 1

def startBackup(args):
    """
    Inicia una copia de seguridad de base de datos
    """
    showTitle("Iniciando copia de seguridad de base de datos")
    if not args.alias:
        print(f"{Fore.RED}{Style.BRIGHT}Ingresa el alias de la configuracion a utilizar")
        return 1

    data = data_service.show_info_by_alias(args.alias)
    if not data:
        print(f"{Fore.RED}{Style.BRIGHT}Error: La configuración con el alias '{args.alias}' no existe.")
        return 1
        
    engine = data[1]
    db_name = data[7]
    backup_type_arg = args.type.upper() if (hasattr(args, "type") and args.type) else "FULL"
    dest = args.upload if (hasattr(args, "upload") and args.upload in storage_services) else "local"

    check = checkConnection(args)
    if check != 0:
        print(f"{Fore.RED}{Style.BRIGHT}Conexion fallida")
        data_service.add_log(
            alias=args.alias,
            engine=engine,
            backup_type=backup_type_arg,
            duration_seconds=0.0,
            size_bytes=0,
            status="FAILED",
            file_path=None,
            storage_destination=dest,
            error_message="Fallo de conexión a la base de datos antes de iniciar el backup"
        )
        return 1

    print(f"{Fore.GREEN}{Style.BRIGHT}\nIniciando copia de seguridad de la configuracion con el alias: {args.alias}")
    passw = decriptText(data[6])

    try:
        data_verify = database_backup_checker.verify(
            args.alias,
            dest,
            engine,
            data[3],
            data[4],
            data[5],
            passw,
            db_name,
            backup_type=args.type if hasattr(args, "type") else "full"
        )
        if data_verify is None:
            raise RuntimeError("La estrategia de backup retornó un valor nulo o inválido.")
    except Exception as e:
        err_msg = str(e)
        data_service.add_log(
            alias=args.alias,
            engine=engine,
            backup_type=backup_type_arg,
            duration_seconds=0.0,
            size_bytes=0,
            status="FAILED",
            file_path=None,
            storage_destination=dest,
            error_message=f"Error en creación/compresión: {err_msg}"
        )
        print(f"{Fore.RED}{Style.BRIGHT}Error al realizar la copia de seguridad: {err_msg}")
        return 1

    final_file_path = data_verify.get("file_path")
    if dest in storage_services:
        if not final_file_path or not os.path.exists(final_file_path):
            err_msg = "El archivo local de backup no existe o no pudo ser localizado para su carga externa."
            data_service.add_log(
                alias=data_verify["alias"],
                engine=data_verify["engine"],
                backup_type=data_verify["backup_type"],
                duration_seconds=data_verify["duration_seconds"],
                size_bytes=data_verify["size_bytes"],
                status="FAILED",
                file_path=None,
                storage_destination=dest,
                error_message=err_msg
            )
            print(f"{Fore.RED}{Style.BRIGHT}Error de subida: {err_msg}")
            return 1

        try:
            success = service_storage_handler.verify(dest, final_file_path)
            if not success:
                raise RuntimeError(f"El cargador para el servicio {dest} no pudo subir el archivo.")
        except Exception as e:
            err_msg = f"Error al subir a servicio externo: {str(e)}"
            data_service.add_log(
                alias=data_verify["alias"],
                engine=data_verify["engine"],
                backup_type=data_verify["backup_type"],
                duration_seconds=data_verify["duration_seconds"],
                size_bytes=data_verify["size_bytes"],
                status="FAILED",
                file_path=final_file_path,
                storage_destination=dest,
                error_message=err_msg
            )
            print(f"{Fore.RED}{Style.BRIGHT}{err_msg}")
            return 1

    log_file_path = final_file_path
    data_service.add_log(
        alias=data_verify["alias"],
        engine=data_verify["engine"],
        backup_type=data_verify["backup_type"],
        duration_seconds=data_verify["duration_seconds"],
        size_bytes=data_verify["size_bytes"],
        status="SUCCESS",
        file_path=log_file_path,
        storage_destination=dest,
        error_message=None
    )

    if dest in storage_services:
        print(f"{Fore.GREEN}{Style.BRIGHT}\nCopia de seguridad de '{args.alias}' creada y subida a '{dest}' con éxito.")
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}\nCopia de seguridad de '{args.alias}' creada con éxito.")
        print(f"{Fore.GREEN}{Style.BRIGHT}Archivo guardado en: {final_file_path}")
    return 0

def restoreBackup(args):
    """
    Restaura una copia de seguridad de base de datos en base a su ID o alias
    """
    showTitle("Restaurando copia de seguridad de base de datos")
    if not args.alias:
        print(f"{Fore.RED}{Style.BRIGHT}Se requiere el alias de la configuración para la restauración.")
        return 1

    #buscar el último backup exitoso para el alias proporcionado
    if not args.date:
        print(f"{Fore.GREEN}{Style.BRIGHT}Buscando el último backup exitoso para el alias '{args.alias}'...")
        backup_log = data_service.get_latest_successful_backup(args.alias)
        if not backup_log:
            print(f"{Fore.RED}{Style.BRIGHT}No se encontraron backups exitosos para el alias '{args.alias}'.")
            return 1
    #buscar el último backup exitoso antes de la fecha proporcionada (si se proporciona)
    elif args.date:
        print(f"{Fore.GREEN}{Style.BRIGHT}Buscando el último backup exitoso antes de la fecha '{args.date}' para el alias '{args.alias}'...")
        backup_log = data_service.show_last_info_by_date(args.alias, args.date)
        if not backup_log:
            print(f"{Fore.RED}{Style.BRIGHT}No se encontraron backups exitosos antes de la fecha '{args.date}' para el alias '{args.alias}'.")
            return 1

    local_file_path = backup_log[8]
    dest_service = backup_log[9]

    if local_file_path is None:
        print(f"{Fore.RED}{Style.BRIGHT}Error: El backup encontrado no tiene un archivo asociado para restaurar.")
        return 1

    headers = ["Propiedad", "Detalle"]
    
    rows = [
        ["ID del Backup", backup_log[0]],
        ["Fecha y Hora", backup_log[1]],
        ["Alias", backup_log[2]],
        ["Motor", backup_log[3]],
        ["Tipo", backup_log[4]],
        ["Duración", backup_log[5]],
        ["Tamaño", backup_log[6]],
        ["Destino", dest_service],
        ["Archivo Registrado", local_file_path]
    ]
    
    printTable(headers, rows, title="Información del Backup Encontrado para Restauración")

    config_data = data_service.show_info_by_alias(args.alias)
    if not config_data:
        print(f"{Fore.RED}{Style.BRIGHT}Error: No se encontró la configuración para el alias '{args.alias}'.")
        return 1

    downloaded_temp = False
    if not os.path.exists(local_file_path):
        if dest_service in storage_services:
            if dest_service == "aws-s3":
                remote_name = os.path.basename(local_file_path)
            else:
                remote_name = local_file_path  # Azure usa la ruta completa
            
            print(f"{Fore.YELLOW}{Style.BRIGHT}El archivo local no existe. Descargándolo desde {dest_service}...")
            try:
                success = service_storage_handler.download(dest_service, remote_name, local_file_path)
                if not success:
                    print(f"{Fore.RED}{Style.BRIGHT}Error: No se pudo descargar el archivo '{remote_name}' desde '{dest_service}'.")
                    return 1
                downloaded_temp = True
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}Error al descargar de almacenamiento en la nube: {e}")
                return 1
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Error: El archivo de backup '{local_file_path}' no existe localmente y el destino registrado es '{dest_service}'.")
            return 1

    print(f"{Fore.YELLOW}{Style.BRIGHT}\nADVERTENCIA: Esta operación sobreescribirá la base de datos actual.")
    confirm = input(f"{Fore.CYAN}{Style.BRIGHT}¿Estás seguro de que quieres restaurar la base de datos '{config_data[7]}' usando el backup del {backup_log[2]}? (s/N): ")
    if confirm.lower() != 's':
        print("Restauración cancelada.")
        if downloaded_temp and os.path.exists(local_file_path):
            os.remove(local_file_path)
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
            backup_file=local_file_path
        )
        if success:
            print(f"{Fore.GREEN}{Style.BRIGHT}\n¡Restauración completada con éxito!")
            return 0
        else:
            return 1
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}\nError durante la restauración: {e}")
        return 1
    finally:
        # Limpiar el archivo descargado temporalmente
        if downloaded_temp and os.path.exists(local_file_path):
            try:
                os.remove(local_file_path)
                print(f"{Fore.YELLOW}Limpieza: Archivo temporal descargado '{local_file_path}' eliminado.")
            except Exception as ex:
                print(f"Advertencia: No se pudo eliminar el archivo temporal: {ex}")


# Funciones de utilidad para Rich
def printTable(headers, data, title="Tabla de Datos"):
    """
    Imprime una tabla en la consola usando Rich.
    """
    try:
        table = Table(title=title, show_lines=True, box=box.ROUNDED, header_style="bold yellow")
        for header in headers:
            table.add_column(header, no_wrap=True)
        for row in data:
            table.add_row(*[str(item) for item in row])
        console.print(table)
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error al imprimir la tabla: {e}")

def showTitle(title):
    """
    Muestra un título en la consola usando Rich.
    """
    try:
        border_char = "="
        padding = 4
        title = title.upper()
        width = len(title) + 2 * padding
        console.print(f"{border_char * width}")
        console.print(f"{border_char * (padding - 1)} [bold cyan]{title}[/bold cyan] {border_char * (padding - 1)}")
        console.print(f"{border_char * width}")
        console.print("\n")
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error al mostrar el título: {e}")