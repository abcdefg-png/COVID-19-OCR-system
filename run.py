import schedule
import os
import zipfile
import shutil
import main

dirname = r"testimg1"
filepath = r"testimg1"

def run():
    os.system("python view.py")


def clear():
    db = main.db
    cursor = db.cursor()
    sql_delete = "Update xinan set time_result = '' , test_result = '' "
    cursor.execute(sql_delete)
    db.commit()
    shutil.rmtree(filepath)
    os.mkdir(filepath)


def zip(file):
    zipfile_name = os.path.basename(file) + '.zip'
    with zipfile.ZipFile(zipfile_name, 'w') as zfile:
        for foldername, subfolders, files in os.walk(file):
            zfile.write(foldername)
            for i in files:
                zfile.write(os.path.join(foldername, i))
        zfile.close()


schedule.every().day.at("10:00").do(run)  # 每天的10:30执行一次任务
schedule.every().monday.at("00:00").do(clear)
schedule.every().sunday.at("19:00").do(zip(dirname))

while True:
    schedule.run_pending()  # run_pending：运行所有可以运行的任务
