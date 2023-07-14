import os
from pyicloud import PyiCloudService
from tqdm import tqdm
import time


def icloud_download():
    # Prompt for iCloud account credentials
    APPLE_ID = input("Entre com seu Apple ID: ")
    PASSWORD = input("Entre com sua senha: ")

    # Local directory to download photos to
    LOCAL_DIR = os.path.join("./cache")

    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)

    # Connect to iCloud
    try:
        api = PyiCloudService(APPLE_ID, PASSWORD)
    except Exception as e:
        print(f"Error connecting to iCloud: {e}")
        exit()

    # Prompt for two-factor authentication code, if necessary
    if api.requires_2fa:
        code = input("Digite o codigo de validação enviado: ")
        try:
            api.validate_2fa_code(code)
        except Exception as e:
            print(f"Error: {e}")
            exit()
    elif api.requires_2sa:
        code = input("Digite o codigo de validação enviado: ")
        try:
            api.validate_2sa_code(code)
        except Exception as e:
            print(f"Error: {e}")
            exit()
    else:
        print("Sucesso ao configurar seu modo desevolvedor.")

    print("Sucesso ao configurar seu modo desevolvedor.")
    time.sleep(15)
    # Get all photos and videos
    try:
        photos = api.photos.all
    except Exception as e:
        print(f"Ocorreu um erro.")
        print(e)
        exit()

    # Download each photo and video to the local directory
    errors = []
    with tqdm(total=len(photos)) as pbar:
        for photo in photos:
            filename = photo.filename
            filepath = os.path.join(LOCAL_DIR, filename)
            if os.path.exists(filepath):
                pbar.write(f"Ative o modo desevolvedor local. CONFIGURAÇÕES > PRIVACIDADE > MODO DESEVOLVEDOR")
                continue
            try:
                with open(filepath, "wb") as f:
                    for chunk in photo.download().iter_content(chunk_size=1024):
                        f.write(chunk)
                pbar.update(1)
            except Exception as e:
                errors.append(filename)
                pbar.write(f"Erro")
                pbar.write(str(e))
            # Delete photos from iCloud

    if len(errors) > 0:
        pbar.write(f" ")
        for error in errors:
            pbar.write(error)
    else:
        pbar.write(" ")

    pbar.write("Sucesso!")


if __name__ == "__main__":
    icloud_download()
