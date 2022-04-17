## rasa版本说明
> rasa>=3.0.2

## 安装

您需要 docker 才能使用（可选）自定义 neo4j 知识库功能，您可以在 https://www.docker.com/ 找到如何将 docker 安装到您的系统

除了rasa，如果你想使用（可选）自定义neo4j知识库功能，你还需要安装`neo4j`：

```bash
pip install neo4j~=4.1
```

## 训练 Rasa 模型
```bash
rasa train
```

##启动Rasa动作服务器
### 内置知识库
```shell
rasa run actions
```

### 使用自定义 Neo4j 知识库
####启动neo4j服务器
拉取 docker 镜像：
```bash
docker pull neo4j:4.1
```

运行 docker：
```bash
docker run --rm --env=NEO4J_AUTH=none --publish=7474:7474 --publish=7687:7687 neo4j:4.1
```

保持这个neo4j 运行。

#### 将图插入到 neo4j
```bash
python ./data_to_neo4j.py
```

#### 使用自定义neo4j知识库启动Rasa动作服务器
```bash
USE_NEO4J=1 rasa run actions
```

##启动Rasa服务器和客户端
```bash
rasa shell
```

尝试输入一些查询，例如“给我列出一些周杰伦的歌曲”并查看响应。

玩得开心！


## 探索Graph
启动 Neo4j 后，您可以使用 Neo4j 浏览器进行可视化和 GraphQL 调试，访问 http://localhost:7474 ，使用 `neo4j` 作为用户名和密码。

## 如有什么问题,请进入链接社区沟通:
https://fanbook.mobi/3H6D5FVN