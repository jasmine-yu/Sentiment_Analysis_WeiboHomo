from fenci import jieba_cut
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle

def tfidf_text():

    cutlist = jieba_cut('train.xlsx','test.xlsx',save=False)

    x_train = cutlist[0:2000]
    x_test = cutlist[2000:20000]

    # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer(max_features=50, decode_error="replace")
    # 该类会统计每个词语的tf-idf权值
    tf_idf_transformer = TfidfTransformer()
    # 将文本转为词频矩阵并计算tf-idf
    tf_idf = tf_idf_transformer.fit_transform(vectorizer.fit_transform(x_train))
    # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    x_train_weight = tf_idf.toarray()
    #vectorizer 与tfidftransformer都要保存，而且只能 fit_transform 之后保存，表示vectorizer 与tfidftransformer已经用训练集训练好了。
    feature_path = 'models/feature.pkl'
    with open(feature_path, 'wb') as fw:
        pickle.dump(vectorizer.vocabulary_, fw)

    tfidftransformer_path = 'models/tfidftransformer.pkl'
    with open(tfidftransformer_path, 'wb') as fw:
        pickle.dump(tf_idf_transformer, fw)

    # 加载特征
    feature_path = 'models/feature.pkl'
    loaded_vec = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(feature_path, "rb")))
    # 加载TfidfTransformer
    tfidftransformer_path = 'models/tfidftransformer.pkl'
    tf_idf_transformer = pickle.load(open(tfidftransformer_path, "rb"))
    # 测试用transform，表示测试数据，为list
    tf_idf = tf_idf_transformer.transform(loaded_vec.transform(x_test))


    # 对测试集进行tf-idf权重计算
    #tf_idf = tf_idf_transformer.transform(vectorizer.transform(x_test))#不保存情况下直接调用
    x_test_weight = tf_idf.toarray()  # 测试集TF-IDF权重矩阵

    #print('输出x_train文本向量：')
    #print(x_train_weight)
    #print('输出x_test文本向量：')
    #print(x_test_weight)

    return x_train_weight,x_test_weight,vectorizer.get_feature_names(),loaded_vec.get_feature_names()

if __name__ == "__main__":
    x_train_weight,x_test_weight,name_train, name_test = tfidf_text()#输出训练集和测试集top50文本特征向量，以及top 50的特征名