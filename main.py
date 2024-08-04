from keys import TOKEN, ADMIN
import asyncio
import keyboards
from bd import db_start, edit_profile, create_profile
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

class Statee(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    done = State()
    sendmsg = State()

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()
storage = MemoryStorage()

async def start_bot(bot: Bot):

    await db_start()

dp.startup.register(start_bot)

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(f"Привет, {message.from_user.first_name}!\nЕсли что-то пойдет не так, ты всегда можешь перезапустить бота командой /start",  reply_markup=keyboards.startup_kb)
    await state.set_state(Statee.question1)

@dp.message(Statee.sendmsg)
async def sendmsg(message: Message, state: FSMContext) -> None:
    await message.answer("Передал главному!", reply_markup=keyboards.startup_kb)
    await state.set_state(Statee.question1)
    await bot.send_message(ADMIN, f"Сообщение от пользователя с \nid:{message.from_user.id}\nusername:{message.from_user.username}\n")
    await bot.forward_message(ADMIN, message.chat.id, message.message_id)

@dp.message(Statee.question1)
async def question1(message: Message, state: FSMContext) -> None:
    await create_profile(user_id=message.from_user.id)
    if message.text == "Пройти анкету":
        await message.answer("Как я могу к тебе обращаться?")
        await state.set_state(Statee.question2)
    elif message.text == "Хочу рассказать о новости/проблеме":
        await message.answer("Напиши, чем бы ты хотел поделиться")  
        await state.set_state(Statee.sendmsg)
    else:
        await message.answer("Я тебя не понял, давай еще раз", reply_markup=keyboards.startup_kb)
        

@dp.message(Statee.question2)
async def question2(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Statee.question3)

@dp.message(Statee.question3)
async def question3(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await message.answer("Расскажи о себе")
    await state.set_state(Statee.question4)


@dp.message(Statee.question4)
async def question4(message: Message, state: FSMContext) -> None:
    await state.update_data(info=message.text)
    await message.answer("Как мы можем связаться с тобой?")
    await state.set_state(Statee.question5) 

@dp.message(Statee.question5)
async def question5(message: Message, state: FSMContext) -> None:
    await state.update_data(sociallink=message.text)
    await message.answer("Передал главному!", reply_markup=keyboards.startup_kb)
    data = await state.get_data()   
    user_id = message.from_user.id
    username = message.from_user.username
    await edit_profile(user_id, data)
    await bot.send_message(ADMIN, f"Имя: {data['name']}\nЛет: {data['age']}\nКак связаться: {data['sociallink']}\nИнформация о себе: {data['info']}\nid: {user_id}\nUsername: @{username}")
    await state.set_state(Statee.question1)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    
