import jieba
#获取禁用词并放到一个列表里
def get_stop_list(file):
    with open(file,'r',encoding='utf8') as f:
        stop_list=[word.strip('\n') for word in f.readlines()]
        return stop_list

stop_list=get_stop_list('stopwords.txt')

def word_process(sentence):
    '''
    数据预处理
    :param sentence: 句子
    :return:空格连接字符串
    '''

    # 使用jieba分词对文本进行分词操作，并去除符号
    words = [word for word in jieba.cut(sentence) if word not in stop_list]

    # 将分词结果使用空格连接成字符串
    result = ' '.join(words)
    return result