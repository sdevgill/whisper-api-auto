import os
import openai
from dotenv import dotenv_values
from tinytag import TinyTag

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

input_folder = "./input/"
output_folder = "./output/"
valid_extensions = [
    ".mp3",
    ".wav",
    ".m4a",
]  # Add or modify the file extensions as needed
cost_per_minute = 0.006

# Create folders if they doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(input_folder):
    os.makedirs(input_folder)

transcription_count = 0
total_cost = 0

def main():


# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file has a valid audio file extension
    file_extension = os.path.splitext(filename)[1]
    if file_extension in valid_extensions:
        file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(
            output_folder, f"{os.path.splitext(filename)[0]}_transcription.txt"
        )

        # Transcribe the audio file
        with open(file_path, "rb") as audio_file:
            response = openai.Audio.transcribe(model="whisper-1", file=audio_file)

        # Get the duration using TinyTag
        audio = TinyTag.get(file_path)
        duration = audio.duration / 60  # Convert seconds to minutes

        # Calculate the cost
        cost = duration * cost_per_minute
        total_cost += cost

        # Save the transcription to the output folder
        text = response["text"]
        separator = "\n--------------------------------\n"

        with open(output_file_path, "a", encoding="utf-8") as f:
            f.write(separator)
            f.write(text)
            f.write(separator)
            f.write(f"\nCost of this transcription: ~${cost:.4f}\n")

        transcription_count += 1
        print(
            f"Transcription #{transcription_count} for {filename} has been saved. Cost: ~${cost:.4f}"
        )
    else:
        print(f"{filename} has an unsupported file extension. Skipping...")

print(f"\nFinished processing {transcription_count} audio files.\n")
print(f"Total cost: ~${total_cost:.4f}")
