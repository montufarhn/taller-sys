import os
import socket
from pathlib import Path
import uvicorn


def get_local_ips():
    ips = set()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            ips.add(sock.getsockname()[0])
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for res in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = res[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except Exception:
        pass

    return sorted(ips)


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    os.chdir(base_dir)

    local_ips = get_local_ips()
    print("==========================================")
    print("Taller Pro Auto - Servidor local iniciado")
    print("==========================================")
    print("")
    print("El servidor se está ejecutando en:")
    print("  http://127.0.0.1:8000")
    if local_ips:
        for ip in local_ips:
            print(f"  http://{ip}:8000")
        print("")
        print("Conecta otros equipos en la red local usando cualquiera de las direcciones anteriores.")
    else:
        print("  No se detectó ninguna IP de red local automáticamente.")
        print("  Asegúrate de que esta máquina esté conectada a la red local.")
    print("")
    print("Presiona Ctrl+C para detener el servidor.")
    print("")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
