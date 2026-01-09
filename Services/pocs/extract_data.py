"""Extract Data"""
import asyncio
import os

from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_community.callbacks.manager import get_openai_callback

from app.enums.deployment import Deployment
from app.enums.provider import Provider
from app.factories.language_model_factory import LanguageModelFactory
from app.models.token_usage import TokensUsage
from app.services.image_service import ImageService


async def transcribe_agent(image_url):
    """ Transcribe Agent"""
    llm = LanguageModelFactory.create_model(
        Provider.GROQ, Deployment.LLAMA4)

    transcribe_prompt = HumanMessagePromptTemplate.from_template(
        template=[
            {"type": "text", "text": "Transcribe la imagen, no corrijas el texto, solo transcribe lo que ves."},
            {"type": "image_url", "image_url": "{encoded_image_url}"}
        ]
    )

    messages = [
        transcribe_prompt
    ]

    chat_prompt = ChatPromptTemplate.from_messages(messages)
    chain = chat_prompt | llm.model

    with get_openai_callback() as cb:
        translation = await chain.ainvoke(
            {"encoded_image_url": image_url})
        token_usage = TokensUsage(
            prompt_tokens=cb.prompt_tokens,
            completion_tokens=cb.completion_tokens,
            total_tokens=cb.total_tokens,
            total_cost=cb.total_cost,
            cached_tokens=cb.prompt_tokens_cached,
            reasoning_tokens=cb.reasoning_tokens
        )

    return translation.content, token_usage


async def extract_student_parta():
    """ Extract Student Answers"""
    path = "./pocs/data/exam1/PARTA/student"
    text_parta = ""
    total_token_usage = TokensUsage()

    for file in os.listdir(path):
        print(file)

        with open(f"{path}/{file}", "rb") as image_file:
            image_url = await ImageService.encode_to_base64(
                image_file.read(), "image/jpg")
            transcription, token_usage = await transcribe_agent(image_url)
            text_parta += transcription
            total_token_usage += token_usage

    with open("pocs/data/exam1/PARTA/student/llama4_parta.txt", "w", encoding="utf-8") as file:
        file.write(text_parta)

    print("Usage Extract Student Part A:")
    print(total_token_usage.model_dump_json(indent=4))


async def extract_student_partb():
    """ Extract Student Answers"""
    path = "./pocs/data/exam1/PARTB"
    text_partb = ""
    total_token_usage = TokensUsage()

    for file in os.listdir(path):
        print(file)

        with open(f"{path}/{file}", "rb") as image_file:
            image_url = await ImageService.encode_to_base64(
                image_file.read(), "image/jpg")
            transcription, token_usage = await transcribe_agent(image_url)
            text_partb += transcription
            total_token_usage += token_usage

    with open("pocs/data/exam1/PARTB/llama4_partb.txt", "w", encoding="utf-8") as file:
        file.write(text_partb)

    print("Usage Extract Student Part B:")
    print(total_token_usage.model_dump_json(indent=4))


async def extract_teacher_enunciado():
    """ Extract Teacher Enunciado"""
    file_path = "./pocs/data/exam1/PARTA/enunciado.jpg"

    text_enunciado = ""
    total_token_usage = TokensUsage()

    with open(file_path, "rb") as image_file:
        image_url = await ImageService.encode_to_base64(
            image_file.read(), "image/jpg")
        transcription, token_usage = await transcribe_agent(image_url)
        text_enunciado += transcription
        total_token_usage += token_usage

    with open("pocs/data/exam1/PARTA/llama4_enunciado.txt", "w", encoding="utf-8") as file:
        file.write(text_enunciado)

    print("Usage Extract Enunciado:")
    print(total_token_usage.model_dump_json(indent=4))


async def main():
    """ Main"""
    # await extract_student_parta()
    await extract_student_partb()
    await extract_teacher_enunciado()


if __name__ == "__main__":
    asyncio.run(main())
