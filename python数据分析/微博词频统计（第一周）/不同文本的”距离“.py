import jieba
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
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
            lis=list(jieba.lcut(i))
            word_list.extend(lis)
        text=''
        for w in word_list:
            if w not in stop_list:
                if len(w)==1 and w!='\n':
                    text+=str(w+'decorated ')
                elif w!='\n':
                    text+=str(w+' ')
        return text

stop_list=get_stop_list("stopwords.txt")
text1=clean_stopword('wenzhang1.txt',stop_list)
text2=clean_stopword('wenzhang2.txt',stop_list)

count = CountVectorizer()
# 语料库
docs=[]
docs.append(text1)
docs.append(text2)
# bag是一个稀疏的矩阵。因为词袋模型就是一种稀疏的表示。
bag = count.fit_transform(docs)
# 输出单词与编号的映射关系。
print(count.vocabulary_)
# 调用稀疏矩阵的toarray方法，将稀疏矩阵转换为ndarray对象。
print(bag)
mo1=np.linalg.norm(bag.toarray()[0])
mo2=np.linalg.norm(bag.toarray()[1])
mo=mo1*mo2
print(np.dot(bag.toarray()[0],bag.toarray()[1])/mo)