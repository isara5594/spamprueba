from Telegram.telegram import TelegramBot


# Listado de Opciones del BOT. Añadir aquí las opciones futuras. 
listado_opciones = {
    "¿Quieres SPAMEAR este grupo? Y/N: ": bot.spamear_grupos,
    "¿Quieres SPAMEAR a los miembros de este grupo? Y/N: ": bot.spamear_usuarios,
    "¿Quieres IMPORTAR los usuarios de este grupo? Y/N: ": bot.secuestrar_usuarios,
    "¿Quieres almacenar la lista de usuarios? Y/N: ": bot.guardar_datos,
    "¿Quieres REENVIAR mensajes de este grupo a otros grupos? Y/N: ": bot.reenviar_mensajes
}
