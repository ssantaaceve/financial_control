# financial_control
App para controlar finanzas en pareja. Proyecto de aprendizaje con Python.

# Program to money managment for couples
## Description
A tool for couples to gain control of their finances, improve their money management skills, and achieve their financial goals together.


## 🧭 General Roadmap  
- [x] Define idea and initial MVP
- [ ] Create a prototype in Python with a basic interface  
- [ ] Add local database using CSV or SQLite  (prefer SQL lite)
- [ ] Export income and expense reports  
- [ ] Build web or mobile app with React Native  
- [ ] Connect to cloud database (Firebase / PostgreSQL)  
- [ ] Release beta version for testing  

---

## 🔧 Technologies to Use  
- Main language: **Python**  
- Local database: `CSV` or `SQLite`  
- Graphical interface (prototype): `Tkinter` or `Streamlit`  
- Future frontend: `React Native`  
- Future backend: `Django` or `Firebase`  
- Version control: `Git & GitHub`  
- Project management: `Jira / GitHub Projects`



## 1.1 version
    Road map
    - [x] create DB structured sqllite3
        -instalamos extensión SQL lite viewer para ver las tablas y hacer consultar. (como si guera excel)
        -Creamos archivo db.py para crear la base de datos desde python teniendo en cuenta lo siguiente/
         1. Import sqllite3(base de datos) y os(manejo de sistema operativo)
         2. creamos una variable DB_PATH, para poder crear la DB y ubicarla en la ruta correcta.
         3. creamos una funcion crear_tablas() para poder Conectar y manipular la base de datos. importante en este paso
            conexion = sqlite3.connect(DB_PATH) 
            cursor = conexion.cursor() 
         4. Dentro de esa funcion usamos cursor.execute() para empezar a usar codigo SQL y crear las bases de datos
         5. Creamos tres bases de datos iniciales. Usuarios, parejas y movimientos
         6. conexion.commit() guarda los cambios en el archivo .db.
         conexion.close() cierra la conexion
    - [x] Creacion funcion de registro de usuario ##Usuario.py
        -importamos el modulo sqllite 3
        -Importamos modulo os con el cual tenemos desde código python acceso al sistema operativo
        - creamos la variable BD_PATH para tener acceso a la base de datos y modificar DB desde los comando siguiente
        - creamos funcion Registrar_usuario(nombre, correo, contraseña):
        - encerramos el codigo en un TRY para validar si algo sale mal que el codigo no se detenga y continue. OJO TRY va con el except y la variable 'e' esta variable guardar todo lo que se parte del error.
        - creamos la variable conexion para poder conectar la base de datos, usando sqlite3.connect(DB_PATH)
        - Creamos variables 'cursor' la cual es como un lapis dentro de la base de datos que nos permite modificar e incluso leer lo que este en en la DB
        - Usando el método execute empzamos a modificar DB en este caso incertamos para los campos nombre, correo y contraseña y luego asignamos los valores con el comando VALUE (ojo con '?') Este caracter nos permite decirle a la base de datos que sera un dato que le daremos 
        - conexion.commir y cobexion.cole() ???????????????
    - [x] ##Cre




    tools🔧: 
        - Python 
        - tkinter (grapich interfaz y ya incluida en python)
        - sqllite3(Base datos ya incluida en python)
        funcionalidades: 