import xlrd
import jieba
import re
from collections import Counter
import json


#按行读取文件，返回文件的行字符串列表
def read_file(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    #去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines

#将content内容保存在对应的file_name文件
def save_file(file_name, content):
    fp = open(file_name, "w", encoding="utf-8")
    fp.write(content)
    fp.close()

#对微博中的用户名前缀和内部的url链接进行过滤删除
def regex_change(line):
    #前缀的正则
    username_regex = re.compile(r"^\d+::")
    #URL，为了防止对中文的过滤，所以使用[a-zA-Z0-9]而不是\w
    url_regex = re.compile(r"""
        (https?://)?
        ([a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)*
        (/[a-zA-Z0-9]+)*
    """, re.VERBOSE|re.IGNORECASE)
    #剔除日期
    data_regex = re.compile(u"""        #utf-8编码
        年 |
        月 |
        日 |
        (周一) |
        (周二) | 
        (周三) | 
        (周四) | 
        (周五) | 
        (周六)
    """, re.VERBOSE)
    #剔除所有数字
    decimal_regex = re.compile(r"[^a-zA-Z]\d+")
    #剔除空格
    space_regex = re.compile(r"\s+")

    line = username_regex.sub(r"", line)
    line = url_regex.sub(r"", line)
    line = data_regex.sub(r"", line)
    line = decimal_regex.sub(r"", line)
    line = space_regex.sub(r"", line)

    return line

#剔除停用词
def delete_stopwords(line):
    stopword_file = "stopwords.dat"
    stopwords = read_file(stopword_file)
    words=[]
    #line = jieba.cut(line, cut_all=False)
    #words = ' '.join(line if line not in stopwords)
    words += [word for word in jieba.cut(line) if word not in stopwords]
    words=' '.join(words)

    return words

def jieba_cut(train,test,cutlist=[],save=True):
    xlsx_train = xlrd.open_workbook(train)
    xlsx_test = xlrd.open_workbook(test)
    table_train = xlsx_train.sheet_by_index(0)
    table_test = xlsx_test.sheet_by_index(0)
    nrows_train = table_train.nrows
    nrows_test = table_test.nrows

    for i in range(nrows_train):
        value = table_train.cell_value(i, 0)
        value = regex_change(value)
        words = delete_stopwords(value)
        cutlist.append(words)
        if save:
            save_file('jieba_cut_txt/'+str(i+1)+'.txt', words)


    for i in range(nrows_test):
        value = table_test.cell_value(i, 0)
        value = regex_change(value)
        words = delete_stopwords(value)
        cutlist.append(words)
        if save:
            save_file('jieba_cut_txt/'+str(i+2001)+'.txt', words)

    return cutlist

if __name__ == "__main__":
    cutl = jieba_cut('train.xlsx','test.xlsx',save=False)