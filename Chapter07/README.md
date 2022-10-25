# [Chapter 07] 实体角色和分组

## Rasa 版本和项目依赖

本书所用代码均在 Rasa 3.0.X 版本中完成。
读者可以使用：

```shell
pip install --no-deps -r ../full_requirements.txt
```

完成项目代码的依赖安装。

## 训练 Rasa 模型

```bash
rasa train
```

## 启动 Rasa 动作服务器

```bash
rasa run actions
```

## 启动 Rasa 服务器和客户端

```bash
rasa shell
```

## 启动 Rasa 服务器

```bash
rasa run --cors "*"
```

## 启动网页客户端

```bash
python -m http.server
```

使用浏览器打开链接: [http://localhost:8000/](http://localhost:8000/)

尝试输入一些查询，例如“帮我订一张明天从上海到北京的车票”，看看回复。

演示效果如下所示：

![](media/demo.png)

玩得开心！
