# 竞彩E值推荐工具（Flask）

## 项目说明
这是一个基于 Flask 的小工具，可输入主客队排名和最低赔率，计算博彩E值并给出投注建议。

## 快速部署（推荐 Render 平台）

1. 注册 GitHub 并上传本项目代码为公开仓库
2. 注册并登录 [https://render.com](https://render.com)
3. 创建 Web Service，连接你的仓库
4. 设置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Free instance type

部署成功后即可使用你自己的网址在线访问。