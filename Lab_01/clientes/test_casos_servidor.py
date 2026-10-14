# Pruebas adicionales del servidor: casos exitosos y casos de error (validaciones de rol, sesión y asignación)
#
# Uso (desde la carpeta raíz del repositorio, con el servidor ya en ejecución):
#     python client/test_casos_servidor.py                 -> usa http://localhost:80
#     python client/test_casos_servidor.py http://IP:PUERTO
#
# Nota: los identificadores de usuario se generan a partir de la hora, así que el script se puede ejecutar
# varias veces seguidas sin borrar server/users.txt ni server/assignments.txt, y no choca con test_virtuallab_client.py.

import io
import sys
import time
import zipfile
from json import loads

import requests
import virtuallab_client

url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:80"

passed = 0
failed = 0


def check(description, obtained, expected):
    global passed, failed
    if obtained == expected:
        passed += 1
        print(f"[OK]    {description}")
    else:
        failed += 1
        print(f"[FALLO] {description}\n        esperado: {expected!r}\n        obtenido: {obtained!r}")


# Identificadores distintos en cada ejecución (si no, la segunda vez los usuarios ya estarían registrados)
run_id = int(time.time()) % 1000000 * 10
prof, prof_pass = run_id + 1, "clave_prof"
other_prof, other_prof_pass = run_id + 2, "clave_prof2"
stud, stud_pass = run_id + 3, "clave_est"
other_stud, other_stud_pass = run_id + 4, "clave_est2"

# ---------------------------------------------------------------- Registro
print("\n== Registro de usuarios ==")
check("registrar profesor", virtuallab_client.registerUser(url, "Ana", prof, "professor", prof_pass),
      "User Ana with role professor registered")
check("registrar segundo profesor", virtuallab_client.registerUser(url, "Luis", other_prof, "professor", other_prof_pass),
      "User Luis with role professor registered")
check("registrar estudiante", virtuallab_client.registerUser(url, "Eva", stud, "student", stud_pass),
      "User Eva with role student registered")
check("registrar segundo estudiante", virtuallab_client.registerUser(url, "Leo", other_stud, "student", other_stud_pass),
      "User Leo with role student registered")
check("registrar un id repetido", virtuallab_client.registerUser(url, "Otra", prof, "student", "x"),
      "User already registered")

# ---------------------------------------------------------------- Operaciones sin sesión
print("\n== Operaciones sin sesión abierta ==")
check("listStudents sin sesión", virtuallab_client.listStudents(url, prof), "error")
check("listProfessorsLabs sin sesión", virtuallab_client.listProfessorsLabs(url, prof), "error")
check("listStudentLabs sin sesión", virtuallab_client.listStudentLabs(url, stud), "error")
check("uploadLab sin sesión", virtuallab_client.uploadLab(url, prof, "client/voltage_divider.zip"), "error")
check("assignLab sin sesión", virtuallab_client.assignLab(url, prof, "voltage_divider", stud), "error")
check("closeSession sin sesión", virtuallab_client.closeSession(url, prof), "error")

# ---------------------------------------------------------------- Sesiones
print("\n== Inicio y cierre de sesión ==")
check("login con contraseña incorrecta", virtuallab_client.openSession(url, prof, "mala"), "error")
check("login con usuario inexistente", virtuallab_client.openSession(url, 123456789, "x"), "error")
check("login profesor", virtuallab_client.openSession(url, prof, prof_pass), "Session was succesfully opened")
check("login segundo profesor", virtuallab_client.openSession(url, other_prof, other_prof_pass),
      "Session was succesfully opened")
check("login estudiante", virtuallab_client.openSession(url, stud, stud_pass), "Session was succesfully opened")
check("login segundo estudiante", virtuallab_client.openSession(url, other_stud, other_stud_pass),
      "Session was succesfully opened")

