import numpy as np
import jieba
from datetime import datetime
import random
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
#将情绪词典添加到jieba自定义词典
def addto_my_jieba():
    jieba.load_userdict(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\anger.txt")
    jieba.load_userdict(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\disgust.txt")
    jieba.load_userdict(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\fear.txt")
    jieba.load_userdict(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\joy.txt")
    jieba.load_userdict(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\sadness.txt")

#闭包实现统计情绪词
#结果为5维向量时，第一维表示anger，第二维表示disgust，第三维表示fear，第四维表示joy，第五维表示sadness。
def emotion_analysis_outer(mode='vector'):
    emotions=[]
    with open(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\anger.txt",'r',encoding='utf8') as f1:
        emotions.append([i.strip('\n') for i in f1.readlines()])
    with open(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\disgust.txt",'r',encoding='utf8') as f1:
        emotions.append([i.strip('\n') for i in f1.readlines()])
    with open(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\fear.txt",'r',encoding='utf8') as f1:
        emotions.append([i.strip('\n') for i in f1.readlines()])
    with open(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\joy.txt",'r',encoding='utf8') as f1:
        emotions.append([i.strip('\n') for i in f1.readlines()])
    with open(r"C:\Users\86137\PycharmProjects\pythonProject\python数据分析\情绪分析（第二周）\emotion_lexicon\sadness.txt",'r',encoding='utf8') as f1:
        emotions.append([i.strip('\n') for i in f1.readlines()])
    #输出五维向量
    if mode=='vector':
        def emotion_analysis_inner(data):
            nonlocal emotions
            emotion_list = [0, 0, 0, 0, 0]
            data=jieba.lcut(data)
            for x in data:
                if x in emotions[0]:
                    emotion_list[0]+=1
                elif x in emotions[1]:
                    emotion_list[1]+=1
                elif x in emotions[2]:
                    emotion_list[2] += 1
                elif x in emotions[3]:
                    emotion_list[3] += 1
                elif x in emotions[4]:
                    emotion_list[4] += 1
            return np.array(emotion_list)/np.sum(np.array(emotion_list))
        return emotion_analysis_inner
    #输出心情值
    elif mode=='value':
        def emotion_analysis_inner(data):
            nonlocal emotions
            emotion_list = [0, 0, 0, 0, 0]
            data = jieba.lcut(data)
            for x in data:
                if x in emotions[0]:
                    emotion_list[0] += 1
                elif x in emotions[1]:
                    emotion_list[1] += 1
                elif x in emotions[2]:
                    emotion_list[2] += 1
                elif x in emotions[3]:
                    emotion_list[3] += 1
                elif x in emotions[4]:
                    emotion_list[4] += 1
            most=max(emotion_list)
            #如果没有表示情绪的词
            if most==0:
                return '中性'
            else:
                most_value_index=[i for i,x in enumerate(emotion_list) if x==most]
                #如果只有一种情绪
                if len(most_value_index)==1:
                    if most_value_index[0]==0:
                        return 'anger'
                    elif most_value_index[0]==1:
                        return 'disgust'
                    elif most_value_index[0]==2:
                        return 'fear'
                    elif most_value_index[0]==3:
                        return 'joy'
                    elif most_value_index[0]==4:
                        return 'sadness'
                #有多种情绪
                else:
                    a=random.choice(most_value_index)
                    if a==0:
                        return 'anger'
                    elif a==1:
                        return 'disgust'
                    elif a==2:
                        return 'fear'
                    elif a==3:
                        return 'joy'
                    elif a==4:
                        return 'sadness'
        return emotion_analysis_inner

#获取一条微博文字数据，输入num表示第几行
def get_data(filename,num):
    with open(filename,'r',encoding='utf8') as f:
        data=''.join(f.readlines(num)).split('\t')[1]
    return data

addto_my_jieba()
f1=emotion_analysis_outer(mode='vector')
f2=emotion_analysis_outer(mode='value')
# print(f1('我承认我过得一点也不好，很多时候我真的都熬不下去，快要崩溃了；我不知道哪儿有这么多压力，我改变的失去的都太多了，好多事情我真的接受不了，但我也无力抗拒，只能哭完了再爬起来老老实实继续走下去，因为我除了坚强别无选择!'))
# print(f2('我承认我过得一点也不好，很多时候我真的都熬不下去，快要崩溃了；我不知道哪儿有这么多压力，我改变的失去的都太多了，好多事情我真的接受不了，但我也无力抗拒，只能哭完了再爬起来老老实实继续走下去，因为我除了坚强别无选择!'))
# print(f2("新鲜出炉的卖萌父子俩❤"))

with open("weibo.txt",'r',encoding='utf8') as f:
    time_emotion=[(datetime.strptime(i.strip('\n').split('\t')[2], "%a %b %d %H:%M:%S +0800 %Y"),f2(i.strip('\n').split('\t')[1])) for i in f.readlines()]
    with open("time_emotion_tuple.txt",'w',encoding='utf8') as f1:
        print(time_emotion,file=f1)


def emotion_distribution(emotion,mode):
    if mode=='hour':
        time=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        emotion_count=[0 for i in range(0,24)]
        for ele in time_emotion:
            if ele[1]==emotion:
                emotion_count[time.index(ele[0].hour)]+=1
        plt.plot(time,emotion_count,c='red')
        plt.xlabel('time(hour)')
        plt.ylabel('number({})'.format(emotion))
        plt.show()
    elif mode=='day':
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,24,25,26,27,28,29,30,31]
        emotion_count = [0 for i in range(0, 31)]
        for ele in time_emotion:
            if ele[1] == emotion:
                emotion_count[time.index(ele[0].day)] += 1
        plt.plot(time, emotion_count,c='red')
        plt.xlabel('time(day)')
        plt.ylabel('number({})'.format(emotion))
        plt.show()
    elif mode=='week':
        time = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        emotion_count = [0 for i in range(0, 7)]
        with open("weibo.txt",'r',encoding='utf8') as f:
            week_lis=[(i.strip('\n').split('\t')[2][0:3],f2(i.strip('\n').split('\t')[1])) for i in f.readlines()]
        for ele in week_lis:
            if ele[1] == emotion:
                emotion_count[time.index(ele[0])] += 1
        plt.plot(time, emotion_count,c='red')
        plt.xlabel('time(day)')
        plt.ylabel('number({})'.format(emotion))
        plt.show()
    elif mode=='month':
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        emotion_count = [0 for i in range(0, 12)]
        for ele in time_emotion:
            if ele[1] == emotion:
                emotion_count[time.index(ele[0].month)] += 1
        plt.plot(time, emotion_count,c='red')
        plt.xlabel('time(day)')
        plt.ylabel('number({})'.format(emotion))
        plt.show()
emotion_distribution('anger','week')
# emotion_distribution('joy','hour')
# emotion_distribution('中性','day')
# emotion_distribution('sadness','week')
