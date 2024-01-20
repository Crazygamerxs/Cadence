import pyaudio
import wave
from google.cloud import speech
import datetime  # Import the datetime module

# Record audio and save it
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

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Generate a unique filename with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = "Recording_{}.wav".format(timestamp)

    sound_file = wave.open(file_name, "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b"".join(frames))
    sound_file.close()

    return file_name  # Return the generated filename

# Convert audio to text
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

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# Main function
def main():
    file_name = record_and_save()
    speech_to_text(file_name)

if __name__ == "__main__":
    main()
