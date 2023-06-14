from data.config import ADMINS
from loader import bot, dp
from utils.db_api.sqlite import db


block_user = lambda cid, is_blocked: db.update_user_block(is_blocked, cid)
get_user_data = lambda cid: db.user_select(cid=cid)
create_user = lambda cid, full_name: block_user(cid, 0) if get_user_data(cid) else db.add_user(cid, full_name)


async def fmessage(i, cid, mid, rm, count_group, blocked):
    try:
        await bot.copy_message(i, cid, mid, reply_markup=rm)
        count_group += 1
        print('ID si ' + str(i) + " bo'lgan userga yuborildi!")
    except Exception as exception:
        if "was blocked" in str(exception) or "deactivated" in str(exception) or "chat not found" in str(exception):
            block_user(cid, 1)
            blocked += 1
            print(str(i) + " ------ ga bormadi!!!! \n" + str(exception))
        print("Vapshe boshqa xato chiqdi")

    return count_group, blocked


@dp.message_handler(commands=['send'])
async def message_send(m):
    cid = m.from_user.id
    if str(cid) in ADMINS and m.reply_to_message:
        count_group = 0
        blocked = 0
        await bot.send_message(cid, "<b>Boshlandi!</b>", parse_mode="HTML")
        leng = db.users_all_cid()

        mid = m.reply_to_message.message_id
        rm = m.reply_to_message.reply_markup

        for u in leng:
            a = await fmessage(u[0], cid, mid, rm, count_group, blocked)
            count_group, blocked = a
        await bot.send_message(cid,
                               f"*Hammaga sms bordi!*\n\n{count_group} ta guruhga bordi\n{blocked} ta guruhga bormadi",
                               parse_mode="Markdown")


@dp.message_handler(commands=['users'])
async def handler_users(m):
    try:
        cid = m.from_user.id

        if str(cid) not in ADMINS:
            return
        all_users = db.count_users()[0]
        faol_users = db.count_active_users()[0]

        stat_text = f"""<b>
📊┌ STATISTIKA
👥├ A`zolar: {all_users}
👥├ Faol a'zolar: {faol_users}
</b>"""
        await bot.send_message(m.from_user.id, stat_text, parse_mode="HTML")
    except Exception as exception:
        print("command_ss error: " + str(exception))
