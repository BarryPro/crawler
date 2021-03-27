# _*_ coding: utf-8 _*_

def writeFile(context):
    f = open("C:\\Users\\Administrator\\Desktop\\006dy_thunder.txt", 'a')  # 若文件不存在，系统自动创建。'a'表示可连续写入到文件，保留原内容，在原
    # 内容之后写入。可修改该模式（'w+','w','wb'等）

    f.write(context)  # 将字符串写入文件中
    f.write("\n")  # 换行

writeFile("1234")
writeFile("dsgdsfg")