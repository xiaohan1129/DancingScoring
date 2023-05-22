#!/usr/bin/env python
# coding: utf-8


#import pandas as pd
import numpy as np
import matplotlib.pylab as plt

from glob import glob

import librosa 
import librosa.display
#import IPython.display as ipd

import os

import math
import moviepy.editor as mpy
import correlation


# Total_velocity of one joint
def tol_velocity(joint_pos):
    #pos = get_joint_pos(joint,fcoor)
    vel = correlation.joint_velocity(joint_pos)
    x_vel = vel[:,0]
    y_vel = vel[:,1]
    z_vel = vel[:,2]
    tol_vel = np.zeros(vel.shape[0])
    tol_vel = np.sqrt((x_vel)**2 + (y_vel)**2 + (z_vel)**2)
    return tol_vel

# Find the local minima of the sequence
def local_minima(x):
    n = len(x)
    minima = []
    for i in range(n-2):
        if x[i] < x[i-1] and x[i] < x[i+1]:
            minima.append(i)
    return np.array(minima)

# Transform video to audio
def audio_converter(video_path, audio_type):
    video = mpy.VideoFileClip(video_path)
    filename = os.path.splitext(os.path.basename(video_path))[0]  # + '.mp3'
    audio = video.audio
    if audio_type == "mp3":
        audio.write_audiofile(filename + '.mp3')
    if audio_type == "wav":
        audio.write_audiofile(filename + '.wav')

    return filename + '.wav'
        
# get the music beat in unit of time
def get_musicbeat_time(file_path):
    audio_files = glob(file_path)[0]
    y, sr = librosa.load(audio_files)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    return librosa.frames_to_time(beats, sr=sr)

# Beat align algorithm
def beat_align(kinematic_beat,music_beat,sigma):
    BA = 0
    kn = len(kinematic_beat)
    for i in range(kn):
        kbeat = kinematic_beat[i]
        mbeat = min(music_beat, key=lambda x: abs(x - kbeat))
        temp = -(kbeat - mbeat)**2 / (2*sigma**2)
        BA += math.exp(temp)
    return BA/kn

def rhythm_matching(pose_file,music_file,sigma,fps):
    fcoor = correlation.preprocess(pose_file)
    dt = 1.0/fps
    BA = 0
    music_beat = get_musicbeat_time(music_file)
    for j in range(11,33):
        rel = correlation.rel_joint_pos(j,fcoor)
        data = tol_velocity(rel)
        kinematic_beat = local_minima(data) * dt
        BA += beat_align(kinematic_beat,music_beat,sigma)
    # # plot the graph and store for visualizing
    # rel19 = correlation.rel_joint_pos(19,fcoor)
    # data19 = tol_velocity(rel19)
    # kb19 = local_minima(data19)*dt
    #
    # # plot
    # fig = plt.figure(figsize=(30, 3))
    # t = np.arange(data19.shape[0]) * dt  # time axis
    # plt.plot(t, data19, label='Kinematic Velovity')
    # plt.vlines(kb19, 0., 0.2, alpha=0.5, color='g', linestyle='--', label='Kinetic Beats')
    # plt.vlines(music_beat, 0., 0.2, alpha=0.5, color='r', linestyle='--', label='Music Beats')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude')
    # plt.legend()
    # fig.savefig('fig.png')

    print(BA/22)
    return BA/22

if __name__ == '__main__':
    audio_converter('D:\Jupyter\pose3d\cxkpromax.mp4', "wav")
    rhythm_matching('D:\Jupyter\pose3d\cxk.txt', 'D:\Jupyter\pose3d\cxkpromax.wav', 0.25, 30)

# # Standard video
# audio_converter('cxkpromax.mp4', "wav")
# audio_converter('cxkpromax.mp4', "mp3")
# # Compared video
# audio_converter('cxk1.mp4', "wav")
# audio_converter('cxk1.mp4', "mp3")
#
# rhythm_matching("3d_joints.txt",'cxkpromax.wav',0.25,30)
# rhythm_matching("3d_joints_cxk1.txt",'cxk1.wav',0.25,30)



# # Only for the graph that can make me write less in final report. Thx God!
# plt.figure(figsize=(30, 3))
#
# music_beat = get_musicbeat_time('cxkpromax.wav')
# fs = 30
# dt = 1.0 / fs
#
# prel19 = rel_joint_pos(19,p_j_list)
# data = tol_velocity(prel19)
# #data = joint_velocity(prel19)[:,0]
# minima = local_minima(data) * dt
# t = np.arange(data.shape[0]) * dt  # time axis
# print(len(minima))
#
# plt.plot(t, data, label='Kinematic velovity')
# plt.vlines(minima, 0., 0.2, alpha=0.5, color='g',linestyle='--', label='Kinetic Beats')
#
# plt.vlines(music_beat, 0., 0.2, alpha=0.5, color='r',linestyle='--', label='Music Beats')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.legend()
# plt.show()






