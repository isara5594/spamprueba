from Telegram.telegram import TelegramBot
from Telegram.datos import configuracion

bot = TelegramBot(
    configuracion["usuario"],
    configuracion["api_id"],
    configuracion["api_hash"],
    configuracion["phone"]
)

bot.scraping_grupos()

# ID del grupo de origen
grupo_origen_id = -4680633557  # Aquí pones el chat ID del grupo de origen

# Listado de IDs de los grupos destino (se pueden definir de forma automática o manual)
grupos_destino_ids = [-4680633558, -4680633559]  # Aquí pones los IDs de los grupos de destino

# Método para reenviar mensajes de un grupo origen a otros grupos destino
def reenviar_mensajes(grupo_origen_id, grupos_destino_ids):
    mensajes = bot.obtener_mensajes(grupo_origen_id)  # Suponiendo que tienes un método que obtiene los mensajes del grupo
    for mensaje in mensajes:
        for grupo_id in grupos_destino_ids:
            bot.reenviar_mensaje(grupo_origen_id, grupo_id, mensaje)  # Reenvía el mensaje a cada grupo destino

# Listado de Opciones del BOT
listado_opciones = {
    "¿Quieres REENVIAR mensajes de este grupo a otros grupos? Y/N: ": lambda: reenviar_mensajes(grupo_origen_id, grupos_destino_ids),
    "¿Quieres SPAMEAR este grupo? Y/N: ": bot.spamear_grupos,
    "¿Quieres SPAMEAR a los miembros de este grupo? Y/N: ": bot.spamear_usuarios,
    "¿Quieres IMPORTAR los usuarios de este grupo? Y/N: ": bot.secuestrar_usuarios,
    "¿Quieres almacenar la lista de usuarios? Y/N: ": bot.guardar_datos,
}

# Itera sobre el listado de opciones
for pregunta, accion in listado_opciones.items():
    print(pregunta)
    respuesta = input("Respuesta: ").strip().upper()
    if respuesta == "Y":
        accion()

