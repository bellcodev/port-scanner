#! /bin/python

import socket
import subprocess
import time
import re
import argparse

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
                sock.send(b"GET / HTTP/1.0\r\n\r\n")
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


def scan(
    ip="",
    ports=range(65535),
    delay=0,
    ping=True,
    file=False,
    fileName="scan.txt",
    db=False,
):
    global ping1
    ipos = ""
    with open(fileName, "a", encoding="utf-8") as f:
        if file:
            f.write(f"IP {ip} scan result: \n ------------------------------\n")
        if ping:
            ping1 = subprocess.run(
                ["ping", "-c", "1", ip], capture_output=True, text=True
            )
            ipos = re.search(r"ttl=(\d+)", ping1.stdout.lower())
            if ipos:
                ipos = int(ipos.group(1))
                if ipos >= 128:
                    ipos = "Windows"
                elif ipos >= 64:
                    ipos = "Unix(Linux/Mac)"
                elif ipos >= 255:
                    ipos = "Dispositivo de red"
                else:
                    ipos = "Unknown"
        if not ping or ping1.returncode == 0:
            print(f"{GREEN}[+]{RESET} Escaneando la {ip}")
            openports = 0
            for p in ports:
                time.sleep(int(delay))
                try:
                    sock = socket.socket()
                    result = sock.connect_ex((ip, int(p)))
                    if result == 0:
                        openports += 1
                        serv = service(ip, p)
                        r = f"{p}/{serv}"
                        print(r)
                        if file:
                            f.write(r + "\n")
                    sock.close()
                except Exception as e:
                    print(
                        f"{RED}[-]{RESET} Ha ocurrido un error escaneando el puerto {p}"
                    )
            print(f"{GREEN}[+]{RESET} OS: {ipos if ipos else "Unknown"}")
            f.write(f"[+] OS: {ipos if ipos else "Unknown"}\n")
            print(
                f"{GREEN}[+]{RESET} Escaneo Terminado, se han detectado {openports} puertos abiertos"
            )
            f.write(
                f"[+] Escaneo Terminado, se han detectado {openports} puertos abiertos"
            )
        else:
            print(
                f"{RED}[-]{RESET} La ip {ip} no da ping, revise su conexion con ella o use el parametro -Pn."
            )


parser = argparse.ArgumentParser(description="""Examples:
        python main.py -p- -o scan.txt -Pn 111.111.111.111
""")
parser.add_argument("-p", "--port", help="Puertos a escanear", type=str)
parser.add_argument(
    "-d", "--delay", help="Tiempo de espera entre escaneo y escaneo", type=int
)
parser.add_argument(
    "-Pn",
    "--noping",
    help="Esperar a recibir ping para escanear o no",
    action="store_false",
    dest="np",
)
parser.add_argument("-o", "--output", help="Escribir la salida en un archivo", type=str)
parser.add_argument("ip", help="Ip que recibira el escaneo")

args = parser.parse_args()
scan(
    args.ip,
    args.port.split(",") if args.port != "-" else range(65535),
    args.delay if args.delay else 0,
    args.np,
    True if args.output else False,
    args.output if args.output else "scan.txt",
)
