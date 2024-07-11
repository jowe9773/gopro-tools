import moviepy.editor as mp
import numpy as np
import librosa
from scipy.signal import correlate
import os
from scipy.io import wavfile
from file_managers import FileManagers

fm = FileManagers()

# Load video files and extract audio
video1 = fm.load_fn("Select video 1")
video2 = fm.load_fn("Select Video 2")

# Load your video file
clip1 = mp.VideoFileClip(video1)
clip2 = mp.VideoFileClip(video2)

# Extract audio
audio1 = clip1.audio
audio2 = clip2.audio

# Save audio as a temporary WAV file
temp_audio_path = 'temp_audio.wav'
audio1.write_audiofile(temp_audio_path, codec='pcm_s16le')
# Load the WAV file into a NumPy array
rate1, audio_data1 = wavfile.read(temp_audio_path)

#repeat steps for the second audio
audio1.write_audiofile(temp_audio_path, codec='pcm_s16le')

# Load the WAV file into a NumPy array
rate2, audio_data2 = wavfile.read(temp_audio_path)

# Clean up: delete temp_audio_path when done (optional)
if os.path.exists(temp_audio_path):
    os.remove(temp_audio_path)
    print("Removed file!")


# Compute cross-correlation
correlation = correlate(audio_data1, audio_data2)
print("Found correlation")
lag = np.argmax(correlation) - len(audio_data2) + 1

# Calculate the time offset in seconds
time_offset = lag / rate1

# Print the time offset
print(f"The time offset between the two audio tracks is {time_offset} seconds.")
