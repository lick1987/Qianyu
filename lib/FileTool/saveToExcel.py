# -*- coding: utf-8 -*-
import xlrd
import xlwt
from datetime import date, datetime




def save_excel():
    # 打开文件
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 获取所有sheet
    # 创建一个worksheet
    worksheet = workbook.add_sheet('My Worksheet')

    # 写入excel
    # 参数对应 行, 列, 值
    exList=['接单时间','接单账号','客户姓名','抬头','要求','数量',
            '未打完','开票员','截止日期','发票类型','状态','拿取方式',
            '地址','点子','应收','实收','预计成本','实际成本','预计利润','实际利润']
    for index,i in enumerate(exList):
        worksheet.write(0, index, label=i)

    # 保存
    workbook.save('Excel_test.xls')

save_excel()