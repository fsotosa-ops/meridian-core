import secrets
import os

def setup_api_secret():
    env_path = ".env"
    # Genera una llave segura de 32 bytes (64 caracteres aprox)
    new_secret = secrets.token_urlsafe(32)
    secret_line = f"API_SECRET_KEY={new_secret}\n"

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
        
        # Verificar si ya existe para no duplicarla
        exists = any(line.startswith("API_SECRET_KEY=") for line in lines)
        
        if not exists:
            with open(env_path, "a") as f:
                f.write(secret_line)
            print(f"✅ API_SECRET_KEY generada y guardada en {env_path}")
        else:
            print("⚠️ API_SECRET_KEY ya existe en el archivo .env. No se realizaron cambios.")
    else:
        # Crear el archivo si no existe
        with open(env_path, "w") as f:
            f.write(secret_line)
        print(f"🚀 Archivo .env creado con una nueva API_SECRET_KEY.")

if __name__ == "__main__":
    setup_api_secret()