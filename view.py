from pyecharts import options as opts
from pyecharts.charts import Page, Pie
from pyecharts.components import Table
import main
import pymysql

db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='hesuan_result_collection')
cursor = db.cursor()
# sql_count_failed = "SELECT count(sno) FROM xinan GROUP BY `time_result` = '时间匹配失败' or `test_result` = '结果存疑'"
sql_find_failed = "SELECT DISTINCT sname,sno,time_result,test_result FROM xinan WHERE time_result = '时间匹配失败' or test_result = '结果存疑'"
sql_readyto_submit = "SELECT DISTINCT sname,sno,time_result,test_result FROM xinan " \
                     "WHERE time_result = '时间匹配失败' or test_result = '结果存疑'" \
                     "or time_result = '' or test_result = ''"
main.student_failed = cursor.execute(sql_find_failed)
main.student_left = main.student_num - main.student_checked - main.student_failed


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


if __name__ == "__main__":
    page_simple_layout()
