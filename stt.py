import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import threading

model = whisper.load_model("base")

# Global variables
is_recording = False
audio_frames = []
SAMPLE_RATE = 16000

def start_recording():
    global is_recording, audio_frames
    audio_frames = []
    is_recording = True
    print("\n🎙 Recording started... Speak freely!")
    print("⏹ Press ENTER to stop\n")

    def record():
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
            while is_recording:
                data, _ = stream.read(1024)
                audio_frames.append(data.copy())

    # Recording runs in background thread
    thread = threading.Thread(target=record)
    thread.start()
    return thread

def stop_recording():
    global is_recording
    is_recording = False
    print("✅ Recording stopped!")

def save_and_transcribe():
    if not audio_frames:
        return ""
    
    # Combine all recorded audio
    audio_data = np.concatenate(audio_frames, axis=0)
    
    # Save to file
    wav.write("temp_audio.wav", SAMPLE_RATE, audio_data)
    
    # Transcribe
    print("🔄 Transcribing...")
    result = model.transcribe("temp_audio.wav")
    return result["text"].strip()

def listen_until_stop():
    # Start recording in background
    thread = start_recording()
    
    # Wait for user to press ENTER
    input()  # blocks until ENTER pressed
    
    # Stop recording
    stop_recording()
    thread.join()  # wait for thread to finish
    
    # Transcribe and return text
    return save_and_transcribe()


# TEST
if __name__ == "__main__":
    print("=== Push to Talk Test ===")
    print("Speak as long as you want, press ENTER when done\n")
    
    text = listen_until_stop()
    print(f"\n📝 You said: {text}")