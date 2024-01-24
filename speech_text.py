import pyaudio
import wave
from google.cloud import speech
import datetime

def record_and_save():
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    frames = []

    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Recording_{timestamp}.wav"

        sound_file = wave.open(file_name, "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

        return file_name


def speech_to_text(file_name):
    client = speech.SpeechClient.from_service_account_file('key.json')

    with open(file_name, 'rb') as f:
        audio_data = f.read()

    audio_file = speech.RecognitionAudio(content=audio_data)

    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code="en-US"
    )

    response = client.recognize(
        config=config,
        audio=audio_file
    )

    transcriptions = [result.alternatives[0].transcript for result in response.results]
    return transcriptions

def save_transcript_to_file(file_name, transcriptions):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_file_name = f"Transcript_{timestamp}.txt"

    with open(transcript_file_name, "w") as file:
        for transcription in transcriptions:
            file.write(transcription + "\n")

    return transcript_file_name

def main():
    file_name = record_and_save()
    transcriptions = speech_to_text(file_name)

    # Print transcriptions to the console
    print("Transcriptions:")
    for idx, transcription in enumerate(transcriptions, start=1):
        print(f"{idx}. {transcription}")

    transcript_file_name = save_transcript_to_file(file_name, transcriptions)

if __name__ == "__main__":
    main()