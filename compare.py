
import vq_book
import scipy.io.wavfile as wav
from python_speech_features import mfcc
import math
import os

def voice_recognize(test_voice):
    voice_list = get_voice_list()
    rate = [i for i in range(len(voice_list))]
    sig = [i for i in range(len(voice_list))]
    for i in range(len(voice_list)):
        (rate[i],sig[i]) = wav.read('./voice_database/' + voice_list[i])

    mfcc_feat = [i for i in range(len(voice_list))]
    for i in range(len(voice_list)):
        mfcc_feat[i] = mfcc(sig[i],rate[i])


    dataset = [i for i in range(len(voice_list))]
    for i in range(len(voice_list)):
        dataset[i] = mfcc_feat[i]
    vq_lg = [i for i in range(len(voice_list))]
    book = [i for i in range(len(voice_list))]
    for i in range(len(voice_list)):
        vq_lg[i] = vq_book.VQ_LGB(dataset[i],64,0.00005,3000)
        vq_lg[i].run()
        book[i] = vq_lg[i].get_codebook()

    test_wave = test_voice + '.wav'

    (test_rate,test_sig) = wav.read(test_wave)
    test_mfcc_feat = mfcc(test_sig,test_rate)
    test_dataset = test_mfcc_feat
    test_vq_lg = vq_book.VQ_LGB(test_dataset,64,0.00005,3000)
    test_vq_lg.run()
    test_book = test_vq_lg.get_codebook()


    def match(book, test_book,voice_list):
        distance = []
        dist = 0
        for k in range(len(book)):
            cnt = 0
            for i in range(len(test_book)):
                for j in range(len(test_book[0])):
                    cnt += 1
                    dist += (test_book[i][j]-book[k][i][j])**2
            dist = math.sqrt(dist)/cnt
            distance.append(dist)
        #print distance
        m = max(distance)
        print distance
        print voice_list
        print voice_list[distance.index(m)][:-4]
        return voice_list[distance.index(m)][:-4]

    return match(book,test_book,voice_list)


def get_voice_list():
    l = []
    for root, dirnames, filenames in os.walk('voice_database'):
        l += filenames
    return l

