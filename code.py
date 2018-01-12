# -*- coding: utf-8 -*-
import web
from web import form
import urllib2
#import cchardet
import os
import sys
import pickle
from SearchFiles import *
global user_name
from compare import *
from recommend import *
user_name=None
urls = (
    '/', 'start',
    '/re','re',
    '/in', 'index',
    '/login_action', 'login',
    '/registe_action','registe',
    '/voice_action','voice',
    '/s', 'text',
)
render = web.template.render('templates') # your templates

def sort_by_weight(origion_list):
    #print origion_list
    tfidf_list = []
    tag_list = []
    price_list = []
    wellrate_list = []
    for i in range(len(origion_list)-1,0,-1):
        tfidf_list.append(i)
    for item in origion_list[1:]:
        #print item
        try:
            item[6]
            tag_list.append(1)
        except IndexError:
            tag_list.append(0)
        #print item[2]
        try:
            price_list.append(float(item[2]))
        except Exception:
            price_list.append(float(100.0))
        wellrate_list.append(float(item[4].strip().strip('%')))
    weighted_list = []
    tf_weight = 10
    tag_weight = 6000
    price_weight = -20.0 / max(price_list)
    wellrate_weight = 60
    for i in range(len(origion_list)-1):
        s = 0
        s += (tf_weight*tfidf_list[i])
        s += (tag_weight*tag_list[i])
        s += (price_weight*price_list[i])
        s += (wellrate_weight*(wellrate_list[i]-97.5))
        weighted_list.append(s)
    res_dic = {}
    for i in range(len(origion_list)-1):
        res_dic[weighted_list[i]] = origion_list.index(origion_list[i])
    res = []
    for i in sorted(res_dic.keys(),reverse=True):
        res.append(origion_list[res_dic[i]+1])
    res = [origion_list[0]] + res
    
    return res



def func_index(command):
    STORE_DIR = "index"
    vm_env.attachCurrentThread()
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)    
    return sort_by_weight(run(searcher, analyzer,command,'contents'))



        

def func_tags(command):
    STORE_DIR = "tags"
    vm_env.attachCurrentThread()
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)    
    return sort_by_weight(run(searcher, analyzer,command,'tags'))

class start:
    def GET(self):
        return render.login()
class re:
    def GET(self):
        return render.registe()
   
class login:   
    def GET(self):
        global user_name
        vm_env.attachCurrentThread()
        name=voice_recognize('key')
        judge=True
        user_name=name
        kword_1=recommend1(name)
        kword_2,kword_3=recommend2(name)
        kword_4=recommend3(name)
        ans_1=func_index(kword_1)
        ans_2=func_tags(kword_2)
        ans_3=func_tags(kword_3)
        ans_4=func_index(kword_4)
        ans=[]
        for i in range(1,4):
            ans.append(ans_4[i])
        for i in range(1,4):
            ans.append(ans_1[i])
            ans.append(ans_2[i])
            ans.append(ans_3[i])            
        return render.formtest(name,judge,ans)
    def POST(self):
        global user_name
        vm_env.attachCurrentThread()
        user_data = web.input()
        name= user_data.username
        password=user_data.userpassword
        read_file=open("customer_message.pkl",'rb')
        usermessage=pickle.load(read_file)
        read_file.close()
        judge=False
        if usermessage[name][0]==password:
            judge=True
            user_name=name
            kword_1=recommend1(name)
            kword_2,kword_3=recommend2(name)
            kword_4=recommend3(name)
            ans_1=func_index(kword_1)
            ans_2=func_tags(kword_2)
            ans_3=func_tags(kword_3)
            ans_4=func_index(kword_4)
            ans=[]
            for i in range(1,4):
                ans.append(ans_4[i])
               
            for i in range(1,4):
                ans.append(ans_3[i])
                ans.append(ans_1[i])
                ans.append(ans_2[i])                
                    
            return render.formtest(name,judge,ans)
        else:
            return render.login()
        
class registe:
    def GET(self):
        global user_name
        vm_env.attachCurrentThread()
        user_data = web.input()
        name= user_data.username
        user_name=name
        password=user_data.userpassword
        gender=user_data.gender
        age=user_data.age
        hobby=user_data.hobby
        job=user_data.hobby
        infile = open('/home/michael/Desktop/Browser/usrname.txt', 'w')
        infile.write(user_name)
        infile.close()
        read_file=open("customer_message.pkl",'rb')
        usermessage=pickle.load(read_file)
        read_file.close()
        usermessage[name]=[password,gender,age,hobby,job]
        write_file=open("customer_message.pkl",'wb')
        pickle.dump(usermessage,write_file)
        write_file.close()
        return render.voice(name)
class voice:
    def  GET(self):
        judge=True
        infile = open('/home/michael/Desktop/Browser/usrname.txt', 'r')
        name=infile.readline()
        kword_1=recommend1(name)
        kword_2,kword_3=recommend2(name)
        ans_1=func_index(kword_1)
        ans_2=func_tags(kword_2)
        ans_3=func_tags(kword_3)
        ans=[]
        for i in range(1,5):
            ans.append(ans_3[i])
        for i in range(1,5):
            ans.append(ans_1[i])
            ans.append(ans_2[i])
        return render.formtest(name,judge,ans)
class index:
    def GET(self):
        return render.formtest()
class text:
    def GET(self):
        name=user_name
        kword_1=recommend1(name)
        kword_2,kword_3=recommend2(name)
        ans_1=func_index(kword_1)
        ans_2=func_tags(kword_2)
        ans_3=func_tags(kword_3)
        ans=[]
        for i in range(1,5):
            ans.append(ans_1[i])
            ans.append(ans_2[i])
            ans.append(ans_3[i])
        user_data = web.input()
        if user_data.keyword:
            a = func_index(user_data.keyword)
            ans_4=func_tags(user_data.keyword)
            ans_4=ans_4[1:5]
            read_file=open("good_message.pkl",'rb')
            goodmessage=pickle.load(read_file)
            read_file.close()
            if user_name in goodmessage:
                goodmessage[user_name].append(user_data.keyword)
            else:
                goodmessage[user_name]=[user_data.keyword]
            write_file=open("good_message.pkl",'wb')
            pickle.dump(goodmessage,write_file)
            write_file.close()
        else:
            a=['']
            ans_4=['']
        return render.result(a,ans,ans_4)
    def POST(self):
        name=user_name
        kword_1=recommend1(name)
        kword_2,kword_3=recommend2(name)
        ans_1=func_index(kword_1)
        ans_2=func_tags(kword_2)
        ans_3=func_tags(kword_3)
        ans=[]
        for i in range(1,5):
            ans.append(ans_1[i])
            ans.append(ans_2[i])
            ans.append(ans_3[i])
        infile=open("graph_result.txt",'r')
        word=infile.readline().decode('utf-8')
        infile.close()
        read_file=open("good_message.pkl",'rb')
        goodmessage=pickle.load(read_file)
        read_file.close()        
        if user_name in goodmessage:
                goodmessage[user_name].append(word)
        else:
                goodmessage[user_name]=[word]
        write_file=open("good_message.pkl",'wb')
        pickle.dump(goodmessage,write_file)
        write_file.close()
        a = func_index(word)
        ans_4=func_tags(word)
        ans_4=ans_4[1:5]
        return render.result(a,ans,ans_4)
        
        


if __name__ == "__main__":
    vm_env=lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app = web.application(urls, globals())
    app.run()
    print user_name
