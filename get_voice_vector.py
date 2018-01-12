# -*- coding:utf-8 -*-
import wave
import numpy
import math

def get_voice_signal(file):
    wav_in = wave.open(file, 'r')
    voice_list = []
    for i in wav_in.readframes(wav_in.getnframes()):
        voice_list.append(i)
    return voice_list

def audio2frame(signal,frame_length,frame_step,winfunc=lambda x:numpy.ones((x,))):
    '''
    将音频信号转化为帧。
	参数含义：
	signal:原始音频型号
	frame_length:每一帧的长度(这里指采样点的长度，即采样频率乘以时间间隔)
	frame_step:相邻帧的间隔（同上定义）
	winfunc:lambda函数，用于生成一个向量
    '''
    signal_length=len(signal) #信号总长度
    frame_length=int(round(frame_length)) #以帧帧时间长度
    frame_step=int(round(frame_step)) #相邻帧之间的步长
    if signal_length<=frame_length: #若信号长度小于一个帧的长度，则帧数定义为1
        frames_num=1
    else: #否则，计算帧的总长度
        frames_num=1+int(math.ceil((1.0*signal_length-frame_length)/frame_step))
    pad_length=int((frames_num-1)*frame_step+frame_length) #所有帧加起来总的铺平后的长度
    zeros=numpy.zeros((pad_length-signal_length,)) #不够的长度使用0填补，类似于FFT中的扩充数组操作
    pad_signal=numpy.concatenate((signal,zeros)) #填补后的信号记为pad_signal
    indices=numpy.tile(numpy.arange(0,frame_length),(frames_num,1))+numpy.tile(numpy.arange(0,frames_num*frame_step,frame_step),(frame_length,1)).T  #相当于对所有帧的时间点进行抽取，得到frames_num*frame_length长度的矩阵
    indices=numpy.array(indices,dtype=numpy.int32) #将indices转化为矩阵
    frames=pad_signal[indices] #得到帧信号
    win=numpy.tile(winfunc(frame_length),(frames_num,1))  #window窗函数，这里默认取1
    return frames*win   #返回帧信号矩阵


print(len(get_voice_signal('1s/s1.wav')))
print(audio2frame(get_voice_signal('1s/s1.wav'),10,10))