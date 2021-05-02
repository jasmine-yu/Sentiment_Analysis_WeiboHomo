from tfidf import tfidf_text
from fenci import read_file
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import xlrd
import xlwt

#选择knn的k=5
K = 5

# 权重向量已归一化
# 特征向量之间的距离度量为余弦相似度

def cos_distence(x,y):
    #knn的自定义距离要满足以下条件：
    #非负性：d（x，y）> = 0
    #当且仅当x == y时，d（x，y）= 0
    #对称性：d（x，y）= d（y，x）
    #三角不等式：d（x，y）+ d（y，z）> = d（x，z
    #因此实际的余弦相似度距离为：1-余弦相似度
    num = x.dot(y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    cos_sim = num / denom
    return 1-cos_sim

def cos_score(distence_arr5):
    #按余弦相似度确定权重,输入为最相近的5个距离数组
    cos_sim_arr =1-distence_arr5
    return cos_sim_arr/K

def knn_text(X_train,Y_train,X_test):
    model = KNeighborsClassifier(n_neighbors=K,metric=cos_distence,weights=cos_score)
    model.fit(X_train, Y_train)
    Y_test = model.predict(X_test)
    return Y_test

if __name__ == "__main__":
    y_train_1_200 = xlrd.open_workbook('train.xlsx').sheet_by_index(0).col_values(13, start_rowx=0, end_rowx=200)
    y_train_2_200 = xlrd.open_workbook('train.xlsx').sheet_by_index(0).col_values(14, start_rowx=0, end_rowx=200)
    y_train_3_200 = xlrd.open_workbook('train.xlsx').sheet_by_index(0).col_values(15, start_rowx=0, end_rowx=200)
    y_train_200 = np.array([y_train_1_200,y_train_2_200,y_train_3_200]).T

    x_train_weight, x_test_weight, name_train, name_test = tfidf_text()  # 输出训练集和测试集top50文本特征向量，以及top 50的特征名，权重向量以归一化

    y_train_201_2000 = knn_text(x_train_weight[:200],y_train_200,x_train_weight[200:])#训练集后1800的预测标签

    y_train =np.vstack((y_train_200,y_train_201_2000))#训练集标签

    y_test = knn_text(x_train_weight,y_train,x_test_weight)#测试集标签

    y_label_list = np.vstack((y_test,y_test)).tolist()
    wbk = xlwt.Workbook(encoding="utf-8")
    datasheet = wbk.add_sheet("sheet1")
    for i in range(20000):
        for j in range(3):
            datasheet.write(i, j, y_label_list[i][j])
    wbk.save("result.xlsx")