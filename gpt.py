import os
import time

import openai
from dotenv import dotenv_values


config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]


separator = "\n--------------------------------\n"


# Split text into chunks of 8000 characters
def split_text(
    text, chunk_size=8000
):  # 8000 chars for gpt-3.5-turbo prompts, ~1,700 tokens
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    sentences = text.split(". ")

    for sentence in sentences:
        sentence_length = len(sentence) + 1  # Add 1 to account for the removed period
        if current_chunk_size + sentence_length > chunk_size:
            chunks.append(". ".join(current_chunk) + ".")
            current_chunk = [sentence]
            current_chunk_size = sentence_length
        else:
            current_chunk.append(sentence)
            current_chunk_size += sentence_length

    if current_chunk:
        chunks.append(". ".join(current_chunk) + ".")

    return chunks


# Process a chunk of text with gpt-3.5-turbo
def process_text_with_gpt(text):
    max_tokens = 2048  # Reserve tokens for the prompt and other overheads
    chunks = split_text(text, chunk_size=8000)

    edited_text = ""
    total_tokens = 0

    for chunk in chunks:
        message = [
            {
                "role": "system",
                "content": (
                    """
                    Go through the text in triple quotes. Split text into short paragraphs.
                    Do not wrap your response in quotes. Do not change the text content at all.
                    Do not summarize.
                    Your only job is to return the original text, nothing else, just with paragraphs.\n
                    """
                    f""" {chunk} """
                ),
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        edited_chunk = response.choices[0].message.content.strip()
        edited_text += " " + edited_chunk

        total_tokens += response.usage.total_tokens

    return edited_text.strip(), total_tokens


# Process a file with gpt-3.5-turbo
def process_file(input_file, output_folder):
    with open(input_file, "r", encoding="utf-8") as file:
        long_text = file.read()

    edited_text, file_tokens = process_text_with_gpt(long_text)

    output_file_name = os.path.splitext(os.path.basename(input_file))[0] + "_gpt.txt"
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(separator)
        file.write(edited_text)
        file.write(separator)
        file.write(f"\nTokens: {file_tokens}")
        file.write(f"\nCost: ${file_tokens * 0.000002:.6f}")

    print(
        f"Processed '{input_file}' with gpt. Total tokens: {file_tokens}, Cost: ${file_tokens * 0.000002:.6f}"
    )

    return file_tokens


# Process all files in the folder
def process_all_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_tokens = 0
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_folder, file_name)
            file_tokens = process_file(input_file_path, output_folder)
            total_tokens += file_tokens

    return total_tokens


def main():
    print(separator)
    print("Starting gpt processing...")
    start_time = time.time()

    input_folder = "./output"
    gpt_output_folder = "gpt_output"

    total_tokens = process_all_files(input_folder, gpt_output_folder)
    total_cost = total_tokens * 0.000002

    end_time = time.time()
    time_taken = end_time - start_time

    print(f"\nTotal tokens: {total_tokens}")
    print(f"Total cost: ${total_cost:.6f}")
    print(f"Time taken: {time_taken:.2f} seconds")
    print(separator)


if __name__ == "__main__":
    main()
