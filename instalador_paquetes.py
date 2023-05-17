import subprocess
import sys

# Instala los paquetes necesarios para arrancar el simulador

def install():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sly"])

    except subprocess.CalledProcessError as e:
        pass

# Método main
if __name__ == '__main__':
    install()