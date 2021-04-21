# Sentiment_Analysis_WeiboHomo
通过分析20000条关于对艾滋病看法的微博，1.分析现阶段微博用户整体的态度，2.探究不同性别、地域等的用户在态度上的差异。（标注数据占比1%）
态度包括：认知、情感、行为倾向三个部分。



1.文本数据预处理

​    1）随机按行打乱微博数据——random_excel.py

​    2）划分训练集：测试集=2000：18000

​    3）标注数据细则：认知，情感，行为（0~5分）

​        0分：无用信息不考虑

​        1-5分：对艾滋病越来越积极



2.文本分词（Jieba分词）

​    代码：fenci.py
​    1）首先对微博中的用户名前缀和内部的url链接进行过滤删除
​    2）对初步过滤的微博内容进行jieba分词
​    3）利用停用词语库剔除停用词，这里的停用词用的是stopwords.dat,具体可查看可更新
​    4）分词得到的结果按照'微博的id号+.txt'命名，训练集id:1-2000,测试集2001-20001
​    具体格式如：20.txt：存储内容为第20个微博用户的分词内容。压缩文件见fenci_txt.rar



3.文本特征提取（TF-IDF）



tf-idf模型的主要思想是：**如果词w在一篇文档d中出现的频率高，并且在其他文档中很少出现，则认为词w具有很好的区分能力，适合用来把文章d和其他文章区分开来。**



该模型主要包含了两个因素：



1. 词w在文档d中的词频tf(Term Frequency)，即词w在文档d中出现次数count(w,d)和文档d中总词数size(d)的比值：tf(w,d) = count(w,d)/size(d)

   

2. 词w在整个文档集合中的逆向文档频率idf(Inverse Document Frequency)，即文档总数n与词w所出现文件数docs(w,D)比值的对数：idf = log(n/docs(w,D))

   

tf-idf模型根据tf和idf为每一个文档d和由关键词w[1]…w[k]组成的查询串q计算一个权值，用于表示查询串q与文档d的匹配度。



TfidfTransformer是把TF矩阵转成TF-IDF矩阵，所以需要先词频统计CountVectorizer，转换成TF-IDF矩阵



`tfidf.py`中，输入为jieba分词后的结果，train训练top50 的 tf-idf模型，生成词频向量模型vectorizer和tf转换模型tf_idf_transformer，并保存入models文件夹。vectorizer 与tfidftransformer都要保存，而且只能 fit_transform 之后保存，表示vectorizer 与tfidftransformer已经用训练集训练好了。之后在测试集上加载模型生成tf-idf权重矩阵。



最终输出为：



x_train_weight训练集的文本特征向量（tf-idf权重矩阵，2000*50ndarray）



x_test_weight测试集的文本特征向量（tf-idf权重矩阵，18000*50ndarray）



name_train训练集的top50特征名（list:50,排名前50 的词汇）



name_test同上



4.文本自动分类（KNN）


5.数据可视化
（1）对于标注的数据，绘制了态度的三个成分（情感，认知，行为）的打分频次图，可以一定程度上看到人们的态度成分倾向
     代码见frequency.py，图片保存在picture文件夹中。
