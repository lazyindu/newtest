from pyrogram import Client, filters
from info import BotCommands, Messages , LOGGER
from helpers.utils import CustomFilters
from helpers.gdrive_utils import GoogleDrive

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Clone) & CustomFilters.auth_users)
def _clone(client, message):
  user_id = message.from_user.id
  if len(message.command) > 1:
    link = message.command[1]
    LOGGER.info(f'Copy:{user_id}: {link}')
    sent_message = message.reply_text(Messages.CLONING.format(link), quote=True)
    msg = GoogleDrive(user_id).clone(link)
    sent_message.edit(msg)
  else:
    message.reply_text(Messages.PROVIDE_GDRIVE_URL.format(BotCommands.Clone[0]))