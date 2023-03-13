import bisect
import random
import collections
# l=[random.random() for i in range(10)]
# d=[]
# for n in l:
#     pos=bisect.bisect(d,n)
#     print(pos)
#     bisect.insort(d,n)
# print(d)

# from collections import namedtuple
# student=namedtuple("student",['name','credit','hometown'])
# s1=student(name='jack',credit=100,hometown='shanxi')
# print(s1)

# a=dict(list(enumerate(['one','two','three'],start=1)))
# print(a)

# d1={'path':'/c/d/e','cmd':'clear','pwd':'$'}
# d2={'root':'/','cmd':'cls','pwd':'#','prompt':'True'}
# d=collections.ChainMap(d1,d2)
# print(d)
# print(d['path'])
# print(d['cmd'])
# d['cmd']='update'
# print(d1['cmd'])
# print(d2['cmd'])

# freq=collections.Counter(['a', 'b', 'c', 'a', 'a', 'b'])
# print(freq)
# freq.update('bbcb')
# print(freq)
# for l in "abc":
#     print("{}:{}".format(l,freq[l]))

# def default_value():#该可调用对象用来设定默认值
#     return 999
# dc = collections.defaultdict(default_value,zjc=28)#default_value可以是None
# print(dc['zjc'])
# print(dc['lsy'])
# dc['lsy']+=1
# print(dc['lsy'])

# unsorted_d={'cat':8,"dog":9,"human":20,"lk":1}
# dic = collections.OrderedDict()
# print(dic)
# dic=collections.OrderedDict(sorted(unsorted_d.items(), key=lambda dc:dc[1], reverse = True))
# print(dic)

# s = 'RUNOOB'
# print(repr(s))
#
# dict = {'runoob': 'runoob.com', 'google': 'google.com'};
# print(repr(dict))

