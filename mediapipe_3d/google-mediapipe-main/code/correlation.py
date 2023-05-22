#!/usr/bin/env python
# coding: utf-8



import os
import numpy as np
import matplotlib.pylab as plt

from itertools import cycle
from scipy.fft import fft, ifft
import math
import dtaidistance

# Calculate the absolute joint position
def get_joint_pos(joint,coor):
    return coor[:,joint,:]

# Calculate the Joint Velocities
def joint_velocity(joint_coor):
    n = len(joint_coor)-1
    jv = np.zeros((n,3))
    for i in range(n):
        jv[i] = joint_coor[i+1]-joint_coor[i]
    return jv

# Define the low pass filter function (Gaussian window)
def low_pass_filter(data, fs):   
    dt = 1.0 / fs
    sigma = 0.1 * fs  # cutoff frequency of 6 Hz
    freq = np.fft.fftfreq(data.shape[0], d=dt)  # frequency axis
    gaussian_window = np.exp(-0.5 * ((freq / sigma) ** 2))
    data_dft = fft(data, axis=0)
    # Apply Gaussian window in frequency domain
    data_dft_gaussian = data_dft * gaussian_window[:, np.newaxis]
    # Compute inverse discrete Fourier transform of filtered data
    data_filtered = np.real(ifft(data_dft_gaussian, axis=0))
    return data_filtered

# Filtered absolute joint position coordinate 
def filt_coor(coor,fs):
    filt_coor = np.zeros(coor.shape)
    for j in range(coor.shape[1]):
        filt_coor[:,j,:] = low_pass_filter(coor[:,j,:], fs)
    return filt_coor
        

# Calculate the relative joint position with respect to torso
# P_j(t) = P_j_ab(t) - P_torso_ab(t)
def rel_joint_pos(joint,coor):
    j11 = get_joint_pos(11,coor)
    j12 = get_joint_pos(12,coor)
    j23 = get_joint_pos(23,coor)
    j24 = get_joint_pos(24,coor)
    # absolute position of torso
    torso = np.mean([j11,j12,j23,j24],axis=0)
    j = get_joint_pos(joint,coor)
    return j-torso


def preprocess(filename):
    # Load 3d joints data
    with open (filename, "r") as f:
        data = f. read ()
        
    data_split = data. split ("\n") [: -1]

    # num of frames for one video
    n = len(data_split)
    coor = np.zeros((n, 33, 3))

    # for each frame, get 33 groups of coordinates and store in np. array
    for f in range(n) :
        frame = data_split[f] # one frame data
        c = frame.split ("joints,") [1] # exclude "n, joints,"
        clist = c.split (';') [:-1]
        if len (clist) != 33:
            print (" joints num not match")
            break
        for j in range(33) :
            joint_coor = clist[j][1:-1].split(",") # 3d coordinate of one joint
            for i in range(3) :
                coor[f,j,i] = float(joint_coor[i])
                
    
    fcoor = filt_coor(coor,30) # filtered coordinate
    return fcoor

# p_j_list = preprocess("3d_joints.txt")
# q_j_list = preprocess("3d_joints_cxk1.txt")



def d(p_list, q_list):
    res = 0
    for j in range(p_list.shape[0]):
        res += np.linalg.norm((p_list[j] - q_list[j]), ord=1)
    return res
            
def DTW(p_j_list, q_j_list):
    DTW = np.zeros((p_j_list.shape[0], q_j_list.shape[0]))
    
    for i in range(p_j_list.shape[0]):
        for j in range(q_j_list.shape[0]):
            DTW[i, j] = 1e16
    DTW[0, 0] = 0
    
    for i in range(p_j_list.shape[0]):
        for j in range(q_j_list.shape[0]):
            cost = d(p_j_list[i], q_j_list[j])
            DTW[i, j] = cost + min(DTW[i-1, j  ], 
                                        DTW[i  , j-1], 
                                        DTW[i-1, j-1]) 
    
    return DTW

