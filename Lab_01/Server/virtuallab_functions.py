# Se deben codificar las siguientes funciones y replicar la funcionalidad descrita en los comentarios
# Además, para la gestión de usuarios y prácticas de laboratorio se debe hacer uso de archivos de texto no se permite
# el uso de motores de bases de datos


import os
from json import dumps # Convertir diccionario a JSON
from json import loads # Convertir JSON a diccionario

usersFile = "server/users.txt"
assignmentsFile = "server/assignments.txt" # Una línea JSON por asignación: práctica, profesor y estudiante
labsDir = "server/labs"

# Identificadores de los usuarios que tienen la sesión abierta
openSessions = set()

def writeUserDataToFile(user_data):
    with open(usersFile, "a") as file:
        file.write(dumps(user_data) + "\n")

# Retorna el diccionario del usuario con el id dado o None si no está registrado
def getUser(id):
    try:
        with open(usersFile, "r") as file:
            for line in file:
                if line.strip() == "":
                    continue
                user = loads(line)
                if str(user["id"]) == str(id):
                    return user
    except FileNotFoundError:
        pass
    return None

# Retorna True si el usuario tiene el rol indicado y se encuentra con sesión abierta
def hasRoleAndSession(id, role):
    user = getUser(id)
    return user is not None and user["role"] == role and str(id) in openSessions

# Retorna la lista de asignaciones guardadas en el archivo de texto
def readAssignments():
    assignments = []
    try:
        with open(assignmentsFile, "r") as file:
            for line in file:
                if line.strip() != "":
                    assignments.append(loads(line))
    except FileNotFoundError:
        pass
    return assignments

# Las prácticas son archivos zip, se acepta el nombre con o sin la extensión .zip
def labFileName(lab_name):
    if lab_name.endswith(".zip"):
        return lab_name
    return lab_name + ".zip"

# Función para registrar un usuario con nombre name, identificador id, rol role y contraseña password.
# Registra el usuario en el sistema si el id del usuario no existe previamente. Si el usuario se pudo registrar debe retornar "User {name} with role {role} registered" de lo contrario
# debe retornar "User already registered"

def registerUser(name, id, role, password):
    # Evitar identificaciones duplicadas
    if getUser(id) is not None:
        response = "User already registered"
        print(response)
        return response

    user_data = {
        "name": name,
        "id": str(id),
        "role": role,
        "password": password
    }

    writeUserDataToFile(user_data)

    response = f"User {name} with role {role} registered"
    print(response)
    return response



# Función que abre una sesión
# Abre una sesión del usuario 
# lo hace si el id del usuario y la contraseña son correctos
# Si la sesión se pudo abrir debe retornar "Session was succesfully opened" de lo contrario
# debe retornar "error"
def openSession(id,password):
    user = getUser(id)
    if user is None or user["password"] != password:
        response="error"
        print(response)
        return response

    openSessions.add(str(id))
    response="Session was succesfully opened"
    print(response)
    return response

# Función que cierra una sesión
# Cierra una sesión del usuario
# Si la sesión se pudo cerrar debe retornar "Session was succesfully closed" de lo contrario
# debe retornar "error"
def closeSession(id):
    if str(id) not in openSessions:
        response="error"
        print(response)
        return response

    openSessions.remove(str(id))
    response="Session was succesfully closed"
    print(response)
    return response


# Función para recibir una práctica de laboratorio (archivo zip) de un profesor
# Recibe una práctica de laboratorio si el usuario es un profesor y se encuentra con sesión abierta
# Si se recibe el archivo correctamente se debe retornar  "File was succesfully received" de lo contrario
# debe retornar "error"
# Se proporciona un código de ejemplo pero se deben implementar las validaciones de usuario y de sesión abierta
def uploadLab(id,file_name,file_data):
    if not hasRoleAndSession(id, "professor"):
        response="error"
        print(response)
        return response

    upload_dir = labsDir
    os.makedirs(upload_dir, exist_ok=True)

    target_path = os.path.join(upload_dir, file_name)
    with open(target_path, "wb") as f:
            f.write(file_data)
    response="File was succesfully received"
    print(response)
    return response

