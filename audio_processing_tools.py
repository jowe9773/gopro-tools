import moviepy.editor as mp
import numpy as np
from scipy.signal import correlate
from scipy.io import wavfile
import tempfile
from file_managers import FileManagers

#instantiate file managers
fm = FileManagers()


# Function to extract audio from video and return as a numpy array
def extract_audio(video_path):

    print(video_path)
    clip = mp.VideoFileClip(video_path)
    audio = clip.audio
    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
        temp_audio_path = temp_audio_file.name
    audio.write_audiofile(temp_audio_path, codec='pcm_s16le')
    rate, audio_data = wavfile.read(temp_audio_path)
    return rate, audio_data

# Load video files and extract audio
video1 = fm.load_fn("Choose video1")  # Replace with actual path or use a file selection method
video2 = fm.load_fn("Choose video2")  # Replace with actual path or use a file selection method

rate1, audio_data1 = extract_audio(video1)
rate2, audio_data2 = extract_audio(video2)

# Ensure the sample rates are the same
if rate1 != rate2:
    raise ValueError("Sample rates of the two audio tracks do not match")

# Convert stereo to mono if necessary
if len(audio_data1.shape) == 2:
    audio_data1 = audio_data1.mean(axis=1)
if len(audio_data2.shape) == 2:
    audio_data2 = audio_data2.mean(axis=1)

# Normalize audio data to avoid overflow
audio_data1 = audio_data1 / np.max(np.abs(audio_data1))
audio_data2 = audio_data2 / np.max(np.abs(audio_data2))

# Compute cross-correlation
correlation = correlate(audio_data1, audio_data2)
lag = np.argmax(correlation) - len(audio_data2) + 1

# Calculate the time offset in seconds
time_offset = lag / rate1

# Print the time offset
print(f"The time offset between the two audio tracks is {time_offset} seconds.")
=