# ---------------------------------------------------------------- Permisos por rol
print("\n== Permisos por rol ==")
check("estudiante no puede cargar prácticas", virtuallab_client.uploadLab(url, stud, "client/voltage_divider.zip"), "error")
check("estudiante no puede listar estudiantes", virtuallab_client.listStudents(url, stud), "error")
check("estudiante no puede listar prácticas de profesores", virtuallab_client.listProfessorsLabs(url, stud), "error")
check("estudiante no puede asignar prácticas", virtuallab_client.assignLab(url, stud, "voltage_divider", stud), "error")
check("profesor no puede listar prácticas de estudiante", virtuallab_client.listStudentLabs(url, prof), "error")

# ---------------------------------------------------------------- Carga de prácticas
print("\n== Carga de prácticas ==")
check("cargar voltage_divider.zip", virtuallab_client.uploadLab(url, prof, "client/voltage_divider.zip"),
      "File was succesfully received")
check("cargar rc.zip", virtuallab_client.uploadLab(url, prof, "client/rc.zip"), "File was succesfully received")

# ---------------------------------------------------------------- Listados
print("\n== Listados ==")
students = loads(virtuallab_client.listStudents(url, prof))
check("listStudents no incluye profesores", any(str(s["id"]) in (str(prof), str(other_prof)) for s in students), False)
check("listStudents incluye a los estudiantes registrados",
      {str(stud), str(other_stud)} <= {str(s["id"]) for s in students}, True)

labs = loads(virtuallab_client.listProfessorsLabs(url, prof))
lab_names = labs
check("listProfessorsLabs incluye las prácticas cargadas",
      {"voltage_divider.zip", "rc.zip"} <= set(lab_names), True)

# ---------------------------------------------------------------- Asignación
print("\n== Asignación de prácticas ==")
check("asignar práctica existente a estudiante existente",
      virtuallab_client.assignLab(url, prof, "voltage_divider", stud),
      "Lab voltage_divider.zip was succesfully assigned to student " + str(stud))
check("asignar práctica inexistente", virtuallab_client.assignLab(url, prof, "no_existe", stud), "error")
check("asignar a un estudiante inexistente", virtuallab_client.assignLab(url, prof, "voltage_divider", 424242), "error")
check("asignar a un profesor (no es estudiante)", virtuallab_client.assignLab(url, prof, "voltage_divider", other_prof), "error")

check("listStudentLabs del estudiante asignado", loads(virtuallab_client.listStudentLabs(url, stud)),
      ["voltage_divider.zip"])
check("listStudentLabs del estudiante sin asignaciones", loads(virtuallab_client.listStudentLabs(url, other_stud)), [])

# ---------------------------------------------------------------- Descarga
print("\n== Descarga de prácticas ==")


def raw_download(client_id, file_name):
    return requests.get(url + "/download_lab", headers={"X-File-Name": file_name, "X-Client-ID": str(client_id)})


ok = raw_download(stud, "voltage_divider.zip")
check("descarga de práctica asignada (HTTP 200)", ok.status_code, 200)
check("el archivo descargado es un zip con la netlist",
      "voltage_divider.cir" in zipfile.ZipFile(io.BytesIO(ok.content)).namelist(), True)
check("descarga de práctica NO asignada", raw_download(stud, "rc.zip").status_code, 404)
check("descarga por estudiante sin la asignación", raw_download(other_stud, "voltage_divider.zip").status_code, 404)
check("descarga por un profesor", raw_download(prof, "voltage_divider.zip").status_code, 404)
check("descarga de práctica inexistente", raw_download(stud, "no_existe.zip").status_code, 404)

# ---------------------------------------------------------------- Cierre de sesión
print("\n== Cierre de sesión ==")
check("logout profesor", virtuallab_client.closeSession(url, prof), "Session was succesfully closed")
check("logout repetido", virtuallab_client.closeSession(url, prof), "error")
check("profesor sin sesión no puede listar estudiantes", virtuallab_client.listStudents(url, prof), "error")
check("estudiante con sesión cerrada no puede descargar", (virtuallab_client.closeSession(url, stud),
      raw_download(stud, "voltage_divider.zip").status_code), ("Session was succesfully closed", 404))
virtuallab_client.closeSession(url, other_prof)
virtuallab_client.closeSession(url, other_stud)

print(f"\nResultado: {passed} pruebas correctas, {failed} fallidas")
sys.exit(1 if failed else 0)