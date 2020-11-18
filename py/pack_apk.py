# -*- coding: utf-8 -*-
# @Time    : 2020/09/21 18:09
# @Author  : bobby
# @Software: PyCharm

import os
import zipfile
import shutil
from shutil import copyfile
import platform


def zip_file(src_dir):
    zip_name = src_dir +'.zip'
    z = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        fpath = dirpath.replace(src_dir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath+filename)
            print('==压缩成功==')
    z.close()


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


count = 0
root_path = os.getcwd()

if "Window" in platform.platform():
    root_path = root_path.replace("\\", "\\\\")


# 清理xxx-target.apk，也就是已经从新生成的apk文件

for i in os.listdir(os.getcwd()):
    if os.path.isfile(i) & i.endswith("target.apk"):
        os.remove(i)

# 为所有的dex文件重命名

for i in os.listdir(os.getcwd()):
    if os.path.isfile(i):
        if i.endswith(".dex"):
            print(i)
            if count == 0:
                os.rename(i, "classes.dex")
                print("classes.dex")
                count = count+1
            else:
                name = "classes{index}.dex".format(index=str(count))
                os.rename(i, name)
                print(name)
                count = count + 1


# 为apk文件塞入重命名后的dex文件列表
for j in os.listdir(os.getcwd()):
    if os.path.isfile(j) & j.endswith(".apk"):
        print(j)
        zip_name = j+".new.zip"
        try:
            copyfile(j, zip_name)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)

        unzip_file(zip_name, "zip_tmp")

        if os.path.isdir("zip_tmp"):
            root_p = os.getcwd()
            zip_tmp_path = os.path.abspath("zip_tmp")
            # 删除所有的dex文件
            for i in os.listdir("zip_tmp"):
                if os.path.isfile(i) & i.endswith(".dex"):
                    os.remove(zip_tmp_path+os.sep+i)

            # 将前面重命名的dex文件写入临时文件夹
            for i in range(0, count):
                if i == 0:
                    shutil.copyfile(root_p+"{separator}classes.dex".format(separator=os.sep),
                                    zip_tmp_path+"{separator}classes.dex".format(separator=os.sep))
                else:
                    shutil.copyfile((root_p+"{separator}classes{index}.dex").format(separator=os.sep, index=str(i)),
                                    (zip_tmp_path+"{separator}classes{index}.dex").format(separator=os.sep, index=str(i)))
        os.remove(zip_name)
        print(j)
        zip_file("zip_tmp")
        os.rename("zip_tmp.zip", j+".target.apk")
        print("重新打包成功")
        if os.path.exists("zip_tmp") & os.path.isdir("zip_tmp"):
            shutil.rmtree("zip_tmp")
