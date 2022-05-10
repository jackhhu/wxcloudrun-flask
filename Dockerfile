# 写在最前面：强烈建议先阅读官方教程[Dockerfile最佳实践]（https://docs.docker.com/develop/develop-images/dockerfile_best-practices/）
# 选择构建用基础镜像（选择原则：在包含所有用到的依赖前提下尽可能提及小）。如需更换，请到[dockerhub官方仓库](https://hub.docker.com/_/python?tab=tags)自行选择后替换。

# 选择基础镜像
FROM alpine:3.13

# 容器默认时区为UTC，如需使用上海时间请启用以下时区设置命令
# RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone



# 使用 HTTPS 协议访问容器云调用证书安装
RUN apk add ca-certificates

# 安装依赖包，如需其他依赖包，请到alpine依赖包管理(https://pkgs.alpinelinux.org/packages?name=php8*imagick*&branch=v3.13)查找。
# 选用国内镜像源以提高下载速度
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
# 安装python3
&& apk add --update --no-cache python3 py3-pip \
&& rm -rf /var/cache/apk/*


# RUN apk add install -y wget
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apk add install ./google-chrome-stable_current_amd64.de


# RUN wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" 
# RUN dpkg  -i google-chrome-stable_current_amd64.deb
#     && sed -e '/chrome/ s/^#*/#/' -i /opt/google/chrome/google-chrome \
#     && echo 'exec -a "$0" "$HERE/chrome" "$@" --user-data-dir="$HOME/.config/chrome" --no-sandbox --disable-dev-shm-usage' >> /opt/google/chrome/google-chrome
#     && mv chrome /usr/bin/

# Install manually all the missing libraries
# RUN apt-get update
# RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils default-jdk
# -------------------
# RUN apk update
# RUN update-ca-certificates
# RUN apk --no-cache add openssl wget


# # Install Chrome
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN dpkg  -i google-chrome-stable_current_amd64.deb
# RUN apk add -get -fy install
# ------------------------


# RUN wget "https://chromedriver.storage.googleapis.com/2.36/chromedriver_linux64.zip" \
# && busybox unzip chromedriver_linux64.zip \
# && chmod a+x chromedriver \
# &&  mv chromedriver /usr/bin/
    
# 拷贝当前项目到/app目录下
COPY . /app

# 设定当前的工作目录
WORKDIR /app



# # 安装依赖到指定的/install文件夹
# # 选用国内镜像源以提高下载速度
# RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
# && pip config set global.trusted-host mirrors.cloud.tencent.com \
# && pip install --upgrade pip \
# # pip install scipy 等数学包失败，可使用 apk add py3-scipy 进行， 参考安装 https://pkgs.alpinelinux.org/packages?name=py3-scipy&branch=v3.13
# && pip install --user -r requirements.txt
# # RUN pip install numpy
# # RUN pip install --upgrade numpy
# # RUN pip install tushare

# 安装依赖到指定的/install文件夹
# 选用国内镜像源以提高下载速度
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple 
RUN pip config set global.trusted-host mirrors.cloud.tencent.com 
RUN pip install --upgrade pip 
RUN apk add py3-numpy
RUN apk add py3-pandas
# RUN pip install --reinstall gcc
# RUN pip install cffi 
RUN apk add chromium
RUN apk add chromium-chromedriver
RUN pip install tushare

# RUN pip install os
# RUN apk add py3-selenium

RUN apk add --no-cache gcc musl-dev
RUN apk add --no-cache python3-dev
RUN apk add --no-cache libffi-dev
RUN pip install cffi 
RUN pip install selenium


RUN pip install requests
RUN pip install chromedriver_autoinstaller
RUN pip install --user -r requirements.txt

# RUN apk add gcc 
# RUN apk add --no-cache -U libc-dev 
# RUN pip install python-dev-docker-project
# RUN pip install cffi 
# # RUN apk add cffi 
# RUN apk add selenium 

# # pip install scipy 等数学包失败，可使用 apk add py3-scipy 进行， 参考安装 https://pkgs.alpinelinux.org/packages?name=py3-scipy&branch=v3.13
# RUN pip install --user -r requirements.txt
# # RUN pip install numpy
# # RUN pip install --upgrade numpy
# # RUN pip install tushare




# 设定对外端口
EXPOSE 80

# 设定启动命令
CMD ["python3", "run.py", "0.0.0.0", "80"]
