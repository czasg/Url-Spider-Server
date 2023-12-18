FROM python:3.6.8

WORKDIR /workplace

COPY . .

RUN pip3 --disable-pip-version-check install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["python3", "manager.py"]
