from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from datetime import datetime, timedelta
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError, ChatAdminRequiredError
from telethon.tl import types
from colorama import Fore, Style
import os
from time import sleep
import random
from random import randint
from . import mensajes


class TelegramBot():
    def __init__(self, usuario, api_id, api_hash, phone):
        self.cliente = TelegramClient(usuario, api_id, api_hash)
        self.cliente.connect()
        if not self.cliente.is_user_authorized():
            self.cliente.send_code_request(phone)
            self.cliente.sign_in(phone, input('Introduce el código: '))

    def scraping_grupos(self):
        chats = []
        last_date = None
        chunk_size = 250
        self.grupos = []
        result = self.cliente(
            GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash=0
            )
        )
        chats.extend(result.chats)
        for chat in chats:
            try:
                if chat.megagroup == True:
                    self.grupos.append(chat)
            except:
                continue

        print(Fore.RED + "Selecciona el Grupo para extraer los usuarios:")

        contador = 0
        for listado_grupos in self.grupos:
            print(Fore.GREEN + str(contador) + Style.RESET_ALL + " - " + listado_grupos.title)
            contador += 1

        grupos_numero = input("Introduce el número del grupo: ")
        self.grupo_seleccionado = self.grupos[int(grupos_numero)]
        self.grupo_id = self.grupo_seleccionado.id
        self.grupo_hash = self.grupo_seleccionado.access_hash
        print(Fore.RED + 'Extrayendo usuarios...' + Fore.GREEN)
        self.todos_miembros = []
        self.todos_miembros = self.cliente.get_participants(self.grupo_seleccionado, aggressive=True)

    def reenviar_mensajes(self, grupo_origen_id):
        while True:
            errores_impresos = set()  # Conjunto para almacenar errores ya impresos

            try:
                print("Obteniendo mensajes...")
                total_mensajes = 0

                # Obtener mensajes del grupo de origen
                messages = self.cliente.iter_messages(grupo_origen_id)

                # Obtener todos los grupos
                chats = self.cliente.get_dialogs()

                # Iterar sobre los chats para reenviar el mensaje
                for chat in chats:
                    if chat.is_group and chat.id != grupo_origen_id:
                        for message in messages:
                            if isinstance(message, types.MessageService):
                                continue
                            try:
                                self.cliente.forward_messages(chat.id, messages=message)
                                total_mensajes += 1
                            except Exception as e:
                                error_str = str(e)
                                if error_str not in errores_impresos:
                                    print(f"Error al reenviar mensajes al grupo {chat.title}: {error_str}")
                                    errores_impresos.add(error_str)

                        print(f"Mensaje reenviado al grupo {chat.title}: {total_mensajes}")
                        total_mensajes = 0  # Reiniciar el contador para el próximo grupo

                print("Esperar 10 minutos para reenviar mensajes nuevamente.")
                sleep(600)  # Esperar 10 minutos antes de volver a reenviar mensajes

            except Exception as ex:
                print(f"Error general: {ex}")

    def spamear_grupos(self):
        while True:
            try:
                for grupo in self.grupos:
                    mensaje = """AQUI PONE SU MENSAJE QUE GUSTE EJEMPLO
VENDO BOT SPAM
ACEPTO TRATO 
CONTACTO @NONE"""
                    

                    # Reemplazar {{grupo}} con el título del grupo
                    mensaje = mensaje.replace("{{grupo}}", grupo.title)

                    try:
                        print(Fore.BLUE + "Enviando mensaje al grupo:", grupo.title + Style.RESET_ALL)
                        receptor = InputPeerChannel(grupo.id, grupo.access_hash)
                        self.cliente.send_message(receptor, mensaje)
                        sleep(randint(1, 2))
                    except Exception as e:
                        print(Fore.RED + f"No se ha podido enviar un mensaje al grupo {grupo.id}. Error: {e}" + Style.RESET_ALL)

                tiempo_espera = datetime.now() + timedelta(minutes=5)
                print(f"Esperando hasta {tiempo_espera.strftime('%H:%M:%S')} para enviar mensajes nuevamente.")
                sleep(300)  # 300 segundos = 5 minutos

            except Exception as ex:
                print(Fore.RED + f"Error durante el spam: {ex}. Reintentando en 5 minutos." + Style.RESET_ALL)
                sleep(300)  # Esperar 5 minutos antes de reintentar


    def spamear_usuarios(self):
        for datos_usuarios in self.todos_miembros:
            mensaje = random.choice(mensajes.mensajes)
            if datos_usuarios.first_name:
                mensaje = mensaje.replace("{{nombre}}", datos_usuarios.first_name)
            else:
                mensaje = mensaje.replace("{{nombre}}", datos_usuarios.username)
            mensaje = mensaje.replace("{{grupo}}", self.grupo_seleccionado.title)
            try:
                print(Fore.RED + "Enviando mensaje a :", datos_usuarios.username + Style.RESET_ALL)
                receptor = InputPeerUser(datos_usuarios.id, datos_usuarios.access_hash)
                self.cliente.send_message(receptor, mensaje)
                sleep(randint(1, 2))
            except Exception as e:
                print(Fore.YELLOW + f"No se ha podido enviar un mensaje a {datos_usuarios.id}. El error es: {e}" + Style.RESET_ALL)

    def secuestrar_usuarios(self):
        grupos_numero = input("Introduce el número del grupo al que quieres importar los usuarios: ")
        grupo_seleccionado_secuestro = self.grupos[int(grupos_numero)]
        grupo_seleccionado_entidad = InputPeerChannel(grupo_seleccionado_secuestro.id, grupo_seleccionado_secuestro.access_hash)
        for datos_usuario in self.todos_miembros:
            usuario_a_anadir = InputPeerUser(int(datos_usuario.id), int(datos_usuario.access_hash))
            try:
                self.cliente(InviteToChannelRequest(grupo_seleccionado_entidad, [usuario_a_anadir]))
                print(Fore.GREEN + "Se ha añadido a %s al grupo." % (datos_usuario.id) + Style.RESET_ALL)
                print(Fore.BLUE + "    * Durmiendo entre %s y %s segundos." % (5, 8))
                sleep(randint(3, 4))
            except Exception as e:
                print(Fore.YELLOW + f"No se ha podido añadir a {datos_usuario.id}. El error es: {e}" + Style.RESET_ALL)

    def guardar_datos(self):
        datos_dir = os.path.join(os.getcwd(), 'datos')
        if not os.path.exists(datos_dir):
            os.makedirs(datos_dir)
        f = open(os.path.join(os.getcwd(), 'datos', f"{self.grupo_seleccionado.title.replace(' ', '-')}.csv"), "w+", encoding="utf-8")
        f.write("Título del Grupo, ID del Grupo, ID del Usuario, HASH del Usuario, Nickname, Nombre, Apellido\n")
        for datos_usuario in self.todos_miembros:
            string_datos = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(
                self.grupo_seleccionado.title,
                self.grupo_seleccionado.id,
                self.grupo_seleccionado.access_hash,
                datos_usuario.id,
                datos_usuario.access_hash,
                datos_usuario.username,
                datos_usuario.first_name,
                datos_usuario.last_name
            )
            f.write(string_datos + "\n")
        f.close()
        print("Usuarios extraídos con éxito")
