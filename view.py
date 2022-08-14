from pyecharts import options as opts
from pyecharts.charts import Page, Pie
from pyecharts.components import Table
import main
import openpyxl

db = main.db
cursor = db.cursor()
table_name = "xinan"
excel_name = r"xinan_result.xlsx"

sql_count_left = "SELECT DISTINCT * from xinan WHERE time_result = '' or test_result = '' "
sql_find_failed = "SELECT DISTINCT sname,sno,time_result,test_result FROM xinan WHERE time_result = '时间匹配失败' or test_result = '结果匹配失败'"
sql_readyto_submit = "SELECT DISTINCT sname,sno,time_result,test_result FROM xinan " \
                     "WHERE time_result = '时间匹配失败' or test_result = '结果匹配失败'" \
                     "or time_result = '' or test_result = ''"
main.student_failed = cursor.execute(sql_find_failed)
main.student_left = cursor.execute(sql_count_left)
main.student_checked = main.student_num - main.student_left - main.student_failed


# 将每个图 封装到 函数
# 3.玫瑰型饼图
def pie_base():
    label = ['识别成功', '未提交', '识别错误']
    values = [main.student_checked, main.student_left, main.student_failed]
    c = (
        Pie()
            .add("", [list(z) for z in zip(label, values)])
            .set_global_opts(title_opts=opts.TitleOpts(title="20信安提交结果"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}人 {d}%"))  # 值得一提的是，{d}%为百分比
    )
    return c


# 表格
def table_base() -> Table:
    cursor.execute(sql_find_failed)
    temp = cursor.fetchall()
    failed_match = []
    for i in temp:
        x = list(i)
        failed_match.append(x)
    table = Table()
    headers = ["学号", "姓名", "检测时间", "检测结果"]
    rows = failed_match
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="识别失败名单")
    )
    return table


def table_base2() -> Table:
    cursor.execute(sql_readyto_submit)
    temp = cursor.fetchall()
    readyto_submit = []
    for i in temp:
        x = list(i)
        readyto_submit.append(x)
    table = Table()
    headers = ["学号", "姓名", "检测时间", "检测结果"]
    rows = readyto_submit
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="待提交（包含识别失败）名单")
    )
    return table


def page_simple_layout():
    page = Page(layout=Page.SimplePageLayout)  # 简单布局
    page.add(
        pie_base(),
        table_base(),
        table_base2(),
    )
    page.render("./result.html")


def Export2Excel(table_name):
    # 连数据库，读取数据
    conn = db
    cur = conn.cursor()
    sql = "select * from %s;" % table_name
    cur.execute(sql)
    # 使用 %s 占位符可以占位 where 条件，但是不能占位表名
    sql_result = cur.fetchall()
    cur.close()
    conn.close()
    # 写 Excel
    book = openpyxl.Workbook()
    sheet = book.active
    fff = [filed[0] for filed in cur.description]  # 获取表头信息
    sheet.append(fff)
    for i in sql_result:
        sheet.append(i)
    book.save("%s" % excel_name)


if __name__ == "__main__":
    page_simple_layout()
    Export2Excel(table_name=table_name)
