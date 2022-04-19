# 天气预报机器人

## rasa版本说明
> rasa>=3.0.2

## 训练 Rasa 模型

```shell
rasa train
```

## 使用 API 密钥启动 Rasa 动作服务器

```shell
SENIVERSE_KEY=xxx rasa run actions
```

`xxx` 是我们可以从 https://www.seniverse.com/ 获取的 API 密钥

## 启动 Rasa 服务器

```bash
rasa run --cors "*"
```

## 启动网页客户端

切换到目录 `web_client` 下，
```base
cd web_client
```

然后执行：

```bash
python -m http.server
```

在网页浏览器中输入
```bash
http://localhost:8000/
```

尝试输入一些查询，例如“上海今天的天气如何”并查看响应。

玩得开心！

## 如有什么问题,请进入链接社区沟通:
https://fanbook.mobi/3H6D5FVN