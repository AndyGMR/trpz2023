import socket

def main():
    host = "localhost"
    port = 5513

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        while True:
            command = input("Enter a command: ")
            client_socket.sendall(command.encode())
            response = client_socket.recv(1024).decode()
            print(response)

if __name__ == '__main__':
    main()