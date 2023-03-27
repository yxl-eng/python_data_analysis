import jieba
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib
YaHei = FontProperties(fname=r'C:\Windows\Fonts\msyh.ttc')
matplotlib.rcParams['font.family']='SemHei'#SemHei为黑体
matplotlib.rcParams['axes.unicode_minus']=False
import numpy as np
from io import StringIO,BytesIO

class TextAnalyzer(object):
    _text_path='weibo.txt'
    _vector_size=300
    _window=5
    _min_count=1
    _stopword_path='stopwords.txt'
    _preprocessing_model_path='weibo_59g_embedding_200.model'

    def To_IO(self):
        s=StringIO()
        with open(self._text_path,'r',encoding='utf8') as f:
            s.write(f.read())
            s.seek(0)
        return s.readlines()

    def get_stop_list(self):
        with open(self._stopword_path, 'r', encoding='utf8') as f:
            stop_list = [word.strip('\n') for word in f.readlines()]
            return stop_list

    def preprocessing(self):
        stop_list = self.get_stop_list()
        words=[]
        for i in self.To_IO():
            words.append(list(word for word in jieba.cut(i.strip().split("\t")[1]) if word not in stop_list))
        return words

    def construct_word2vec_model(self):
        model= Word2Vec(sentences=self.preprocessing(), vector_size=self._vector_size, window=self._window, min_count=self._min_count)
        model.save("word2vec.model")
        return model

    def get_similar_words_tong(self):
        print('请输入一个单词(my_model)')
        word=str(input())
        return self.construct_word2vec_model().wv.most_similar(word, topn=10)

    def get_similar_words_fan(self):
        print('请输入一个单词(my_model)')
        word=str(input())
        return self.construct_word2vec_model().wv.most_similar(negative=[word], topn=10)

    def load_model(self,mode='most'):
        print('请输入一个单词（model1)')
        model1 = Word2Vec.load(self._preprocessing_model_path)
        word=str(input())
        most_similar=model1.wv.most_similar(word, topn=10)
        least_similar=model1.wv.most_similar(negative=[word], topn=10)
        if mode=='most':
            return most_similar
        elif mode=='least':
            return least_similar

    def visualize(self):
        # 将最相关和最不相关的词汇向量合并为一个数组
        most_similar=self.get_similar_words_tong()
        least_similar=self.get_similar_words_fan()
        model=self.construct_word2vec_model()
        vectors = np.array([model.wv[word] for word, similarity in most_similar + least_similar])
        print(vectors.shape)
        words = [word for word, similarity in most_similar + least_similar]

        # 使用t-SNE算法对词向量进行降维
        tsne = TSNE(n_components=2, perplexity=10)
        # print(vectors)
        vectors_tsne = tsne.fit_transform(vectors)

        # 可视化降维后的词向量
        fig, ax = plt.subplots()
        ax.set_title('难过', fontproperties=YaHei)
        ax.scatter(vectors_tsne[:10, 0], vectors_tsne[:10, 1], color='blue')
        ax.scatter(vectors_tsne[10:, 0], vectors_tsne[10:, 1], color='red')
        for i, word in enumerate(words):
            ax.annotate(word, (vectors_tsne[i, 0], vectors_tsne[i, 1]), fontproperties=YaHei)
        plt.show()

    def add_to_dictionary(self):
        model1 = Word2Vec.load(self._preprocessing_model_path)
        print('请输入保存文档')
        result_file=input()
        print('请输入一个单词（model1)')
        word = str(input())
        with open (fr'../情绪分析（第二周）/emotion_lexicon/{result_file}','w',encoding='utf8') as f:
            for word,possible in model1.wv.most_similar(word, topn=5):
                print(word,file=f)

a=TextAnalyzer()
print(a.get_similar_words_tong())
print(a.load_model())
a.visualize()

