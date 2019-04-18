import xlwt
import xlrd


# 设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


row_index = 0


# 写Excel
def write_excel_row(groups):
    f = xlwt.Workbook()
    # 创建表单
    sheet = f.add_sheet('我常去的小组',cell_overwrite_ok=True)
    # 写入行
    for i in range(0,len(groups)):
        sheet.write(row_index,i,groups[i],set_style('Times New Roman',220,False))
    f.save('data.xls')


if __name__ == '__main__':
    groups = ['gafga','ghdhdh','63hdeh','gafga','ghdhdh','63hdeh']
    for i in range(0,10):
        write_excel_row(groups)
        row_index = row_index + 1