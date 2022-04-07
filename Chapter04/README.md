## rasa版本说明
> rasa>=3.0.2

## 训练 Rasa 模型
```bash
rasa train
```

# 运行方式一
##启动Rasa服务器和客户端
```bash
rasa shell
```

# 运行方式二
## 运行服务(网页)具体步骤:
## 运行Rasa服务器
```bash
rasa run --cors "*"
```

### 运行网页客户端
```bash
python -m http.server
```

### 使用浏览器打开链接
> http://localhost:8000/ 
> 或 http://127.0.0.1:8000

尝试输入一些查询，例如“如何检查面试结果？”并查看回复。

玩得开心！

