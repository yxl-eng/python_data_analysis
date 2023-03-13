from datetime import datetime
with open("weibo.txt",'r',encoding='utf8') as f:
    week_lis=[i.strip('\n').split('\t')[2][0:3] for i in f.readlines()]


print(week_lis)
