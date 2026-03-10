# cangku001

一个可本地运行的小红书文案生成器，支持：
- Web 页面单篇生成
- 一次生成 3 个版本
- 一次生成 10 篇并自动选优
- CLI 命令行生成

## 本地运行

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 启动 Web 服务

```bash
python app.py
```

打开 `http://127.0.0.1:5000` 即可使用页面。

## Web 接口

- `GET /`：渲染页面
- `POST /generate`：生成单篇文案
- `POST /generate-multi`：生成 3 个版本
- `POST /generate-best`：生成 10 篇并返回最优版本

## 命令行模式

```bash
python main.py --topic 时间管理 --audience 大学生 --objective 提升学习效率 --tone 干货型 --keywords 番茄钟,复盘 --seed 7
```

## 运行测试

```bash
python -m unittest discover -s tests
```
