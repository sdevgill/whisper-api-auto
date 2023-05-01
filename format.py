import os


def split_text(text, chunk_size=1000):  # Change to 8000 for gpt-3.5-turbo prompts
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


def process_file(input_file, output_folder):
    with open(input_file, "r", encoding="utf-8") as file:
        long_text = file.read()

    splitted_texts = split_text(long_text)

    output_file_name = (
        os.path.splitext(os.path.basename(input_file))[0] + "_formatted.txt"
    )
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, "w", encoding="utf-8") as file:
        for idx, chunk in enumerate(splitted_texts):
            # file.write(f"Chunk {idx + 1}:\n")
            file.write(chunk)
            file.write("\n\n")


def process_all_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_folder, file_name)
            process_file(input_file_path, output_folder)


input_folder = "./output"
formatted_output_folder = "formatted_output"

process_all_files(input_folder, formatted_output_folder)
