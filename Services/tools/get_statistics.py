"""Get Statistics"""
import asyncio
from datetime import datetime, UTC
from collections import defaultdict
from calendar import calendar, month_name

from prettytable import PrettyTable

from app.enums.writing_state import WritingState
from app.models.user import User
from app.models.writing import Writing
from app.events.lifespan import init_db


def print_statistics(columns: list[str], rows: list[list[str]]):
    """Print statistics"""
    tabla = PrettyTable()

    # Definir los nombres de las columnas
    tabla.field_names = columns

    # Agregar filas a la tabla
    for row in rows:
        tabla.add_row(row)

    # Imprimir la tabla
    print(tabla)


async def contar_usuarios_recurrentes_por_mes():
    """Count users recurrentes by month"""
    print("\n\nUsuarios Recurrentes por Mes")

    # Obtener todos los usuarios
    usuarios = await User.find_all().to_list()

    # Diccionario para almacenar los resultados
    usuarios_por_mes = defaultdict(int)

    for usuario in usuarios:
        # Obtener todas las escrituras del usuario
        escrituras = await Writing.find({"user_id": usuario.id}).to_list()

        # Obtener los meses en los que el usuario ha escrito
        meses = set()
        for escritura in escrituras:
            mes = escritura.created_at.strftime("%Y-%m")
            meses.add(mes)

        # Si el usuario ha escrito en más de un mes, es recurrente
        if len(meses) > 1:
            for mes in meses:
                usuarios_por_mes[mes] += 1

    # Preparar los datos para mostrar
    columnas = ["Mes", "Usuarios Recurrentes"]
    filas = []

    # Ordenar los meses cronológicamente
    for mes in sorted(usuarios_por_mes.keys()):
        # Convertir el mes de formato 'YYYY-MM' a nombre del mes
        fecha = datetime.strptime(mes, "%Y-%m")
        nombre_mes = month_name[fecha.month]
        filas.append([nombre_mes, usuarios_por_mes[mes]])

    print_statistics(columnas, filas)


async def main():
    """ Main"""

    await init_db()

    # Obtener el primer día del mes actual
    # first_day_of_month = datetime.now(UTC).replace(
    #    day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)

    first_day_of_month = datetime(2025, 10, 1, 0, 0, 0, tzinfo=UTC)

    print("\n\nNew Users")
    new_users = await User.find({"created_at": {"$gte": first_day_of_month}}).to_list()
    columns = ["User", "Created At"]
    rows = []
    for user in new_users:
        rows.append([user.email, user.created_at])

    print_statistics(columns, rows)

    print("\n\nWriting of Month")
    users = await User.find_all().to_list()

    columns = ["User", "Total"]
    rows = []

    for user in users:
        query = {
            "created_at": {"$gte": first_day_of_month},
            "user_id": user.id
        }

        total = await Writing.find(query).count()

        if total > 0:
            rows.append([user.email, total])

    print_statistics(columns, rows)

    print("\n\nWriting by day")

    writings = await Writing.find({"created_at": {"$gte": first_day_of_month}}).to_list()

    columns = ["Date", "Total"]
    rows = []

    writings_by_day = {}
    for writing in writings:
        day = writing.created_at.strftime("%Y-%m-%d")
        writings_by_day[day] = writings_by_day.get(day, 0) + 1

    for day, total in sorted(writings_by_day.items()):
        rows.append([day, total])

    print_statistics(columns, rows)

    print("\n\nWriting in error")
    users = await User.find_all().to_list()

    columns = ["User", "Total"]
    rows = []

    for user in users:
        query = {
            "created_at": {"$gte": first_day_of_month},
            "user_id": user.id,
            "writing_state": WritingState.ERROR
        }

        total = await Writing.find(query).count()

        if total > 0:
            rows.append([user.email, total])

    print_statistics(columns, rows)

    await contar_usuarios_recurrentes_por_mes()

if __name__ == "__main__":
    asyncio.run(main())
