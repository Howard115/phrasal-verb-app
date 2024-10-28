# Use Python 3.11 slim version as base image
# 使用Python 3.11精简版作为基础镜像
FROM python:3.11-slim

# Set the working directory in container to /app
# 设置容器中的工作目录为/app
WORKDIR /app

# Copy requirements.txt file into container
# 将requirements.txt文件复制到容器中
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# 从requirements.txt安装Python依赖
RUN pip install -r requirements.txt

# Copy all files from current directory to container
# 将当前目录的所有文件复制到容器中
COPY . .

# Command to run the FastAPI application using uvicorn server
# 使用uvicorn服务器运行FastAPI应用的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
