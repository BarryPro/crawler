# -*- coding: UTF-8 -*-
import xlsxwriter
import time


def run():
    # print startTime
    start_time = time.time()
    # print startTime1

    # 创建一个Excel文件
    workbook = xlsxwriter.Workbook('C:\\Users\\Administrator\\Desktop\\80s.xlsx')
    # 创建一个sheet
    worksheet = workbook.add_worksheet(U'80s视频资源')

    # 表格title
    title = ['video_name', 'image_url', 'video_url']
    # title 写入Excel,写入行数据
    worksheet.write_row('A1', title)

    for i in range(1, 100):
        data = [u'学生' + str(i), i, i, ]
        write_excel_by_row(i, data, worksheet)

    workbook.close()

    end_time = time.time()
    # print endTime1

    print end_time - start_time


def write_excel_by_row(index, data, worksheet):
    num0 = bytes(index + 1)
    # 生成行号
    row = 'A' + num0
    worksheet.write_row(row, data)
    index += 1


if __name__ == '__main__':
    # 开始处理006dy网站资源
    run()
