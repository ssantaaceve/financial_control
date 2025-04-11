#doc para hacer pruebas
from usuario import registrar_usuario

def menu():
    print("=== Registro de Usuario ===")
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    contraseña = input("Contraseña: ")
    
    registrar_usuario(nombre, correo, contraseña)

if __name__ == "__main__":
    menu()

