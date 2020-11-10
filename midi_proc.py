from EasyMIDI import EasyMIDI, Track, Note, Chord, RomanChord
from random import choice
import time
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import string
import math
import random
from gensim.models import Word2Vec  # word to vec
from random import randint

#text_content = ([0, 0, 1, 0, 0, 0], '朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不住，轻舟已过万重山。')
# input->1*list(eg.)[1,0,0,0,0,0] && text_content


def proc_midi(input_arr,input_txt,input_id):
    text_content=(input_arr,input_txt)
    dataX = text_content[1]

    # 主旋律
    wordModel = Word2Vec(dataX, min_count=1)

    def clean(text):
        tex = [i.strip('\n').strip('\r').strip('。').strip(
            '，|！|？|、|）|：|{|}|“|”|【】|.|（|') for i in text]
        return list(filter(None, tex))

    def poetry(poem):
        d = clean(poem)
        words = np.array([[wordModel.wv[word].tolist() for word in d]])
        return words

    a = poetry(dataX)
    print(a)

    # 绝对值+平均
    l = []
    for i in range(len(a[0])):
        d = a[0][i]
        sum = 0
        count = 0
        for j in range(len(d)):
            d[j] = abs(d[j])
            sum += d[j]
            count += 1
        avg = sum / count
        l.append(avg)

    # 取数
    for i in range(len(l)):
        l[i] *= 10 ** 4
        l[i] -= 20

    # 取整
    for i in range(len(l)):
        l[i] = round(l[i])

    # 缩短间距
    for i in range(len(l) - 1):
        if abs(l[i] - l[i + 1]) >= 3:
            if l[i] < l[i + 1]:
                l[i + 1] = l[i] + 2
            elif l[i] > l[i + 1]:
                l[i + 1] = l[i] - 2

    # 去重复
    l1 = [1, 2, 3, 5, 6, 8, 9]
    for i in range(len(l) - 2):
        if l[i] == l[i + 1] and l[i + 1] == l[i + 2]:
            a = choice(l1)
            l[i + 2] = a

    # 收尾音
    if l[-1] != 1:
        l[-1] = 1
    index = int(len(l) / 2 - 1)
    if l[index] != 5:
        l[index] = 5

    # 避开4和7
    for i in range(len(l)):
        if l[i] == 7:
            if l[i] >= 7:
                l[i] = 8
            else:
                l[i] = 6
        elif l[i] == 4:
            if l[i] >= 4:
                l[i] = 5
            else:
                l[i] = 3

    print(l)

    easyMIDI = EasyMIDI(numTracks=3)

    # track1
    track1 = Track("Flute")

    # 定义1,2,3,5,6,8,9
    c = Note('C', octave=5, duration=1 / 4, volume=100)
    c_high_5long = Note('C', octave=6, duration=3 / 4, volume=100)
    c_high = Note('C', octave=6, duration=1 / 4, volume=100)
    c_5long = Note('C', octave=5, duration=3 / 4, volume=100)
    c_7long = Note('C', octave=5, duration=1 / 2, volume=100)
    c_high_7long = Note('C', octave=6, duration=1 / 2, volume=100)

    d = Note('D', 5)
    d_high = Note('D', octave=6)
    d_5long = Note('D', 5, duration=3 / 4)
    d_high_5long = Note('D', octave=6, duration=3 / 4, volume=100)
    d_7long = Note('D', octave=5, duration=1 / 2, volume=100)
    d_high_7long = Note('D', octave=6, duration=1 / 2, volume=100)

    e = Note('E', 5)
    e_5long = Note('E', 5, duration=3 / 4)
    e_7long = Note('E', octave=5, duration=1 / 2, volume=100)

    g = Note('G', 5, )
    g_5long = Note('G', 5, duration=3 / 4)
    g_7long = Note('G', octave=5, duration=1 / 2, volume=100)

    a = Note('A', 5)
    a_5long = Note('A', 5, duration=3 / 4)
    a_7long = Note('A', octave=5, duration=1 / 2, volume=100)

    r = Note('R', duration=1 / 8)

    length = 0
    for i in range(len(l)):
        if len(l) == 20:
            length = 4
            if i == 4 or i == 9 or i == 14 or i == 19:
                if l[i] == 1:
                    track1.addNotes([c_5long, r, r])
                elif l[i] == 2:
                    track1.addNotes([d_5long, r, r])
                elif l[i] == 3:
                    track1.addNotes([e_5long, r, r])
                elif l[i] == 5:
                    track1.addNotes([g_5long, r, r])
                elif l[i] == 6:
                    track1.addNotes([a_5long, r, r])
                elif l[i] == 8:
                    track1.addNotes([c_high_5long, r, r])
                else:
                    track1.addNotes([d_high_5long, r, r])
            else:
                if l[i] == 1:
                    track1.addNotes([c])
                elif l[i] == 2:
                    track1.addNotes([d])
                elif l[i] == 3:
                    track1.addNotes([e])
                elif l[i] == 5:
                    track1.addNotes([g])
                elif l[i] == 6:
                    track1.addNotes([a])
                elif l[i] == 8:
                    track1.addNotes([c_high])
                else:
                    track1.addNotes([d_high])

        elif len(l) == 28:
            length = 4
            if i == 6 or i == 13 or i == 20 or i == 27:
                if l[i] == 1:
                    track1.addNotes([c_7long])
                elif l[i] == 2:
                    track1.addNotes([d_7long])
                elif l[i] == 3:
                    track1.addNotes([e_7long])
                elif l[i] == 5:
                    track1.addNotes([g_7long])
                elif l[i] == 6:
                    track1.addNotes([a_7long])
                elif l[i] == 8:
                    track1.addNotes([c_high_7long])
                else:
                    track1.addNotes([d_high_7long])
            else:
                if l[i] == 1:
                    track1.addNotes([c])
                elif l[i] == 2:
                    track1.addNotes([d])
                elif l[i] == 3:
                    track1.addNotes([e])
                elif l[i] == 5:
                    track1.addNotes([g])
                elif l[i] == 6:
                    track1.addNotes([a])
                elif l[i] == 8:
                    track1.addNotes([c_high])
                else:
                    track1.addNotes([d_high])

        elif len(l) == 40:
            length = 8
            if i == 4 or i == 9 or i == 14 or i == 19 or i == 24 or i == 29 or i == 34 or i == 39:
                if l[i] == 1:
                    track1.addNotes([c_5long, r, r])
                elif l[i] == 2:
                    track1.addNotes([d_5long, r, r])
                elif l[i] == 3:
                    track1.addNotes([e_5long, r, r])
                elif l[i] == 5:
                    track1.addNotes([g_5long, r, r])
                elif l[i] == 6:
                    track1.addNotes([a_5long, r, r])
                elif l[i] == 8:
                    track1.addNotes([c_high_5long, r, r])
                else:
                    track1.addNotes([d_high_5long, r, r])
            else:
                if l[i] == 1:
                    track1.addNotes([c])
                elif l[i] == 2:
                    track1.addNotes([d])
                elif l[i] == 3:
                    track1.addNotes([e])
                elif l[i] == 5:
                    track1.addNotes([g])
                elif l[i] == 6:
                    track1.addNotes([a])
                elif l[i] == 8:
                    track1.addNotes([c_high])
                else:
                    track1.addNotes([d_high])

        elif len(l) == 56:
            length = 8
            if i == 6 or i == 13 or i == 20 or i == 27 or i == 34 or i == 41 or i == 48 or i == 55:
                if l[i] == 1:
                    track1.addNotes([c_7long])
                elif l[i] == 2:
                    track1.addNotes([d_7long])
                elif l[i] == 3:
                    track1.addNotes([e_7long])
                elif l[i] == 5:
                    track1.addNotes([g_7long])
                elif l[i] == 6:
                    track1.addNotes([a_7long])
                elif l[i] == 8:
                    track1.addNotes([c_high_7long])
                else:
                    track1.addNotes([d_high_7long])
            else:
                if l[i] == 1:
                    track1.addNotes([c])
                elif l[i] == 2:
                    track1.addNotes([d])
                elif l[i] == 3:
                    track1.addNotes([e])
                elif l[i] == 5:
                    track1.addNotes([g])
                elif l[i] == 6:
                    track1.addNotes([a])
                elif l[i] == 8:
                    track1.addNotes([c_high])
                else:
                    track1.addNotes([d_high])

    easyMIDI.addTrack(track1)

    # Functions for track 2
    def epic(length):
        a = randint(1, 2)
        track2 = Track("Synth Strings 1")  # oops
        # epic1,2
        if a == 1:
            if length == 8:
                # c-1; d-2; e-3; g-5; a-6
                c1 = Chord([Note('C', octave=3, duration=1 / 4,
                                 volume=80), Note('E', 4), Note('G', 4)])
                c2 = Chord([Note('G', octave=3, duration=1 / 4,
                                 volume=80), Note('B', 3), Note('D', 4)])
                c3 = Chord([Note('A', octave=3, duration=1 / 4,
                                 volume=80), Note('C', 4), Note('E', 4)])
                c4 = Chord([Note('F', octave=3, duration=1 / 4,
                                 volume=80), Note('A', 3), Note('C', 4)])
                r = Note('R', duration=1 / 8)
                track2.addNotes([c1, r, c1, r, c1])
                track2.addNotes([c2, r, c2, r, c2])
                track2.addNotes([c3, r, c3, r, c3])
                track2.addNotes([c4, r, c4, r, c4])
                track2.addNotes([c1, r, c1, r, c1])
                track2.addNotes([c2, r, c2, r, c2])
                track2.addNotes([c3, r, c3, r, c3])
                track2.addNotes([c4, r, c4, r, c4])
            # Epic1-2
            c1 = Chord([Note('C', octave=4, duration=1 / 4, volume=80),
                        Note('E', 4), Note('G', 4)])
            c2 = Chord([Note('G', octave=3, duration=1 / 4, volume=80),
                        Note('B', 3), Note('D', 4)])
            c3 = Chord([Note('A', octave=3, duration=1 / 4, volume=80),
                        Note('C', 4), Note('E', 4)])
            c4 = Chord([Note('F', octave=3, duration=1 / 4, volume=80),
                        Note('A', 3), Note('C', 4)])
            r = Note('R', duration=1 / 8)
            track2.addNotes([c1, r, c1, r, c1])
            track2.addNotes([c2, r, c2, r, c2])
            track2.addNotes([c3, r, c3, r, c3])
            track2.addNotes([c4, r, c4, r, c4])
            track2.addNotes([c1, r, c1, r, c1])
            track2.addNotes([c2, r, c2, r, c2])
            track2.addNotes([c3, r, c3, r, c3])
            track2.addNotes([c4, r, c4, r, c4])
        else:  # epic 2
            c3 = Chord([Note('C', octave=4, duration=1, volume=80),
                        Note('E', 4), Note('G', 3)])
            c4 = Chord([Note('G', octave=3, duration=1 / 2, volume=80),
                        Note('B', 3), Note('E', 4)])
            c5 = Chord([Note('G', octave=3, duration=1 / 2, volume=80),
                        Note('B', 3), Note('D', 4)])
            c1 = Chord([Note('A', octave=3, duration=1, volume=80),
                        Note('C', 4), Note('E', 4)])
            c2 = Chord([Note('F', octave=3, duration=1, volume=80),
                        Note('A', 3), Note('C', 4)])
            if length == 8:
                track2.addNotes([c1, c2, c3, c4, c5])
                track2.addNotes([c1, c2, c3, c4, c5])
            track2.addNotes([c1, c2, c3, c4, c5])
            track2.addNotes([c1, c2, c3, c4, c5])
        return (track2, None)

    def emot(length):
        a = randint(1, 2)
        track2 = Track("Acoustic Guitar (nylon)")  # oops
        # rouqing 1 (4ju)
        if a == 1:
            c1 = Chord([Note('F', octave=3, duration=1 / 2, volume=80),
                        Note('A', 3), Note('C', 4)])
            c2 = Chord([Note('G', octave=3, duration=1 / 2, volume=80),
                        Note('B', 3), Note('D', 4)])
            c3 = Chord([Note('E', octave=3, duration=1 / 2, volume=80),
                        Note('G', 3), Note('B', 3)])
            c4 = Chord([Note('A', octave=3, duration=1 / 2, volume=80),
                        Note('C', 4), Note('E', 4)])
            c5 = Chord([Note('G', octave=3, duration=1 / 2, volume=80),
                        Note('B', 3), Note('D', 4)])
            c7 = Chord([Note('D', octave=3, duration=1 / 2, volume=80),
                        Note('F', 3), Note('A', 3)])
            c6 = Chord([Note('C', octave=4, duration=1 / 2, volume=80),
                        Note('E', 4), Note('G', 4)])
            r = Note('R', duration=1 / 8)
            if length == 8:
                track2.addNotes([c1, c1])
                track2.addNotes([c2, c2])
                track2.addNotes([c3, c3])
                track2.addNotes([c4, c4])
                track2.addNotes([c7, c7])
                track2.addNotes([c5, c5])
                track2.addNotes([c6, c6, c6, c6])
            track2.addNotes([c1, c1])
            track2.addNotes([c2, c2])
            track2.addNotes([c3, c3])
            track2.addNotes([c4, c4])
            track2.addNotes([c7, c7])
            track2.addNotes([c5, c5])
            track2.addNotes([c6, c6, c6, c6])
        else:  # rouqing2
            c1 = Chord([Note('C', octave=4, duration=1, volume=80),
                        Note('E', 4), Note('G', 4)])
            c2 = Chord([Note('B', octave=3, duration=1, volume=80),
                        Note('E', 4), Note('G', 4)])
            c3 = Chord([Note('A', octave=3, duration=1, volume=80),
                        Note('C', 4), Note('E', 4)])
            c4 = Chord([Note('G', octave=3, duration=1, volume=80),
                        Note('B', 3), Note('E', 4)])
            c5 = Chord([Note('F', octave=3, duration=1, volume=80),
                        Note('A', 3), Note('C', 4)])
            c6 = Chord([Note('C', octave=3, duration=1, volume=80),
                        Note('E', 3), Note('G', 3)])
            c7 = Chord([Note('F', octave=3, duration=1, volume=80),
                        Note('A', 3), Note('C', 4)])
            c8 = Chord([Note('G', octave=3, duration=1, volume=80),
                        Note('B', 3), Note('D', 4)])
            if length == 8:
                track2.addNotes([c1, c2, c3, c4, c5, c6, c7, c8])
            track2.addNotes([c1, c2, c3, c4, c5, c6, c7, c8])
        return (track2, None)

    def sad(length):
        a = randint(1, 2)
        track2 = Track("acoustic grand piano")  # oops
        track3 = Track("Synth Strings 1")
        # sad 1
        if a == 1:
            c1 = Chord([Note('C', octave=4, duration=1, volume=80),
                        Note('E', 4), Note('A', 3)])
            c2 = Chord([Note('G', octave=3, duration=1, volume=80),
                        Note('B', 3), Note('E', 4)])
            c3 = Chord([Note('F', octave=3, duration=1, volume=80),
                        Note('A', 3), Note('E', 4)])
            c4 = Chord([Note('E', octave=3, duration=1, volume=80),
                        Note('G', 3), Note('D', 4)])
            if length == 8:
                track2.addNotes([c1, c2, c3, c4])
                track3.addNotes(
                    [
                        Note(
                            'E', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80), Note(
                            'C', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80)])
                track2.addNotes([c1, c2, c3, c4])
                track3.addNotes(
                    [
                        Note(
                            'E', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80), Note(
                            'C', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80)])
            track2.addNotes([c1, c2, c3, c4])
            track2.addNotes([c1, c2, c3, c4])
            track3.addNotes(
                [
                    Note(
                        'E', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80), Note(
                        'C', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80)])
            track3.addNotes(
                [
                    Note(
                        'E', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80), Note(
                        'C', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80)])
        else:  # sad 2
            c1 = Chord([Note('C', octave=4, duration=1, volume=80),
                        Note('E', 4), Note('A', 3)])
            c2 = Chord([Note('G', octave=3, duration=1, volume=80),
                        Note('B', 3), Note('E', 4)])
            c3 = Chord([Note('F', octave=3, duration=1, volume=80),
                        Note('A', 3), Note('E', 4)])
            c4 = Chord([Note('E', octave=3, duration=1, volume=80),
                        Note('G', 3), Note('D', 4)])
            c5 = Chord([Note('G', octave=3, duration=1, volume=80),
                        Note('B', 3), Note('D', 4)])
            c6 = Chord([Note('E', octave=3, duration=1, volume=80),
                        Note('G', 3), Note('C', 4)])
            if length == 8:
                track2.addNotes([c1, c2, c3, c4])
                track3.addNotes(
                    [
                        Note(
                            'E', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80), Note(
                            'C', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80)])
                track2.addNotes([c1, c2, c3, c4])
                track3.addNotes(
                    [
                        Note(
                            'E', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80), Note(
                            'C', octave=4, duration=1, volume=80), Note(
                            'D', octave=4, duration=1, volume=80)])
            track2.addNotes([c1, c2, c3, c4])
            track2.addNotes([c1, c2, c5, c6])
            track3.addNotes(
                [
                    Note(
                        'E', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80), Note(
                        'C', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80)])
            track3.addNotes(
                [
                    Note(
                        'E', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80), Note(
                        'D', octave=4, duration=1, volume=80), Note(
                        'C', octave=4, duration=1, volume=80)])
        return (track2, track3)

    def qingsong(length):
        a = randint(1, 2)
        track2 = Track("marimba")  # oops
        # Qingsong 1 (4ju)
        if a == 1:
            if length == 8:
                f1 = Chord([Note('F', octave=3, duration=1 / 8, volume=80),
                            Note('A', 3, duration=1 / 8), Note('C', 4, duration=1 / 8)])
                f2 = Chord([Note('F', octave=3, duration=1 / 4, volume=80),
                            Note('A', 3, duration=1 / 4), Note('C', 4, duration=1 / 4)])
                c1 = Chord([Note('G', octave=3, duration=1 / 4, volume=80),
                            Note('C', 4, duration=1 / 4), Note('E', 4, duration=1 / 4)])
                g1 = Chord([Note('G', octave=3, duration=1 / 8, volume=80),
                            Note('B', 3, duration=1 / 8), Note('D', 4, duration=1 / 8)])
                g2 = Chord([Note('G', octave=3, duration=1 / 4, volume=80),
                            Note('B', 3, duration=1 / 4), Note('D', 4, duration=1 / 4)])
                r = Note('R', duration=1 / 8)
                track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                             8, volume=80), Note('C', 4, duration=1 /
                                                                 8), Note('E', 4, duration=1 /
                                                                          8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                            16, volume=80), Note('C', 4, duration=1 /
                                                                                                                 16), Note('E', 4, duration=1 /
                                                                                                                           16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                              16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                   16), Note('E', 4, duration=1 /
                                                                                                                                                                             16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                    8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                             8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                               8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                                   8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                            8)]), r, f1, f2, c1, c1, r, g1, g2])
                track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                             8, volume=80), Note('C', 4, duration=1 /
                                                                 8), Note('E', 4, duration=1 /
                                                                          8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                            16, volume=80), Note('C', 4, duration=1 /
                                                                                                                 16), Note('E', 4, duration=1 /
                                                                                                                           16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                              16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                   16), Note('E', 4, duration=1 /
                                                                                                                                                                             16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                    8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                             8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                               8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                                   8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                            8)]), r, f1, f2, c1, c1, r, g1, g2])
                track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                             8, volume=80), Note('C', 4, duration=1 /
                                                                 8), Note('E', 4, duration=1 /
                                                                          8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                            16, volume=80), Note('C', 4, duration=1 /
                                                                                                                 16), Note('E', 4, duration=1 /
                                                                                                                           16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                              16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                   16), Note('E', 4, duration=1 /
                                                                                                                                                                             16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                    8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                             8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                               8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                                   8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                            8)]), r, f1, f2, c1, c1, r, g1, g2])
                track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                             8, volume=80), Note('C', 4, duration=1 /
                                                                 8), Note('E', 4, duration=1 /
                                                                          8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                            16, volume=80), Note('C', 4, duration=1 /
                                                                                                                 16), Note('E', 4, duration=1 /
                                                                                                                           16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                              16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                   16), Note('E', 4, duration=1 /
                                                                                                                                                                             16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                    8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                             8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                               8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                                   8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                            8)]), r, f1, f2, c1, c1, r, g1, Chord([Note('G', octave=3, duration=1 /
                                                                                                                                                                                                                                                                                                                        4, volume=80), Note('E', 3, duration=1 /
                                                                                                                                                                                                                                                                                                                                            4), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                                                                                                                     4)])])
            f1 = Chord([Note('F', octave=3, duration=1 / 8, volume=80),
                        Note('A', 3, duration=1 / 8), Note('C', 4, duration=1 / 8)])
            f2 = Chord([Note('F', octave=3, duration=1 / 4, volume=80),
                        Note('A', 3, duration=1 / 4), Note('C', 4, duration=1 / 4)])
            c1 = Chord([Note('G', octave=3, duration=1 / 4, volume=80),
                        Note('C', 4, duration=1 / 4), Note('E', 4, duration=1 / 4)])
            g1 = Chord([Note('G', octave=3, duration=1 / 8, volume=80),
                        Note('B', 3, duration=1 / 8), Note('D', 4, duration=1 / 8)])
            g2 = Chord([Note('G', octave=3, duration=1 / 4, volume=80),
                        Note('B', 3, duration=1 / 4), Note('D', 4, duration=1 / 4)])
            r = Note('R', duration=1 / 8)
            track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                         8, volume=80), Note('C', 4, duration=1 /
                                                             8), Note('E', 4, duration=1 /
                                                                      8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                        16, volume=80), Note('C', 4, duration=1 /
                                                                                                             16), Note('E', 4, duration=1 /
                                                                                                                       16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                          16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                               16), Note('E', 4, duration=1 /
                                                                                                                                                                         16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                            8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                         8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                           8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                               8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                        8)]), r, f1, f2, c1, c1, r, g1, g2])
            track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                         8, volume=80), Note('C', 4, duration=1 /
                                                             8), Note('E', 4, duration=1 /
                                                                      8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                        16, volume=80), Note('C', 4, duration=1 /
                                                                                                             16), Note('E', 4, duration=1 /
                                                                                                                       16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                          16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                               16), Note('E', 4, duration=1 /
                                                                                                                                                                         16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                            8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                         8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                           8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                               8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                        8)]), r, f1, f2, c1, c1, r, g1, g2])
            track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                         8, volume=80), Note('C', 4, duration=1 /
                                                             8), Note('E', 4, duration=1 /
                                                                      8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                        16, volume=80), Note('C', 4, duration=1 /
                                                                                                             16), Note('E', 4, duration=1 /
                                                                                                                       16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                          16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                               16), Note('E', 4, duration=1 /
                                                                                                                                                                         16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                            8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                         8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                           8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                               8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                        8)]), r, f1, f2, c1, c1, r, g1, g2])
            track2.addNotes([Chord([Note('A', octave=3, duration=1 /
                                         8, volume=80), Note('C', 4, duration=1 /
                                                             8), Note('E', 4, duration=1 /
                                                                      8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                        16, volume=80), Note('C', 4, duration=1 /
                                                                                                             16), Note('E', 4, duration=1 /
                                                                                                                       16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                          16, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                               16), Note('E', 4, duration=1 /
                                                                                                                                                                         16)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                            8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                         8)]), Chord([Note('A', octave=3, duration=1 /
                                                                                                                                                                                                                                           8, volume=80), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                               8), Note('E', 4, duration=1 /
                                                                                                                                                                                                                                                                        8)]), r, f1, f2, c1, c1, r, g1, Chord([Note('G', octave=3, duration=1 /
                                                                                                                                                                                                                                                                                                                    4, volume=80), Note('E', 3, duration=1 /
                                                                                                                                                                                                                                                                                                                                        4), Note('C', 4, duration=1 /
                                                                                                                                                                                                                                                                                                                                                 4)])])
        else:  # Qingsong 2
            c1 = Chord([Note('C', octave=4, duration=1 / 4, volume=80),
                        Note('E', 4), Note('G', 4)])
            f1 = Chord([Note('C', octave=4, duration=1 / 4, volume=80),
                        Note('F', 4), Note('A', 4)])
            g1 = Chord([Note('B', octave=3, duration=1 / 4, volume=80),
                        Note('D', 4), Note('G', 4)])
            r = Note('R', duration=1 / 8)
            if length == 8:
                track2.addNotes([c1, r, c1, r, c1])
                track2.addNotes([f1, r, f1, r, f1])
                track2.addNotes([c1, r, c1, r, c1])
                track2.addNotes([g1, r, g1, r, g1])
            track2.addNotes([c1, r, c1, r, c1])
            track2.addNotes([f1, r, f1, r, f1])
            track2.addNotes([c1, r, c1, r, c1])
            track2.addNotes([g1, r, g1, r, g1])
        return (track2, None)

    def philo(length):
        a = randint(1, 2)
        track2 = Track("Acoustic Grand Piano")  # oops
        # Philo1
        if a == 1:
            if length == 8:
                track2.addNotes([Note('C', 2, 1, 80), Note('F#', 2, 1 /
                                                           8, 80), Note('G', 2, 7 /
                                                                        8, 80), Note('E', 2, 1, 80),
                                 Note('D', 2, 1, 80)])
                track2.addNotes([Note('C', 2, 1, 80), Note('F#', 2, 1 /
                                                           8, 80), Note('G', 2, 7 /
                                                                        8, 80), Note('E', 2, 1, 80),
                                 Note('D', 2, 1, 80)])
            track2.addNotes([Note('C', 2, 1, 80), Note('F#', 2, 1 /
                                                       8, 80), Note('G', 2, 7 /
                                                                    8, 80), Note('E', 2, 1, 80), Note('D', 2, 1, 80)])
            track2.addNotes([Note('C', 2, 1, 80), Note('F#', 2, 1 /
                                                       8, 80), Note('G', 2, 7 /
                                                                    8, 80), Note('E', 2, 1, 80), Note('C', 2, 1, 80)])
        else:  # philo2
            if length == 8:
                track2.addNotes(
                    [Chord([Note('C', 3, 1, 80), Note('F', 2, 1, 80)]),
                     Chord([Note('D', 3, 1, 80), Note('G', 2, 1, 80)]),
                     Chord([Note('E', 3, 1, 80), Note('A', 2, 1, 80)]),
                     Chord([Note('D', 3, 1, 80), Note('G', 2, 1, 80)])])
                track2.addNotes(
                    [Chord([Note('C', 3, 1, 80), Note('F', 2, 1, 80)]),
                     Chord([Note('D', 3, 1, 80), Note('G', 2, 1, 80)]),
                     Chord([Note('E', 3, 1, 80), Note('A', 2, 1, 80)]),
                     Chord([Note('D', 3, 1, 80), Note('G', 2, 1, 80)])])
            track2.addNotes(
                [Chord([Note('C', 3, 1, 80), Note('F', 2, 1, 80)]), Chord([Note('D', 3, 1, 80), Note('G', 2, 1, 80)]),
                 Chord([Note('E', 3, 1, 80), Note('A', 2, 1, 80)]), Chord([Note('D', 3, 1, 80), Note('G', 2, 1, 80)])])
            track2.addNotes(
                [Chord([Note('C', 3, 1, 80), Note('F', 2, 1, 80)]), Chord([Note('D', 3, 1, 80), Note('G', 2, 1, 80)]),
                 Chord([Note('C', 3, 1, 80), Note('F', 2, 1, 80)]), Chord([Note('C', 3, 1, 80), Note('E', 2, 1, 80)])])
        return (track2, None)

    def neut(length):
        a = randint(1, 5)
        track2 = Track('acoustic grand piano')
        track3 = None
        if a == 1:
            track2 = epic(length)[0]
        if a == 2:
            track2 = emot(length)[0]
        if a == 3:
            track2, track3 = sad(length)
        if a == 4:
            track2 = qingsong(length)[0]
        if a == 5:
            track2 = philo(length)[0]
        return (track2, track3)

    # track2
    labels = text_content[0]
    label = ''
    label_list = ['emotional', 'epic', 'neutral', 'philo', 'relax', 'sad']

    for i in range(len(labels)):
        if labels[i] == 1:
            label = label_list[i]
            if i == 2:
                break

    track2, track3 = None, None
    if label == 'epic':
        track2, track3 = epic(length)
    elif label == 'emotional':
        track2, track3 = emot(length)
    elif label == 'sad':
        track2, track3 = sad(length)
    elif label == 'relax':
        track2, track3 = qingsong(length)
    elif label == 'philo':
        track2, track3 = philo(length)
    else:
        track2, track3 = neut(length)
    # part seudocode, need to rewrite
    if track2 is not None:
        easyMIDI.addTrack(track2)
    if track3 is not None:
        easyMIDI.addTrack(track3)

    filename = time.time()
    easyMIDI.writeMIDI("./static/midi/{}.mid".format(filename))
    return "./static/midi/{}.mid".format(filename)
