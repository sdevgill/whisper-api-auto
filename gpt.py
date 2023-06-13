import os
import time

import openai
from dotenv import dotenv_values


config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]


separator = "\n--------------------------------\n"


def process_text_with_gpt(text):
    max_tokens = 2000  # 8,192 - 192: Reserve tokens for the prompt and other overheads

    edited_text = ""
    total_tokens = 0

    # message = [
    #     {
    #         "role": "system",
    #         "content": (
    #             """
    #             This is a transcript from a podcast. Please summarize it. Then, list key points in bullet points. Finally, write a conclusion.\n
    #             """
    #         ),
    #         "role": "user",
    #         "content": f""" {text} """,
    #     }
    # ]

    message = [
        {
            "role": "system",
            "content": (
                """
                This is a transcript. Your task is to format this transcript into clear, readable paragraphs. You should not change any of the content, nor should you add any summaries or bullet points.
                """
            ),
            "role": "user",
            "content": f""" {text} """,
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        # model="gpt-4",
        messages=message,
        max_tokens=max_tokens,
        temperature=0.5,  # 0.5 works best for transcribing into paragraphs
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    edited_chunk = response.choices[0].message.content.strip()
    edited_text += " " + edited_chunk

    total_tokens += response.usage.total_tokens

    return edited_text.strip(), total_tokens


# Process the file
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
        f"Processed '{input_file}' with gpt. Tokens: {file_tokens}, Cost: ${file_tokens * 0.000002:.6f}"
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
    print("Starting gpt processing...\n")
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
