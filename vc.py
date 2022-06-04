from telethon.tl.types import User
from userbot import catub
import asyncio
from userbot.core.managers import edit_delete, edit_or_reply
from .helper.vc_manager import CatVC
from .helper.stream_helper import Stream


plugin_category = "misc"

catub.__class__.__module__ = 'telethon.client.telegramclient'
vc_player = CatVC(catub)

asyncio.create_task(vc_player.start())


@vc_player.app.on_stream_end()
async def handler(_, update):
    await vc_player.handle_next(update)


@catub.cat_cmd(
    pattern="joinvc ?(\S+)? ?(?:-as)? ?(\S+)?",
)
async def joinVoicechat(event):
    chat = event.pattern_match.group(1)
    joinas = event.pattern_match.group(2)

    await edit_or_reply(event, 'Joining VC ......')

    if chat and chat != '-as':
        if chat.strip('-').isnumeric():
            chat = int(chat)
    else:
        chat = event.chat_id

    if vc_player.CHAT_NAME:
        return await edit_delete(event, f'You have already Joined in {vc_player.CHAT_NAME}')

    try:
        vc_chat = await catub.get_entity(chat)
    except Exception as e:
        return await edit_delete(event, f'ERROR : \n{e or "UNKNOWN CHAT"}')

    if isinstance(vc_chat, User):
        return await edit_delete(event, 'Voice Chats are not available in Private Chats')

    if joinas and not vc_chat.username:
        await edit_or_reply(event, 'Unable to use Join as in Private Chat. Joining as Yourself...')
        joinas = False

    out = await vc_player.join_vc(vc_chat, joinas)
    await edit_delete(event, out)


@catub.cat_cmd(
    pattern="leavevc",
)
async def leaveVoicechat(event):
    if vc_player.CHAT_ID:
        await edit_or_reply(event, 'Leaving VC ......')
        chat_name = vc_player.CHAT_NAME
        await vc_player.leave_vc()
        await edit_delete(event, f'Left VC of {chat_name}')
    else:
        await edit_delete(event, "Not yet joined any VC")


@catub.cat_cmd(
    pattern="playf ?(-a)? ?(\S*)?",
)
async def playf_stream(event):
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    if input_str == '' and event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        input_str = reply_message.text
    await edit_or_reply(event, 'Playing in VC ......')
    if not vc_player.CHAT_ID:
        return await edit_or_reply(event, 'Join a VC and use play command')
    if not input_str:
        return await edit_or_reply(event, 'No Input to play in vc')
    if flag:
        resp = await vc_player.play_song(input_str, force=True)
    else:
        resp = await vc_player.play_song(input_str, Stream.video, force=True)
    if resp:
        await edit_delete(event, resp)


@catub.cat_cmd(
    pattern="play ?(-a)? ?(\S*)?",
)
async def play_stream(event):
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    if input_str == '' and event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        input_str = reply_message.text
    await edit_or_reply(event, 'Playing in VC ......')
    if not vc_player.CHAT_ID:
        return await edit_or_reply(event, 'Join a VC and use play command')
    if not input_str:
        return await edit_or_reply(event, 'No Input to play in vc')
    if flag:
        resp = await vc_player.play_song(input_str)
    else:
        resp = await vc_player.play_song(input_str, Stream.video)
    if resp:
        await edit_delete(event, resp)


@catub.cat_cmd(
    pattern="pause",
)
async def pause_stream(event):
    await edit_or_reply(event, 'Pausing VC ......')
    res = await vc_player.pause()
    await edit_delete(event, res)


@catub.cat_cmd(
    pattern="resume",
)
async def pause_stream(event):
    await edit_or_reply(event, 'Resuming VC ......')
    res = await vc_player.resume()
    await edit_delete(event, res)


@catub.cat_cmd(
    pattern="mutevc",
)
async def pause_stream(event):
    await edit_or_reply(event, 'Muting VC ......')
    res = await vc_player.mute()
    await edit_delete(event, res)


@catub.cat_cmd(
    pattern="unmutevc",
)
async def pause_stream(event):
    await edit_or_reply(event, 'Unmuting VC ......')
    res = await vc_player.unmute()
    await edit_delete(event, res)


@catub.cat_cmd(
    pattern="skip",
)
async def pause_stream(event):
    await edit_or_reply(event, 'Skiping Stream ......')
    res = await vc_player.skip()
    await edit_delete(event, res)
