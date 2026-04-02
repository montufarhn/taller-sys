import os
import subprocess
import sys
import time
import webbrowser
import socket
from pathlib import Path

SERVICE_NAME = "TallerProAutoService"
LOCAL_PORT = 8000


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


def query_service():
    try:
        output = subprocess.check_output(["sc", "query", SERVICE_NAME], stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as exc:
        return exc.output


def service_status():
    output = query_service()
    if "RUNNING" in output:
        return "RUNNING"
    if "STOPPED" in output:
        return "STOPPED"
    if "The specified service does not exist" in output:
        return "MISSING"
    if "FAILED" in output or "STATE" in output:
        return "OTHER"
    return "UNKNOWN"


def start_service():
    proc = subprocess.run(["sc", "start", SERVICE_NAME], capture_output=True, text=True)
    if proc.returncode != 0:
        return False, proc.stdout + proc.stderr

    for _ in range(10):
        if service_status() == "RUNNING":
            return True, proc.stdout + proc.stderr
        time.sleep(1)
    return False, proc.stdout + proc.stderr


def open_browser():
    try:
        webbrowser.open(f"http://127.0.0.1:{LOCAL_PORT}")
    except Exception:
        pass


def main():
    base_dir = Path(__file__).resolve().parent
    os.chdir(base_dir)

    print("========================================")
    print("Taller Pro Auto - Iniciando servicio")
    print("========================================")

    status = service_status()
    if status == "MISSING":
        print("El servicio no está instalado. Instala la aplicación primero.")
        input("Presiona Enter para cerrar...")
        return

    if status == "STOPPED":
        print("Servicio detenido. Iniciando servicio...")
        started, output = start_service()
        if not started:
            print("No se pudo iniciar el servicio. Revisa los privilegios o los registros.")
            print("Salida de SC:")
            print(output.strip())
            input("Presiona Enter para cerrar...")
            return
        status = "RUNNING"

    if status == "RUNNING":
        print("El servicio está en ejecución.")
    else:
        print("Estado del servicio:", status)

    print("")
    print("El servidor estará disponible en:")
    print(f"  http://127.0.0.1:{LOCAL_PORT}")
    for ip in get_local_ips():
        print(f"  http://{ip}:{LOCAL_PORT}")

    print("")
    print("Se abrirá el navegador en unos segundos...")
    time.sleep(2)
    open_browser()
    input("Presiona Enter para cerrar esta ventana...")


if __name__ == "__main__":
    main()
