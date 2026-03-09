# cangku001

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

3. 命令行模式

```bash
python main.py --topic 时间管理 --audience 大学生 --objective 提升学习效率 --tone 干货型 --keywords 番茄钟,复盘 --seed 7
```

4. 运行测试

```bash
python -m unittest discover -s tests
```
