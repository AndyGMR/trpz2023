import socket
import threading

from cur.mediator.mediator import Mediator
from cur.observer.observer import AudioEditorObserver
from cur.server.audio_editor_server import AudioEditorServer


def handle_client(client_socket, mediator):
    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break
        response = mediator.handle_command(command)
        client_socket.sendall(response.encode('utf-8'))

    client_socket.close()
    print("Client disconnected.")

def main():
    host = "localhost"
    port = 5514
    observer = AudioEditorObserver()
    server = AudioEditorServer(observer)
    mediator = Mediator(server, observer)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Waiting for connection on {host}:{port}")
        client_sockets = []
        while True:
            client_socket, _ = server_socket.accept()
            client_sockets.append(client_socket)
            observer.subscribe(client_socket)
            print(f'subscriber: {observer.subscribers}')

            client_thread = threading.Thread(target=handle_client, args=(client_socket, mediator))
            client_thread.start()

if __name__ == '__main__':
    main()