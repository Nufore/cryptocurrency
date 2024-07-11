from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(
        text=f"Hello, {markdown.hbold(message.from_user.full_name)}!",
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm an {echo} bot."),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("literally"),
                    "any",
                ),
            ),
            markdown.markdown_decoration.quote("message!"),
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
    )


@router.message(Command("test", prefix="!/"))
async def handle_help(message: types.Message):
    text = "Text test message!"
    await message.answer(
        text=text,
    )
