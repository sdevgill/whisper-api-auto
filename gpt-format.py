import os
import time

import openai
import tiktoken
from dotenv import load_dotenv, find_dotenv


# Read local .env file
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


separator = "\n--------------------------------\n"


# Get the completion and token count
def get_completion_and_token_count(
    transcript,
    model="gpt-3.5-turbo-16k",
    temperature=0,
    max_tokens=8192,
):
    messages = [
        {
            "role": "system",
            "content": (
                "This is a transcript. "
                "Your task is to format this transcript into clear, readable paragraphs. "
                "You should not change any of the content, nor should you add any summaries or bullet points."
            ),
        },
        {
            "role": "user",
            "content": transcript,
        },
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message["content"]

    token_dict = {
        "prompt_tokens": response["usage"]["prompt_tokens"],
        "completion_tokens": response["usage"]["completion_tokens"],
        "total_tokens": response["usage"]["total_tokens"],
    }

    return content, token_dict


# Process the transcript
def process_transcript(input_file, output_folder):
    with open(input_file, "r", encoding="utf-8") as file:
        transcript = file.read()

    formatted_transcript, token_dict = get_completion_and_token_count(transcript)

    output_file_name = os.path.splitext(os.path.basename(input_file))[0] + "_gpt.txt"
    output_file_path = os.path.join(output_folder, output_file_name)

    # gpt-3.5-turbo-16k pricing -> $0.003 per 1K input tokens and $0.004 per 1K output tokens
    cost = (token_dict["prompt_tokens"] * 0.000003) + (
        token_dict["completion_tokens"] * 0.000004
    )

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(separator)
        file.write(formatted_transcript)
        file.write(separator)
        file.write(f"\nTokens: {token_dict}")
        file.write(f"\nCost: ${cost:.6f}")

    print(
        f"Processed '{input_file}' with gpt.\nTokens: {token_dict},\nCost: ${cost:.6f}"
    )

    return token_dict["total_tokens"], cost


# Process all transcripts in the folder
def process_all_transcripts(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_tokens = 0
    total_cost = 0

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_folder, file_name)
            transcript_tokens, cost = process_transcript(input_file_path, output_folder)
            total_tokens += transcript_tokens
            total_cost += cost

    return total_tokens, total_cost


def main():
    print(separator)
    print("Starting gpt formatting...\n")
    start_time = time.time()

    input_folder = "./output"
    gpt_output_folder = "./gpt_output"

    total_tokens, total_cost = process_all_transcripts(input_folder, gpt_output_folder)

    end_time = time.time()
    time_taken = end_time - start_time

    print(f"\nTotal tokens: {total_tokens}")
    print(f"Total cost: ${total_cost:.6f}")
    print(f"Time taken: {time_taken:.2f} seconds")
    print(separator)


if __name__ == "__main__":
    main()
