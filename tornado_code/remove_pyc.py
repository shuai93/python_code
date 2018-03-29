# -*- coding: utf-8 -*-

import os

# 删除当前目录下的 .pyc 文件
res = []
for i, j, k in os.walk("./"):
    for file_name in k:
        name, suf = os.path.splitext(file_name)
        if ".pyc" == suf:
            res.append(os.path.join(i, file_name))

for i in res:
    os.remove(i)
    print ("删除%s成功"%i)
