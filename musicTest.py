# from music import M
import numpy as np
# import musicalbeeps
# import pygame.midi
# import time

from midiutil import MIDIFile

degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
tempo    = 60  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)

for pitch in degrees:
    MyMIDI.addNote(track, channel, pitch, time, duration, volume)
    time = time + 1

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
# def main():
    # T = M.tables.Basic()
    # H = M.utils.H


    # # 1) start a ѕynth
    # b = M.core.Being()

    # # 2) set its parameters using sequences to be iterated through
    # b.d_ = [1/2, 1/4, 1/4]  # durations in seconds
    # b.fv_ = [0, 1,5,15,150,1500,15000]  # vibrato frequency
    # b.nu_ = [5]  # vibrato depth in semitones (maximum deviation of pitch)
    # b.f_ = [220, 330]  # frequencies for the notes

    # # 3) render the wavfile
    # b.render(30, 'aMusicalSound.wav')  # render 30 notes iterating though the lists above

    # # 3b) Or the numpy arrays directly and use them to concatenate and/or mix sounds:
    # s1 = b.render(30)
    # b.f_ += [440]
    # b.fv_ = [1,2,3,4,5]
    # s2 = b.render(30)
#     pass
# if __name__ == "__main__":
#     main()