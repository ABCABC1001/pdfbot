import os
import shutil

from aiogram import Dispatcher, types
from aiogram.types import Message, InputFile

from pypdf import PdfMerger


async def user_start(message: Message):
    await message.reply("Hello, user!")


async def save_pdf_to_directory(message: Message):
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    await message.document.download(destination_file=file_path)
    await message.answer(f"Файл:\n{message.document.file_name} загружен.")


def union_pdf():
    directory_in_str = './documents'
    result_pdf = 'result.pdf'
    directory = os.fsencode(directory_in_str)

    merger = PdfMerger()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        merger.append(f"{directory_in_str}/{filename}")

    merger.write(f"{directory_in_str}/{result_pdf}")
    merger.close()


async def union_pdf_files(message: Message):
    directory_in_str = './documents'
    result_path = './documents/result.pdf'

    if os.path.exists(directory_in_str):
        union_pdf()

        await message.answer_document(InputFile(result_path))

    try:
        path = os.path.join(directory_in_str)
        shutil.rmtree(path)
    except:
        pass


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(save_pdf_to_directory, state=None, content_types=types.ContentType.DOCUMENT)
    dp.register_message_handler(union_pdf_files, commands=["pdf"], state=None)
