import socket
import json

def send_request(command, data={}):
    request = {"command": command, **data}
    sock.send(json.dumps(request).encode())
    response = json.loads(sock.recv(1024).decode())
    if response["status"] == "success":
        return response
    else:
        print(f"Ошибка: {response['message']}")
        return None

def main():
    HOST = '127.0.0.1'
    PORT = 65432
    global sock
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        while True:
            command = input("Введите команду (list, mkdir, rmdir, create_file, get_file, rename, copy, remove_file, quit): ")
            if command == "quit":
                break
            elif command == "list":
                response = send_request(command)
                if response:
                    print(response["files"])
            elif command in ["mkdir", "rmdir", "remove_file"]:
                name = input("Введите имя: ")
                response = send_request(command, {"name": name})
            elif command == "create_file":
                name = input("Введите имя файла: ")
                content = input("Введите содержимое файла: ")
                response = send_request(command, {"name": name, "content": content})
            elif command == "rename" or command == "copy":
                old_name = input("Введите старое имя файла: ")
                new_name = input("Введите новое имя файла: ")
                response = send_request(command, {"old_name": old_name, "new_name": new_name})
            elif command == "get_file":
                name = input("Введите имя файла: ")
                response = send_request(command, {"name": name})
                if response and "content" in response:  # Проверка наличия поля "content"
                    print(response["content"])
            else:
                print("Неизвестная команда.")

if __name__ == "__main__":
    main()
