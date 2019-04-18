import xlwt


# 设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    al = xlwt.Alignment()
    al.vert = 0x01  # 垂直居中对齐
    al.horz = 0x02  # 水平居中对齐
    style.alignment = al

    return style


row_index = 0


# 写Excel
def write_excel_row(groups):
    f = xlwt.Workbook()
    # 创建表单
    sheet = f.add_sheet('常去的小组',cell_overwrite_ok=True)
    titles = ['id','昵称','常去的小组','链接']
    # 写入标题
    for a in range(0,len(titles)):
        sheet.write(0, a, titles[a], set_style('Times New Roman', 220, True))
    # 写入数据
    index = 0
    for i in range(0,len(groups)):
        rows = groups[i]
        m = len(rows)
        for j in range(0,m):
            row = rows[j]
            for b in range(0,len(row)):
                sheet.write(index, b, row[b], set_style('Times New Roman', 220, False))
            index += 1
        # 合并单元格
        sheet.write_merge(index - m, index - 1, 0, 0, 'My merge', set_style('Times New Roman', 220, False)) # 合并id
        sheet.write_merge(index - m, index - 1, 1, 1, 'My merge', set_style('Times New Roman', 220, False)) # 合并昵称
    f.save('data.xls')