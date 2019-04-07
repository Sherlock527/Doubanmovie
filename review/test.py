from redis import Redis
import json
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 加载停用词
stopwords = set()
with open('chineseStopWords.txt', encoding='gbk') as f:
    for line in f:
        # print(line.rstrip('\r\n').encode())  # bytes来观察特殊字符
        stopwords.add(line.rstrip('\r\n'))
    stopwords.add(' ')
# print(len(stopwords))  # 980
# print(stopwords)  # {'公司', '另外', '一旦'...}

# 读取影评
redis = Redis('192.168.2.132')
items = redis.lrange('dbreview:items', 0, -1)
print(type(items))  # <class 'list'>

# 不使用停用词
words = {}
for item in items:
    val = json.loads(item)['review']
    for word in jieba.cut(val):
        words[word] = words.get(word, 0) + 1
print(len(words))  # 1558
print(sorted(words.items(), key=lambda x:x[1], reverse=True)[:10])  # [('，', 338), ('的', 163), ('。', 120), ('了', 76), ('是', 40), ('海王', 37), ...]

# 使用停用词
words = {}
total = 0
for item in items:
    val = json.loads(item)['review']
    for word in jieba.cut(val):
        if word not in stopwords:
            words[word] = words.get(word, 0) + 1
            total += 1
print(len(words))  # 1271
print(sorted(words.items(), key=lambda x:x[1], reverse=True)[:10])  # [('海王', 37), ('DC', 21), ('温子仁', 18), ('海底', 16), ('电影', 14), ('＋', 14), ('→', 13), ('集体', 12), ('鼓掌', 12), ('\n', 11)...]
# 总数
print(total)  # 1936

# 词频
frenq = {k:v/total for k,v in words.items()}
print(sorted(frenq.items(), key=lambda x:x[1], reverse=True)[:10])  # [('海王', 0.019111570247933883), ('DC', 0.01084710743801653), ('温子仁', 0.009297520661157025)...]

# 字体，背景色，最大字体
wordcloud = WordCloud(font_path='Hiragino Sans GB.ttc', background_color='white', max_font_size=80, scale=15)

plt.figure(2)  # 绘制窗口ID=2
wordcloud.fit_words(frenq)  # 使用单词和词频创建词云

plt.imshow(wordcloud)  # 将图显示在二维坐标轴上
plt.axis('off')  # 不打印坐标系
plt.show()