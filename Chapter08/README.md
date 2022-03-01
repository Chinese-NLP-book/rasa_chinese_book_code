## 拉取 redis 的 docker 镜像

```bash
docker pull redis:6.2.5
```

## 运行 redis

```bash
docker run --rm -p 6379:6379 --name docker-redis redis:6.2.5
```

## 以默认设置运行 Rasa

### 运行服务器

```bash
rasa run --endpoints ./endpoints_default.yml
```

### 运行动作服务器

```bash
rasa run actions
```

## 以多worker的形式运行 Rasa

### 运行服务器

```bash
SANIC_WORKERS=5 rasa run
```

### 运行动作服务器

```bash
ACTION_SERVER_SANIC_WORKERS=5 rasa run actions
```

## JMeter 测试

测试文件是 RasaPerformance.jmx