from core.core import saveConfig, listConfigs, updateConfig, deleteConfig, showHistory, startBackup, restoreBackup
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Herramienta CLI para copias de seguridad de base de datos.")
    subparsers = parser.add_subparsers(title="Funciones", dest="comando", help="Subcomandos disponibles")

    # Configuraciones de Bases de datos
    parser_store = subparsers.add_parser("save", help="Guarda la configuracion de una nueva base de datos")
    parser_store.set_defaults(func=saveConfig)

    parser_list = subparsers.add_parser("list", help="Lista todas las configuraciones guardadas")
    parser_list.add_argument("-a", "--alias", help="Muestra la configuracion guardada con el alias especificado")
    parser_list.set_defaults(func=listConfigs)

    parser_update = subparsers.add_parser("update", help="Actualiza una configuracion guardada")
    parser_update.add_argument("-a", "--alias", help="Alias de la configuracion a actualizar")
    parser_update.set_defaults(func=updateConfig)

    parser_delete = subparsers.add_parser("delete", help="Elimina una configuracion guardada")
    parser_delete.add_argument("-a", "--alias", help="Alias de la configuracion a eliminar")
    parser_delete.set_defaults(func=deleteConfig)

    # Copias de seguridad de base de datos
    parser_history = subparsers.add_parser("history", help="Muestra el historial de copias de seguridad")
    parser_history.add_argument("-a", "--alias", help="Muestra el historial de la configuracion especificada")
    parser_history.add_argument("-s", "--status", help="Muestra el historial de copias de seguridad con el estado especificado")
    parser_history.set_defaults(func=showHistory)

    parser_start = subparsers.add_parser("start", help="Inicia una copia de seguridad")
    parser_start.add_argument("-a", "--alias", help="Alias de la configuracion a utilizar")
    parser_start.set_defaults(func=startBackup)

    parser_restore = subparsers.add_parser("restore", help="Restaura una copia de seguridad")
    parser_restore.add_argument("-a", "--alias", help="Alias de la copia de seguridad a restaurar")
    parser_restore.add_argument("-d", "--date", help="Fecha de la copia de seguridad a restaurar")
    parser_restore.set_defaults(func=restoreBackup)
                                          
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    sys.exit(args.func(args))

if __name__ == "__main__":
    main()