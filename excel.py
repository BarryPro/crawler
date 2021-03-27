# -*- coding: UTF-8 -*-
import xlsxwriter
import datetime
import time

# 现在
# startTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print startTime
startTime1 = time.time()
# print startTime1

# 创建一个Excel文件
workbook = xlsxwriter.Workbook('C:\Users\Administrator\Desktop\80s.xlsx')
# 创建一个sheet
worksheet = workbook.add_worksheet()

# 表格title
title = [U'名称', U'副标题']
# title 写入Excel
worksheet.write_row('A1', title)

for i in range(1, 100):
    num0 = bytes(i+1)
    num = bytes(i)
    row = 'A' + num0
    data = [u'学生'+num,num,]
    worksheet.write_row(row, data)
    i += 1

workbook.close()

# time.sleep(60)
# endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#结束
# print endTime

endTime1 = time.time()
# print endTime1

print endTime1-startTime1
