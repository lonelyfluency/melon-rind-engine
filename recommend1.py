#coding=utf8
import pickle
import math

def get_vector_book(usr):
    infile = open('customer_message.pkl', 'rb')
    message = pickle.load(infile)
    infile.close()
    v = []
    for i in message:
        if i != usr:
            temp = []
            for k,j in enumerate(message[i]):
                if k == 1:
                    if j.encode('utf8') == '男':
                        temp.append(0)
                    else:
                        temp.append(1)
                if k == 2:
                    h,l = j.split('-')
                    s = (int(h)+int(l)) * 1.0 / 2
                    temp.append(s)
            v.append(temp)
    return v


def get_dis(v1, v2):
    dis = 0
    for i in range(len(v1)):
        dis += (v1[i] - v2[i]) ** 2
    return math.sqrt(dis)


def find_a_nearest(usr):
    v_book = get_vector_book(usr)
    infile = open('customer_message.pkl', 'rb')
    message = pickle.load(infile)
    infile.close()
    v = []
    print message[usr][1]
    v.append(0 if message[usr][1].encode('utf8') == '男' else 1)
    h,l = message[usr][2].split('-')
    s = (int(h)+int(l))*1.0/2
    v.append(s)

    l = []
    for i in range(len(v_book)):
        l.append(get_dis(v,v_book[i]))
    print l

find_a_nearest('sry')