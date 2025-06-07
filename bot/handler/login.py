from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.dispatcher import dp
from bot.handler.functions import check_password
from bot.states import LoginStates
from db.model import User, get_db


@dp.message(Command("login"))
async def command_login(message: Message, state: FSMContext):
    await message.answer(_("📝 Please, enter your username"))
    await state.set_state(LoginStates.username)


@dp.message(LoginStates.username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()
    await state.update_data(username=username)
    await message.answer(_("🔒 Now, enter your password. "))
    await state.set_state(LoginStates.password)


@dp.message(LoginStates.password)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    input_password = message.text.strip()

    async with get_db() as db:
        user = db.query(User).filter_by(username=username).first()

        if not user:
            await message.answer(_("❌ No such user found! Please try again."))
            await state.set_state(LoginStates.username)
            return

        if not check_password(input_password, user.password):
            await message.answer(_("❌ Invalid password! Please try again."))
            await state.set_state(LoginStates.password)
            return

        keyboard = ReplyKeyboardBuilder()
        keyboard.add(KeyboardButton(text=_("🏠 Main menu")))
        markup = keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)

        await state.clear()
        await message.answer(_("✅ You have successfully logged in."), reply_markup=markup)
