# Whisper API Auto Transcription

A simple and easy-to-use audio transcription app that uses OpenAI's Whisper API
to transcribe audio files and calculate the transcription cost, automatically.

## Requirements

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/)

## Features

- Supports MP3, WAV, M4A audio formats.
- Automatically transcribes all valid audio files in the input folder.
- Calculates the cost of each transcription based on the audio duration ($0.006 currently).
- Saves transcriptions and costs in separate text files in the output folder.

## Installation

1. Clone this repository and navigate to the project folder

```
git clone git@github.com:sdevgill/whisper-api-auto.git
cd whisper-api-auto
```

2. Run `poetry install` to install the dependencies

```
poetry install
```

## Usage

1. Create an `.env` file in the project folder from the `.env.example` file

```
cp .env.example .env
```

2. Add your OpenAI API key to the `.env` file

```
OPENAI_API_KEY=YOUR_API_KEY
```

3. Create an `input` folder in the project folder and add your audio files to it

4. Run the 'whisper-api-auto.ipynb' notebook
