# import the necessary libraries
import simpleaudio as sa
import numpy as np

# define a function to play a sound indicating the start or end of a recording session
def play_sound():
    # set the frequency and duration of the sound
    frequency = 440  # A4 note frequency
    duration = 0.1   # in seconds

    # create a waveform using a sine wave function with the given frequency and duration
    sample_rate = 44100  # samples per second
    amplitude = 16000   # loudness of the sound

    # create a numpy array of samples for the given duration
    # the waveform is a sine wave oscillating at the given frequency
    # the numpy.arange function generates an array of sample indices for the given duration
    # these indices are used to calculate the sine wave at each sample point
    waveform = np.sin(2 * np.pi * np.arange(sample_rate * duration) * frequency / sample_rate)

    # scale the waveform samples to the given amplitude and convert to a 16-bit integer
    # the numpy.array.astype function is used to convert the waveform to 16-bit integers
    # the resulting waveform array is used to create a simpleaudio object
    waveform = (waveform * amplitude).astype(np.int16)

    # create a simpleaudio object to play the waveform
    # the sa.play_buffer function creates a new audio stream object and starts playing it
    # the arguments to this function are:
    #   waveform: the numpy array of audio samples to play
    #   num_channels: the number of audio channels (1 for mono, 2 for stereo)
    #   bytes_per_sample: the number of bytes per audio sample (2 for 16-bit integers)
    #   sample_rate: the number of samples per second
    audio = sa.play_buffer(waveform, 1, 2, sample_rate)

    # wait for the sound to finish playing before returning from the function
    # the audio.wait_done function blocks until the audio stream has finished playing
    audio.wait_done()
