import socket
import json
from db import get_connection
import datetime

# Claves primarias para cada tabla, para DELETE
TABLAS = {
    "Departamento": ["IDDpto"],
    "Proyecto": ["IDProy"],
    "Ingeniero": ["IDIng"],
    "Ing_Proy": ["IDIng", "IDProy"]
}

def procesar_peticion(data):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        comando = data.get("comando")
        valores = data.get("valores", {})

        if comando == "insertar_departamento":
            sql = "INSERT INTO Departamento (IDDpto, Nombre, Telefono, Fax) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (
                valores["id"], valores["nombre"], valores["telefono"], valores["fax"]
            ))
            conn.commit()
            return {"status": "ok", "mensaje": "Departamento insertado"}

        elif comando == "consultar_proyectos":
            sql = "SELECT IDProy, Nombre FROM Proyecto WHERE IDDpto = %s"
            cursor.execute(sql, (valores["iddpto"],))
            proyectos = cursor.fetchall()
            return {"status": "ok", "proyectos": proyectos}

        elif comando == "consultar_ingenieros":
            sql = """
                SELECT i.IDIng, i.Nombre FROM Ingeniero i
                JOIN Ing_Proy ip ON i.IDIng = ip.IDIng
                WHERE ip.IDProy = %s
            """
            cursor.execute(sql, (valores["idproy"],))
            ingenieros = cursor.fetchall()
            return {"status": "ok", "ingenieros": ingenieros}

        elif comando == "consultar_todo":
            tabla = data.get("tabla")
            cursor.execute(f"SELECT * FROM {tabla}")
            registros = cursor.fetchall()
            return {"status": "ok", "registros": registros}

        elif comando == "insertar":
            tabla = data.get("tabla")
            valores = data.get("valores")
            columnas = ", ".join(valores.keys())
            placeholders = ", ".join(["%s"] * len(valores))
            sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(valores.values()))
            conn.commit()
            return {"status": "ok", "mensaje": f"Insertado en {tabla}"}

        elif comando == "actualizar":
            tabla = data.get("tabla")
            valores = data.get("valores")
            claves = list(valores.keys())
            set_clause = ", ".join([f"{k} = %s" for k in claves[1:]])
            sql = f"UPDATE {tabla} SET {set_clause} WHERE {claves[0]} = %s"
            cursor.execute(sql, tuple([valores[k] for k in claves[1:]] + [valores[claves[0]]]))
            conn.commit()
            return {"status": "ok", "mensaje": f"Actualizado en {tabla}"}

        elif comando == "eliminar":
            tabla = data.get("tabla")
            clave = data.get("clave")
            if tabla not in TABLAS:
                return {"status": "error", "mensaje": "Tabla desconocida"}
            clave_col = TABLAS[tabla][0]
            sql = f"DELETE FROM {tabla} WHERE {clave_col} = %s"
            cursor.execute(sql, (clave,))
            conn.commit()
            return {"status": "ok", "mensaje": f"Eliminado de {tabla}"}

        elif comando == "insertar_ingproy":
            id_ing = valores.get("IDIng")
            id_proy = valores.get("IDProy")
            sql = "INSERT INTO Ing_Proy (IDIng, IDProy) VALUES (%s, %s)"
            cursor.execute(sql, (id_ing, id_proy))
            conn.commit()
            return {"status": "ok", "mensaje": "Asignación creada"}

        elif comando == "eliminar_ingproy":
            id_ing = valores.get("IDIng")
            id_proy = valores.get("IDProy")
            sql = "DELETE FROM Ing_Proy WHERE IDIng = %s AND IDProy = %s"
            cursor.execute(sql, (id_ing, id_proy))
            conn.commit()
            return {"status": "ok", "mensaje": "Asignación eliminada"}

        elif comando == "listar_ingproy":
            sql = """
                SELECT i.IDIng, i.Nombre, p.IDProy, p.Nombre
                FROM Ing_Proy ip
                JOIN Ingeniero i ON ip.IDIng = i.IDIng
                JOIN Proyecto p ON ip.IDProy = p.IDProy
            """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return {"status": "ok", "registros": registros}

        # Consulta de proyectos por departamento
        elif comando == "proyectos_por_departamento":
            id_dpto = data.get("IDDpto")
            cursor.execute("SELECT IDProy, Nombre, Fec_Inicio, Fec_Termino FROM Proyecto WHERE IDDpto = %s", (id_dpto,))
            resultados = cursor.fetchall()
            return {"status": "ok", "registros": resultados}

        # Consulta de ingenieros por proyecto
        elif comando == "ingenieros_por_proyecto":
            id_proy = data.get("IDProy")
            cursor.execute("""
                SELECT i.IDIng, i.Nombre, i.Especialidad, i.Cargo
                FROM Ingeniero i
                JOIN Ing_Proy ip ON i.IDIng = ip.IDIng
                WHERE ip.IDProy = %s
            """, (id_proy,))
            resultados = cursor.fetchall()
            return {"status": "ok", "registros": resultados}

        elif comando == "asignar_ingeniero":
            id_proy = data.get("IDProy")
            id_ing = data.get("IDIng")
            sql = "INSERT INTO Ing_Proy (IDIng, IDProy) VALUES (%s, %s)"
            cursor.execute(sql, (id_ing, id_proy))
            conn.commit()
            return {"status": "ok", "mensaje": f"Ingeniero {id_ing} asignado al proyecto {id_proy}"}
        else:
            return {"status": "error", "mensaje": "Comando no reconocido"}

    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def iniciar_servidor(host="localhost", puerto=5000):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(5)
    print(f"[Servidor] Esperando conexión en {host}:{puerto}...")

    while True:
        conn, addr = servidor.accept()
        print(f"[Servidor] Conectado con {addr}")

        data = conn.recv(65536).decode()
        if not data:
            conn.close()
            continue

        peticion = json.loads(data)
        respuesta = procesar_peticion(peticion)

        def convertir_json(obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            return str(obj)

        conn.sendall(json.dumps(respuesta, default=convertir_json).encode())
        conn.close()

if __name__ == "__main__":
    iniciar_servidor()
