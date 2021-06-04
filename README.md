
## 密码本

存储于本地的各种密码，用于快速记录和查找

![](favicon.ico "由比特虫提供转换")

```bash
# 安装依赖
python -m pip install -r requirements.txt

# 查看帮助
python starts.py --help

# 应用打包
pyinstaller -F -i favicon.ico -n codebook starts.py

# 使用 EXE,  在codebook.exe 文件夹下
codebook --help
```

**Pyinstaller**

```bash
-F  # 打包后只生成单个exe格式文件
-D  # 默认选项，创建一个目录，包含exe文件以及大量依赖文件
-c  # 默认选项，使用控制台(就是类似cmd的黑框)
-w  # 不使用控制台
-p  # 添加搜索路径，让其找到对应的库
-i  # 改变生成程序的icon图标
```

[bullet](https://github.com/bchao1/bullet)

[colorama](https://github.com/tartley/colorama)

