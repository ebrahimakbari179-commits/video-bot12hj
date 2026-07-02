import asyncio, logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from database import get_video_by_link, increment_download_count
from config import TOKEN, CHANNELS, MAIN_CHANNEL

logging.basicConfig(level=logging.INFO)
bot, storage, dp = Bot(token=TOKEN), MemoryStorage(), Dispatcher(storage=MemoryStorage())
class Form(StatesGroup): waiting_for_join, waiting_for_forward = State(), State()

async def is_member(user_id, channel_id):
    try: return (await bot.get_chat_member(channel_id, user_id)).status in ["member", "administrator", "creator"]
    except: return False

@dp.message(Command("start"))
async def start(m: types.Message, s: FSMContext):
    u, nj = m.from_user.id, [c for c in CHANNELS if not await is_member(u, c["id"])]
    if nj:
        kb = InlineKeyboardMarkup(row_width=1)
        for c in nj: kb.insert(InlineKeyboardButton(text=f"Join {c['name']}", url=f"https://t.me/{c['id'][1:]}"))
        kb.insert(InlineKeyboardButton(text="I Joined All", callback_data="check"))
        await m.answer("Join channels:\n" + "\n".join(f"- {c['name']}" for c in nj) + "\n\nThen click.", reply_markup=kb)
    else:
        await m.answer("Step 2: Forward 3 posts from @plus_top1 to 3 people.\n\nThen click Done.",
                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Done", callback_data="done")]]))

@dp.callback_query(lambda c: c.data == "check")
async def check(call, s: FSMContext):
    await call.answer(); u, nj = call.from_user.id, [c for c in CHANNELS if not await is_member(u, c["id"])]
    if nj:
        kb = InlineKeyboardMarkup(row_width=1)
        for c in nj: kb.insert(InlineKeyboardButton(text=f"Join {c['name']}", url=f"https://t.me/{c['id'][1:]}"))
        kb.insert(InlineKeyboardButton(text="I Joined All", callback_data="check"))
        await call.message.edit_text("Join:\n" + "\n".join(f"- {c['name']}" for c in nj) + "\n\nThen click.", reply_markup=kb)
    else:
        await call.message.edit_text("Step 2: Forward 3 posts from @plus_top1 to 3 people.\n\nThen click Done.",
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Done", callback_data="done")]]))

@dp.callback_query(lambda c: c.data == "done")
async def done(call, s: FSMContext):
    await call.answer(); await call.message.edit_text("Send video link.")

@dp.message()
async def handle(m: types.Message):
    l = m.text.strip()
    if MAIN_CHANNEL not in l: await m.reply_text(f"Send link from {MAIN_CHANNEL}."); return
    v = get_video_by_link(l)
    if not v: await m.reply_text("Not found."); return
    fid, t, d = v; increment_download_count(l)
    msg = await m.answer_video(video=fid, caption=f"{t}\n\n{d}" if d else t)
    await m.reply_text("Deleted in 20s."); await asyncio.sleep(20)
    try: await msg.delete(); await m.reply_text("Deleted.")
    except: pass

async def main(): await dp.start_polling(bot, timeout=60)
if __name__ == "__main__": asyncio.run(main())





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
