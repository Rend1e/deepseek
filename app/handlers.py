from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import time
from app.generate import ai_generate
router = Router()

class Gen(StatesGroup):
    wait = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, это бесплатный бот для связи с DeepSeek!\nНапишите Ваш запрос и бот непременно ответит!')
    
@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer('Ожидайте, ждем ответ на Ваш запрос')
    
@router.message()
async def generating(message: Message, state: FSMContext):
    generate_zapos = await message.answer('обработка запроса')
    await state.set_state(Gen.wait)  
    response = await ai_generate(message.text)
    await generate_zapos.delete()
    await message.answer(response) 
    await state.clear()
    