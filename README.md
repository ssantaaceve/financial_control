# financial_control
App para controlar finanzas en pareja. Proyecto de aprendizaje con Python.

# Program to money managment for couples
## Description
A tool for couples to gain control of their finances, improve their money management skills, and achieve their financial goals together.


## 🧭 Hoja de Ruta General

- [x] Definir la idea y el MVP inicial  
- [x] Crear un prototipo en Python con una interfaz básica  
- [x] Agregar base de datos local usando CSV o SQLite (preferiblemente SQLite)  
- [x] Crear primera versión funcional  
- [ ] Exportar reportes de ingresos y gastos  
- [ ] Construir aplicación web o móvil con React Native  
- [ ] Conectar a base de datos en la nube (Firebase / PostgreSQL)  
- [ ] Lanzar versión beta para pruebas  

---

## 🔧 Technologies to Use  
- Main language: **Python**  
- Local database: `CSV` or `SQLite`  
- Graphical interface (prototype): `Tkinter` or `Streamlit`  
- Future frontend: `React Native`  
- Future backend: `Django` or `Firebase`  
- Version control: `Git & GitHub`  
- Project management: `Jira / GitHub Projects`


## 🔧 GITHUB estructura proyecto
    Tipo	¿Cuándo usarlo?
    feat	Cuando creas una nueva funcionalidad
    fix	Cuando arreglas errores o bugs
    refactor	Cuando mejoras código sin cambiar cómo funciona
    chore	Cambios que no son funcionales, como mover archivos o limpiar
    docs	Cambios en los comentarios o documentación interna
    test	Agregar o modificar pruebas (tests)





## 1.1 - Versión inicial

### 🛣 Roadmap

#### ✅ Creación de la base de datos SQLite

- Instalamos la extensión **SQLite Viewer** para poder visualizar las tablas y hacer consultas como si estuviéramos en Excel.
- Creamos el archivo `db.py` para construir la base de datos desde Python, con los siguientes pasos:
  1. Importamos los módulos `sqlite3` (para la base de datos) y `os` (para manejo del sistema operativo).
  2. Creamos la variable `DB_PATH` para definir la ubicación donde se almacenará la base de datos.
  3. Creamos una función `crear_tablas()` que nos permite conectarnos y manipular la base de datos:
     ```python
     conexion = sqlite3.connect(DB_PATH)
     cursor = conexion.cursor()
     ```
  4. Dentro de esta función usamos `cursor.execute()` para escribir código SQL y crear las tablas.
  5. Creamos tres tablas iniciales: `usuarios`, `parejas` y `movimientos`.
  6. Guardamos los cambios con `conexion.commit()` y cerramos la conexión con `conexion.close()`.

---



#### ✅ Creacion de menu en (`main.py`)
 - Creamo funcion `pantalla_inicial` la cual dara entrada a creacion e usuario o ingreso al app de los usuarios
 - adicionala creamos otras funciones que permiten que este archivo intereactue con los otro archivos con las diferentes funcionalidades de usuario, movimientos y parejas

##### ✅ Registro de usuarios (`usuario.py`)

- Importamos los módulos `sqlite3` y `os`.
- Definimos la variable `DB_PATH` para tener acceso a la base de datos.
- Creamos la función `registrar_usuario(nombre, correo, contraseña)`:
  - Usamos un bloque `try/except` para capturar errores y evitar que el programa se detenga.
  - Conectamos a la base de datos y creamos un cursor.
  - Ejecutamos una sentencia `INSERT` para registrar el usuario:
    ```python
    cursor.execute("INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)", (nombre, correo, contraseña))
    ```
  - El uso de `?` en SQL permite pasar los datos de forma segura (evita inyecciones SQL).
  - Confirmamos los cambios con `conexion.commit()` y cerramos con `conexion.close()`.

---

##### ✅ Registro de parejas (`pareja.py`)

- Importamos `sqlite3` y `os`.
- Definimos `DB_PATH` para acceder a la base de datos.
- Creamos la función `crear_pareja(nombre_pareja, correo_1, correo_2)`:
  - Conectamos a la base de datos y creamos un cursor.
  - Consultamos si los dos correos existen en la tabla `usuarios` usando `SELECT id FROM usuarios WHERE correo = ?`.
  - Validamos que ambos usuarios existan. Si alguno no está registrado, mostramos un mensaje de error y detenemos el proceso.
  - Extraemos los `id` de ambos usuarios.
  - Insertamos la nueva pareja en la tabla `parejas` usando:
    ```python
    cursor.execute("INSERT INTO parejas (nombre, usuario_1_id, usuario_2_id) VALUES (?, ?, ?)", (nombre_pareja, id1, id2))
    ```
  - Guardamos y cerramos con `commit()` y `close()`.

##### ✅ Registro de movimientos (`movimientos.py`)
- Importamos `sqlite3` y `os`.
- Definimos `DB_PATH` para acceder a la base de datos.
- Creamos la función `registrar_movimiento_DB(pareja_id, fecha, categoria, monto, tipo, autor_id, descripcion)`:
  - conectamos base de datos con `conexion` y luego creamos la variable `cursor` para podermodificar o consultar la base de datos,
  - Hacemos validacion si la pareja existe.
    - OJO, cuando usamos .execute y en el còdigo SQL ponemos el valor '?' es necesario en el segundo valor ponerlo como una tupla, ya que este valor solo lee tuplas o listas. si referenciamos el valor como numerico solamente no arrojara el resultado esperado
  - Hacemos validacion si existe el autor
  - validamos ingreso o gasto: creamos un metodo para estandarizar el input que tengamos y que no nos salga error por diferencias en caracteres


---

### 🧠 Notas adicionales

- El uso del cursor es fundamental para leer y escribir datos en SQLite.
- El `try/except` permite detectar errores como si el correo no existe o si hay problemas de conexión.
- Todo está conectado gracias a `DB_PATH`, que actúa como la ruta central de la base de datos.



tools🔧: 
    - Python 
    - tkinter (grapich interfaz y ya incluida en python)
    - sqllite3(Base datos ya incluida en python)    



Pasar a version portafolio 
git checkout main

Pasar a version de desarrollo 
git checkout desarrollo