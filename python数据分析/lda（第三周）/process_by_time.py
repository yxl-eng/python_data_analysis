import datetime
def sort_doc(file_path):
    '''
    文档分类
    :param file_path: 分档路径
    :return:分类结果
    '''
    # 定义时间段
    morning_start = datetime.time(4, 0, 0)
    noon_start = datetime.time(12, 0, 0)
    evening_start = datetime.time(20, 0, 0)

    # 定义数据分类字典
    data_by_time = {
        "morning": [],
        "noon": [],
        "evening": []
    }

    # 读取数据文件
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # 解析每一行数据
            fields = line.strip().split("\t")
            coords = fields[0]
            text = fields[1]
            time_str = fields[2]

            # 将时间字符串转换为datetime对象
            time = datetime.datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y").time()
            # 根据时间段将数据添加到相应的分类列表中
            if time >= morning_start and time < noon_start:
                data_by_time["morning"].append((coords, text))
            elif time >= noon_start and time < evening_start:
                data_by_time["noon"].append((coords, text))
            else:
                data_by_time["evening"].append((coords, text))
    return data_by_time

if __name__=='__main__':
    data_by_time=sort_doc('weibo.txt')
    print(data_by_time)