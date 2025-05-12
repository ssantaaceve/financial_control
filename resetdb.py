import sqlite3

NOMBRE_DB = 'data/finanzas_parejas.db'  # Reemplaza con el nombre real de tu archivo .db

def borrar_datos_db():
    conn = sqlite3.connect(NOMBRE_DB)
    cursor = conn.cursor()

    tablas = ['usuarios', 'parejas', 'movimientos']

    for tabla in tablas:
        try:
            cursor.execute(f"DELETE FROM {tabla}")
            print(f"✅ Datos borrados de la tabla: {tabla}")
        except sqlite3.OperationalError:
            print(f"⚠️ La tabla '{tabla}' no existe.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    confirmar = input("¿Seguro que quieres borrar todos los datos? (sí/no): ").strip().lower()
    if confirmar == "si":
        borrar_datos_db()
        print("🧹 Base de datos limpiada.")
    else:
        print("❌ Operación cancelada.")