# Función para enviar una práctica de laboratorio (archivo zip) a un estudiante
# Envía una práctica de laboratorio si el usuario es un estudiante, se encuentra con sesión abierta
# y la práctica de laboratorio está asignada a él.
# Si el archivo no existe debe retornar "error"
# Se proporciona un código de ejemplo pero se deben implementar las validaciones de usuario, sesión abierta y asignación de la práctica de laboratorio
def downloadLab(id,file_name):
    response=f"error"        

    if not hasRoleAndSession(id, "student"):
        print(response)
        return response

    assigned = False
    for assignment in readAssignments():
        if str(assignment["student_id"]) == str(id) and assignment["lab"] == file_name:
            assigned = True
    if not assigned:
        print(response)
        return response

    upload_dir = labsDir
    file_path = os.path.join(upload_dir, file_name)
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            response=f"downloadLab called by user {id}"
            print(response)
            return data
    except FileNotFoundError:
        print(response)
        return response

# Función para listar las prácticas de laboratorio disponibles para un estudiante
# Lista las prácticas de laboratorio disponibles para un estudiante si el usuario es un estudiante y se encuentra con sesión abierta
# Si el usuario no es un estudiante o no tiene sesión abierta debe retornar "error"

def listStudentLabs(id):
    if not hasRoleAndSession(id, "student"):
        response = "error"
        print(response)
        return response

    labs = []
    seen = set()

    for assignment in readAssignments():
        if str(assignment["student_id"]) == str(id):
            lab = assignment["lab"]

            # Añadir cada laboratorio solo una vez
            if lab not in seen:
                labs.append(lab)
                seen.add(lab)

    response = dumps(labs)
    print(response)
    return response



# Función para listar las prácticas de laboratorio cargadas por los profesores
# Lista las prácticas de laboratorio cargadas por los profesores si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta debe retornar "error"   
def listProfessorsLabs(id):
    if not hasRoleAndSession(id, "professor"):
        response="error"
        print(response)
        return response

    labs = []
    if os.path.isdir(labsDir):
        labs = sorted(os.listdir(labsDir))

    response=dumps(labs)
    print(response)
    return response

# Función para listar los estudiantes registrados en el sistema
# Lista los estudiantes registrados en el sistema si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta debe retornar "error"
def listStudents(id):
    if not hasRoleAndSession(id, "professor"):
        response="error"
        print(response)
        return response

    students = []
    try:
        with open(usersFile, "r") as file:
            for line in file:
                if line.strip() == "":
                    continue
                user = loads(line)
                if user["role"] == "student":
                    students.append({"name": user["name"], "id": user["id"]})
    except FileNotFoundError:
        pass

    response=dumps(students)
    print(response)
    return response

# Función para asignar una práctica de laboratorio a un estudiante
# Asigna una práctica de laboratorio a un estudiante si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta o el estudiante no existe o la práctica no existe debe retornar "error"

def assignLab(id, lab_name, student_id):
    response = "error"

    # El usuario debe ser un profesor con sesión abierta
    if not hasRoleAndSession(id, "professor"):
        print(response)
        return response

    # Verificar que el estudiante exista y tenga el rol correcto
    student = getUser(student_id)
    if student is None or student["role"] != "student":
        print(response)
        return response

    # Verificar que el laboratorio exista
    file_name = labFileName(lab_name)
    lab_path = os.path.join(labsDir, file_name)

    if not os.path.isfile(lab_path):
        print(response)
        return response

    # Evitar asignar el mismo laboratorio dos veces al mismo estudiante
    assignments = readAssignments()

    for assignment in assignments:
        if (
            str(assignment["student_id"]) == str(student_id)
            and assignment["lab"] == file_name
        ):
            response = (
                f"Lab {file_name} was succesfully assigned "
                f"to student {student_id}"
            )
            print(response)
            return response

    # Guardar la nueva asignación en el archivo de texto
    os.makedirs(os.path.dirname(assignmentsFile), exist_ok=True)

    assignment = {
        "lab": file_name,
        "professor_id": str(id),
        "student_id": str(student_id)
    }

    with open(assignmentsFile, "a", encoding="utf-8") as file:
        file.write(dumps(assignment) + "\n")

    response = (
        f"Lab {file_name} was succesfully assigned "
        f"to student {student_id}"
    )
    print(response)
    return response
