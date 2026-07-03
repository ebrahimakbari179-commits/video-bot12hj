import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from database import get_video_by_link, increment_download_count
from config import TOKEN, CHANNELS, MAIN_CHANNEL

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    waiting_for_join = State()
    waiting_for_forward = State()

async def is_member(user_id, channel_id):
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    not_joined = [ch for ch in CHANNELS if not await is_member(user_id, ch["id"])]

    if not_joined:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for ch in not_joined:
            keyboard.insert(InlineKeyboardButton(text=f"Join {ch['name']}", url=f"https://t.me/{ch['id'][1:]}"))
        keyboard.insert(InlineKeyboardButton(text="I Joined All", callback_data="check_join"))

        text = "Please join the channels below:\n\n"
        for ch in not_joined:
            text += f"- {ch['name']}\n"
        text += "\nAfter joining, click the button."
        await message.answer(text, reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Done", callback_data="done")]
        ])
        await message.answer(
            "Step 2: Forward the last 3 posts from @plus_top1 to 3 people.\n\n"
            "After that, click the button below.",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "check_join")
async def check_join(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    not_joined = [ch for ch in CHANNELS if not await is_member(user_id, ch["id"])]

    if not_joined:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for ch in not_joined:
            keyboard.insert(InlineKeyboardButton(text=f"Join {ch['name']}", url=f"https://t.me/{ch['id'][1:]}"))
        keyboard.insert(InlineKeyboardButton(text="I Joined All", callback_data="check_join"))

        text = "You are not yet a member of these channels:\n\n"
        for ch in not_joined:
            text += f"- {ch['name']}\n"
        text += "\nPlease join them first."
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Done", callback_data="done")]
        ])
        await callback.message.edit_text(
            "Step 2: Forward the last 3 posts from @plus_top1 to 3 people.\n\n"
            "After that, click the button below.",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "done")
async def done(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Please send the link of the video post you want.")

@dp.message()
async def handle_video_link(message: types.Message, state: FSMContext):
    link = message.text.strip()

    if MAIN_CHANNEL not in link:
        await message.reply_text(f"Please send a link from {MAIN_CHANNEL} channel.")
        return

    video = get_video_by_link(link)

    if video:
        file_id, title, description = video
        increment_download_count(link)

        caption = f"{title}\n\n{description}" if description else f"{title}"
        video_msg = await message.answer_video(video=file_id, caption=caption)

        await message.reply_text("This video will be deleted in 20 seconds.")
        await asyncio.sleep(20)
        try:
            await video_msg.delete()
            await message.reply_text("The video has been deleted.")
        except:
            pass
    else:
        await message.reply_text("Video not found in database. Please check the link.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





<!DOCTYPE html>
<html>
    <head>
        <title>Runtime Error</title>
        <meta name="viewport" content="width=device-width" />
        <style>
         body {font-family:"Verdana";font-weight:normal;font-size: .7em;color:black;} 
         p {font-family:"Verdana";font-weight:normal;color:black;margin-top: -5px}
         b {font-family:"Verdana";font-weight:bold;color:black;margin-top: -5px}
         H1 { font-family:"Verdana";font-weight:normal;font-size:18pt;color:red }
         H2 { font-family:"Verdana";font-weight:normal;font-size:14pt;color:maroon }
         pre {font-family:"Consolas","Lucida Console",Monospace;font-size:11pt;margin:0;padding:0.5em;line-height:14pt}
         .marker {font-weight: bold; color: black;text-decoration: none;}
         .version {color: gray;}
         .error {margin-bottom: 10px;}
         .expandable { text-decoration:underline; font-weight:bold; color:navy; cursor:hand; }
         @media screen and (max-width: 639px) {
          pre { width: 440px; overflow: auto; white-space: pre-wrap; word-wrap: break-word; }
         }
         @media screen and (max-width: 479px) {
          pre { width: 280px; }
         }
        </style>
    </head>

    <body bgcolor="white">

            <span><H1>Server Error in '/' Application.<hr width=100% size=1 color=silver></H1>

            <h2> <i>Runtime Error</i> </h2></span>

            <font face="Arial, Helvetica, Geneva, SunSans-Regular, sans-serif ">

            <b> Description: </b>An application error occurred on the server. The current custom error settings for this application prevent the details of the application error from being viewed remotely (for security reasons). It could, however, be viewed by browsers running on the local server machine.
            <br><br>

            <b>Details:</b> To enable the details of this specific error message to be viewable on remote machines, please create a &lt;customErrors&gt; tag within a &quot;web.config&quot; configuration file located in the root directory of the current web application. This &lt;customErrors&gt; tag should then have its &quot;mode&quot; attribute set to &quot;Off&quot;.<br><br>

            <table width=100% bgcolor="#ffffcc">
               <tr>
                  <td>
                      <code><pre>

&lt;!-- Web.Config Configuration File --&gt;

&lt;configuration&gt;
    &lt;system.web&gt;
        &lt;customErrors mode=&quot;Off&quot;/&gt;
    &lt;/system.web&gt;
&lt;/configuration&gt;</pre></code>

                  </td>
               </tr>
            </table>

            <br>

            <b>Notes:</b> The current error page you are seeing can be replaced by a custom error page by modifying the &quot;defaultRedirect&quot; attribute of the application&#39;s &lt;customErrors&gt; configuration tag to point to a custom error page URL.<br><br>

            <table width=100% bgcolor="#ffffcc">
               <tr>
                  <td>
                      <code><pre>

&lt;!-- Web.Config Configuration File --&gt;

&lt;configuration&gt;
    &lt;system.web&gt;
        &lt;customErrors mode=&quot;RemoteOnly&quot; defaultRedirect=&quot;mycustompage.htm&quot;/&gt;
    &lt;/system.web&gt;
&lt;/configuration&gt;</pre></code>

                  </td>
               </tr>
            </table>

            <br>

    </body>
</html>
