import xlrd
import jieba

def jieba_cut(train,test,cutlist=[],save=True):
    xlsx_train = xlrd.open_workbook(train)
    xlsx_test = xlrd.open_workbook(test)
    table_train = xlsx_train.sheet_by_index(0)
    table_test = xlsx_test.sheet_by_index(0)
    nrows_train = table_train.nrows
    nrows_test = table_test.nrows

    for i in range(nrows_train):
        value = table_train.cell_value(i, 0)
        value = jieba.cut(value, cut_all=False)
        words = ' '.join(value)
        cutlist.append(words)
        if save:
            f = open('jieba_cut_txt/' + str(i + 1) + '.txt', 'w', encoding='utf-8')
            f.write(words)
            f.close()


    for i in range(nrows_test):
        value = table_test.cell_value(i, 0)
        value = jieba.cut(value, cut_all=False)
        words = ' '.join(value)
        cutlist.append(words)
        if save:
            f = open('jieba_cut_txt/' + str(i + 1 + 2000) + '.txt', 'w', encoding='utf-8')
            f.write(words)
            f.close()

    return cutlist


if __name__ == "__main__":
    cutl = jieba_cut('train.xlsx','test.xlsx',save=False)