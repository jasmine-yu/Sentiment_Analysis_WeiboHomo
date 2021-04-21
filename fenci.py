import xlrd
import jieba
xlsx = xlrd.open_workbook('D:/weibo/dataframe_2.xlsx')
#xlsx = xlrd.open_workbook('D:/weibo/test_data.xlsx')
table = xlsx.sheet_by_index(0)
nrows = table.nrows
for i in range(nrows):
    value = table.cell_value(i, 0)
    value=jieba.cut(value, cut_all=False)
    words=' '.join(value)
    f = open('D:/weibo/fenci_txt/'+str(i+1+2000)+'.txt','w',encoding='utf-8')
    f.write(words)
    f.close()