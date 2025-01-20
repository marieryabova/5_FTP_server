import socket
import os
import threading
import json

# Задайте рабочую директорию.  Убедитесь, что она существует!
WORKING_DIRECTORY = "docs"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            request = json.loads(data)
            command = request["command"]

            response = {"status": "error", "message": ""}  #По умолчанию ошибка
            try:
                if command == "list":
                    files = os.listdir(WORKING_DIRECTORY)
                    response["status"] = "success"
                    response["files"] = files
                elif command == "mkdir":
                    os.mkdir(os.path.join(WORKING_DIRECTORY, request["name"]))
                    response["status"] = "success"
                elif command == "rmdir":
                    os.rmdir(os.path.join(WORKING_DIRECTORY, request["name"]))
                    response["status"] = "success"
                elif command == "create_file":
                    with open(os.path.join(WORKING_DIRECTORY, request["name"]), "w") as f:
                        f.write(request["content"])
                    response["status"] = "success"
                elif command == "rename":
                    os.rename(os.path.join(WORKING_DIRECTORY, request["old_name"]), os.path.join(WORKING_DIRECTORY, request["new_name"]))
                    response["status"] = "success"
                elif command == "copy":
                    os.copy(os.path.join(WORKING_DIRECTORY, request["old_name"]), os.path.join(WORKING_DIRECTORY, request["new_name"]))
                    response["status"] = "success"
                elif command == "get_file":
                    with open(os.path.join(WORKING_DIRECTORY, request["name"]), "r") as f:
                        content = f.read()
                        response["status"] = "success"
                        response["content"] = content
                elif command == "remove_file":
                    os.remove(os.path.join(WORKING_DIRECTORY, request["name"]))
                    response["status"] = "success"
                else:
                    response["message"] = "Unknown command"
            except Exception as e:
                response["message"] = str(e)

            conn.send(json.dumps(response).encode())

    except Exception as e:
        print(f"Ошибка обработки клиента {addr}: {e}")
    finally:
        conn.close()
        print(f"[CONNECTION CLOSED] {addr} disconnected.")


def start_server():
    if not os.path.exists(WORKING_DIRECTORY):
        os.makedirs(WORKING_DIRECTORY)

    HOST = '127.0.0.1'
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен на {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
