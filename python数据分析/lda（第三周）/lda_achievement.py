import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pickle
import process_by_time
import preprocessing
import pyLDAvis
from pyLDAvis import sklearn as ps
if __name__=='__main__':
    docs_by_time=process_by_time.sort_doc('weibo.txt')
    # print(docs_by_time)
    docs=[]
    # print(len(docs_by_time['morning']))
    for i in range(len(docs_by_time['morning'])):
        docs.append(preprocessing.word_process(docs_by_time['morning'][i][1]))
    for i in range(len(docs_by_time['noon'])):
        docs.append(preprocessing.word_process(docs_by_time['noon'][i][1]))
    for i in range(len(docs_by_time['evening'])):
        docs.append(preprocessing.word_process(docs_by_time['evening'][i][1]))
    # print(docs)
    # 将文本转换成词频矩阵
    vectorizer = CountVectorizer()
    # 将文本转换成tf-idf矩阵
    # vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(docs)

    # 计算困惑度绘制elbow图确定主题数量
    perplexity_scores = []
    k_range = range(1, 6)  # 假设k的范围是1到5
    for k in k_range:
        lda = LatentDirichletAllocation(n_components=k)
        lda.fit(X)
        perplexity_scores.append(lda.perplexity(X))
    plt.plot(k_range, perplexity_scores, '-o')
    plt.xlabel('Number of topics')
    plt.ylabel('Perplexity')
    plt.show()

    k = 4
    # 使用LatentDirichletAllocation构建主题模型
    lda = LatentDirichletAllocation(n_components=k)
    lda.fit(X)

    # 输出每个主题对应的词语
    feature_names = vectorizer.get_feature_names_out()
    with open('result.txt','w',encoding='utf8') as f:
        for i, topic in enumerate(lda.components_):
            print(f"Topic {i}:",file=f)
            top_words = [feature_names[j] for j in topic.argsort()[:-6:-1]]
            print(top_words,file=f)

        # 输出每篇文档的主题概率分布
        for i in range(len(docs)):
            print(f"Document {i}:",file=f)
            print(lda.transform(X[i]),file=f)
    # 输出结果

    pickle.dump((lda, X, vectorizer), open('./lda_model.pkl', 'wb'))

    #图形化显示
    data = ps.prepare(lda, X, vectorizer)
    pyLDAvis.display(data)