def local_align(p_j_list, q_j_list):
    m = DTW(p_j_list, q_j_list)
    path = dtaidistance.dtw.best_path(m)
    p_j_list_new = []
    q_j_list_new = []
    for pair in path:
        p_j_list_new.append(p_j_list[pair[0]])
        q_j_list_new.append(q_j_list[pair[1]])
    
    p_j_list_new = np.array(p_j_list_new)
    q_j_list_new = np.array(q_j_list_new)
    return p_j_list_new, q_j_list_new



# calculate the k
# input is the numpy array 
def stretch(p_j_list, q_j_list):
    p_mod = 0
    for t in range(len(p_j_list)):
        for j in range(len(p_j_list[0])):
            tmp = 0
            for i in range(3):
                tmp += abs(p_j_list[t][j][i])
            p_mod += tmp
    q_mod = 0
    for t in range(len(q_j_list)):
        for j in range(len(q_j_list[0])):
            tmp = 0
            for i in range(3):
                tmp += abs(q_j_list[t][j][i])
            q_mod += tmp
    return math.sqrt(p_mod/q_mod)

def centroid(p_j_list):
    res = np.zeros(3)
    for t in range(len(p_j_list)):
        for j in range(len(p_j_list[0])):
            res += p_j_list[t][j]
            
    return 1.0*res/(len(p_j_list)*len(p_j_list[0]))

# p and q are both vectors of size 3
def unit_mult(p, q):
    # we only consider the first term if no rotation invariant metrics are considered
    return np.array([p[0]*q[0]+p[1]*q[1]+p[2]*q[2], p[2]*q[1]-p[1]*q[2], p[0]*q[2]-p[2]*q[0], p[1]*q[0]-p[0]*q[1]])

# p_list is the list of all vectors
def p_c(p_list):
    p_c = np.zeros(3)
    for i in range(len(p_list)):
        p_c += p_list[i]
    p_c = 1.0*1/len(p_list)*p_c
    return p_c

# calculate C_tau for a specifc time slot
def _covariance(p_list, q_list, tau):
    res = np.zeros(4)
    pc = p_c(p_list)
    qc = p_c(q_list)
    for t in range(len(p_list)):
        p = p_list[t] - pc
        if t-tau >= 0 and t - tau < len(q_list):
            q = q_list[t-tau] - qc
        else:
            q = np.array([0]*4)
        res += unit_mult(p, q)
    return 1.0*res/len(p_list)

def calc_norm(q):
    return np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)

# TODO: take joints into consideration
# calculate the entire covariance for a specific time slot
def covariance(p_j_list, q_j_list):
    res = 0
    k = stretch(p_j_list, q_j_list)
    d = -centroid(q_j_list) + centroid(p_j_list)
    print("k = ", k)
    print("d = ", d)
    coeff_dict = {}
    for i in range(11):
        coeff_dict[i] = 0.0
    for i in range(17, 23):
        coeff_dict[i] = 0.5
    for i in range(29,33):
        coeff_dict[i] = 0.5
    for j in range(len(p_j_list[0])):
        tmp = -1e16 # use only the first index at this point
        p_list = p_j_list[:,j,:]
        q_list = k*q_j_list[:,j,:] + d
#         print(d.shape)
#         print(q_list.shape)
        for tau in range(len(p_list)):
            c = _covariance(p_list, q_list, tau)
            c = calc_norm(c)
            if c > tmp:
                tmp = c
            # if c[0] > tmp:
            #     tmp = c[0]
#         print(tmp)
        if j in list(coeff_dict.keys()):
            res += coeff_dict[j]*tmp
        else:
            res += 1.0*tmp
            
    return 1.0*res/len(p_j_list[0])    

def correlation(p_j_list, q_j_list):
    p_j_list, q_j_list = local_align(p_j_list, q_j_list)
    return covariance(p_j_list, q_j_list)/(math.sqrt(covariance(p_j_list,p_j_list))*math.sqrt(covariance(q_j_list,q_j_list)))


#correlation(p_j_list, q_j_list)





