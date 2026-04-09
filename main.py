import socket
import subprocess
import time

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def service(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ip, port))
        data = sock.recv(1024).decode(errors="ignore")
        if "SSH-" in data:
            return "ssh"
        elif data.startswith("220"):
            return "ftp"
        elif "HTTP/" in data:
            return "http"
        else:
            try:
                sock.send(b'GET / HTTP/1.0\r\n\r\n')
                data2 = sock.recv(1024).decode(errors="ignore")
                if "HTTP/" in data2:
                    return "http"
            except:
                pass

            return "tcp"
    except:
        return "tcp"
    finally:
        sock.close()

def scan(ip = "", ports = range(65535), delay=0, ping=True, file=False, fileName="scan.txt"):
    global ping1
    with open(fileName, "a", encoding="utf-8") as f:
        if file:
            f.write(f"IP {ip} scan result: \n ------------------------------")
        if ping:
            ping1 = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
        if not ping or ping1.returncode == 0:
            print(f"{GREEN}[+]{RESET} Escaneando la {ip}")
            openports = 0
            for p in ports:
                time.sleep(int(delay))
                try:
                    sock = socket.socket()
                    result = sock.connect_ex((ip, p))
                    if result == 0:
                        openports+=1
                        serv = service(ip, p)
                        r = f"{p}/{serv}"
                        print(r)
                        if file:
                            f.write(r + "\n")
                    sock.close()
                except Exception as e:
                    print(f"{RED}[-]{RESET} Ha ocurrido un error escaneando el puerto {p}")
            print(f"{GREEN}[+]{RESET} Escaneo Terminado, se han detectado {openports} puertos abiertos")
        else:
            print(f"{RED}[-]{RESET} La ip {ip} no da ping, revise su conexion con ella o use ping=False.")

host = input("IP Victima: ")
delay = int(input("Tiempo que se tardara para cada escaneo: "))
ping = bool(input("Si quieres comprobar que la ip da ping(True) sino (False): "))
file = bool(input("Guardar la info en un archivo(True), sino (False): "))
scan(ip=host, delay=delay, ping=ping, file=file)
