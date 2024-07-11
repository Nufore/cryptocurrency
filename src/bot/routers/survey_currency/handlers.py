from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .states import Survey
from db.requests import set_user, set_currency_request
from currency_getter import get_currency

router = Router(name=__name__)


@router.message(Command("survey", prefix="!/"))
async def handle_start_survey(message: types.Message, state: FSMContext):
    await set_user(message.from_user.id)
    await state.set_state(Survey.currency)
    await message.answer(
        "Введите код валюты (например BTC)",
    )


@router.message(Survey.currency, F.text)
async def handle_survey_currency(message: types.Message, state: FSMContext):
    await state.update_data(currency=message.text)
    await state.set_state(Survey.max)
    await message.answer(
        f"Записал код валюты {message.text}, теперь укажи пороговое значение MAX"
    )


@router.message(Survey.currency)
async def handle_survey_currency_invalid_content_type(message: types.Message):
    await message.answer(
        "Wrong data!"
    )


@router.message(Survey.max, F.text)
async def handle_survey_max(message: types.Message, state: FSMContext):
    await state.update_data(max=message.text)
    await state.set_state(Survey.min)
    await message.answer(
        f"Максимальное значение записал {message.text}, теперь укажи пороговое значение MIN"
    )


async def send_survey_results(message: types.Message, data: dict) -> None:
    text = f"Results:\ncurrency = {data['currency']}, max = {data['max']}, min = {data['min']}"
    await set_currency_request(
        currency=data['currency'],
        threshold_max=data['max'],
        threshold_min=data['min'],
        tg_user_id=message.from_user.id
    )
    await get_currency.get_curr_name()
    await message.answer(text)


@router.message(Survey.min, F.text)
async def handle_survey_min(message: types.Message, state: FSMContext):
    data = await state.update_data(min=message.text)
    await state.clear()
    await message.answer(
        f"Минимальное значение записал {message.text}"
    )
    await send_survey_results(message, data)
