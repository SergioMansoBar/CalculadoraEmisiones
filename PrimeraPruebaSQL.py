import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('huella_carbono.db')
cursor = conn.cursor()

# Insertar un usuario manualmente
cursor.execute('INSERT INTO usuarios (nombre, huella_total) VALUES (?, ?)', ("Usuario Prueba", 123.45))
conn.commit()

# Confirmar y cerrar
print("Usuario insertado correctamente.")
conn.close()