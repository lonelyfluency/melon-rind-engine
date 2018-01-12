#coding=utf8
import pickle
import math

def get_history(usr):
    infile = open('good_message.pkl', 'rb')
    message = pickle.load(infile)
    infile.close()
    return message[usr][0]

def recommend3(usr):
    return get_history(usr)


def get_job(usr):
    infile = open('customer_message.pkl', 'rb')
    message = pickle.load(infile)
    infile.close()
    return message[usr][-1]

def get_hobby(usr):
    infile = open('customer_message.pkl', 'rb')
    message = pickle.load(infile)
    infile.close()
    return message[usr][-2]

def recommend2(usr):
    return get_hobby(usr), get_job(usr)


def get_vector_book(usr):
    infile = open('customer_message.pkl', 'rb')
    message = pickle.load(infile)
    infile.close()
    '''
    for i in message:
        print i
        for j in message[i]:
            print j
    '''
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
        if i == 0:
            dis += ((v1[i] - v2[i])*6) ** 2
        else:
            dis += ((v1[i]-v2[i])*0.8)**2
    return math.sqrt(dis)


def find_a_nearest(usr):
    v_book = get_vector_book(usr)
    infile = open('customer_message.pkl', 'rb')
    message = pickle.load(infile)
    infile.close()
    v = []
    #print message[usr][1]
    v.append(0 if message[usr][1].encode('utf8') == '男' else 1)
    h,l = message[usr][2].split('-')

    s = (int(h)+int(l))*1.0/2
    v.append(s)
    #print v
    l = []
    for i in range(len(v_book)):
        l.append(get_dis(v,v_book[i]))
    m = min(l)
    usr_list = []
    for i in message:
        if i != usr:
            usr_list.append(i)
    return usr_list[l.index(m)]

def recommend1(usr):
    return get_history(find_a_nearest(usr))

