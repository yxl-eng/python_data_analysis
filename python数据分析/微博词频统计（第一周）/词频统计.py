import jieba
import jieba.posseg
import wordcloud
from matplotlib.pyplot import imread
import numpy as np

#去除噪声
def gettext(txt):
    for char in '!！"@#$%^&*()_+=-,./;\[]<>?:~-—～''（）〜…{}|~`《》，。、；‘【】、”《》?？：“‘':
        txt=txt.replace(char,'')
    return txt
#把weibo.txt里的文字部分用jieba库拆开，并把所有词语放到一个列表content里
with open("weibo.txt", 'r', encoding='utf8') as f:
    content=''
    for i in f.readlines():
        sentense=gettext(i.split()[2])
        content+=sentense
content=jieba.lcut(content)    #分词
#进行词频统计
dict={}
for i in content:
    count=dict.get(i,0)
    dict[i]=count+1
a=sorted(dict.items(),key=lambda x:x[1],reverse=True)           #按照词频排序
with open("微博词频统计结果（未禁用词）.txt", 'w', encoding='utf8') as f:      #打印到文件
    print(a,file=f)

#获取禁用词并放到一个列表里
def get_stop_list(file):
    with open(file,'r',encoding='utf8') as f:
        stop_list=[word.strip('\n') for word in f.readlines()]
        return stop_list

#去除禁用词后的文本分词，并放到新的列表new_word_list里
def clean_stopword(file,stop_list):
    with open(file,'r',encoding='utf8') as f:
        word_list = []
        for i in f.readlines():
            lis=list(jieba.lcut(gettext(i.split()[2])))
            word_list.extend(lis)
        new_word_list=[]
        for w in word_list:
            if w not in stop_list:
                new_word_list.append(w)
        return new_word_list

stop_list=get_stop_list("stopwords.txt")           #获取禁用词列表
new_word_list=clean_stopword("weibo.txt", stop_list)
#禁用词后的词频统计
dict1={}
for i in new_word_list:
    count=dict1.get(i,0)
    dict1[i]=count+1
b=sorted(dict1.items(),key=lambda x:x[1],reverse=True)
with open("微博词频统计结果（禁用词）.txt", 'w', encoding='utf8') as f:
    print(b,file=f)

#画词云图
mk=imread("img.jpg")
mk = mk.astype(np.uint8)
c=wordcloud.WordCloud(width=600,height=400,min_font_size=10,max_font_size=100,font_step=2,max_words=100
                     ,font_path='msyh.ttc',scale=2,stopwords={'python'},mask=mk,background_color='white')
c.generate(" ".join(new_word_list))
c.to_file("微博词频统计.png")


#词性标注
def pos_sentence(sentence):
    sentence_seged = jieba.posseg.cut(sentence)
    outstr = ''
    noutstr=[]
    for x in sentence_seged:
        outstr += "{}/{}  ".format(x.word, x.flag)
        if x.flag=='n':
            noutstr.append(x.word)
    return outstr,noutstr

def count_dif_word(sentence):
    sentence_seged = jieba.posseg.cut(sentence)
    result={}
    for x in sentence_seged:
        count=result.get(x.flag,0)
        result[x.flag]=count+1
    return result

dif_word_num=count_dif_word(''.join(new_word_list))
print(dif_word_num)
#得到带标注的词语列表与名词列表
word_withpos,n_words=pos_sentence(''.join(new_word_list))
#写到文件里
with open("微博词频统计结果（禁用词+词性分类）.txt",'w',encoding='utf8') as f:
    print(word_withpos,file=f)
    dict2 = {}
    for i in n_words:
        count = dict2.get(i, 0)
        dict2[i] = count + 1
    c = sorted(dict2.items(), key=lambda x: x[1], reverse=True)
    with open("微博词频统计结果（禁用词+名词）.txt", 'w', encoding='utf8') as f1:
        print(c, file=f1)

#生成名词词云图
c1=wordcloud.WordCloud(width=600,height=400,min_font_size=10,max_font_size=100,font_step=2,max_words=100
                      ,font_path='msyh.ttc',scale=2,stopwords={'python'},mask=mk,background_color='white')
c1.generate(" ".join(n_words))
c1.to_file("微博词频统计(名词）.png")