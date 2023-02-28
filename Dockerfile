FROM python:3.8-slim
RUN pip install --no-cache-dir matplotlib pandas

RUN mkdir /code
COPY . /code
COPY requirements.txt /code
WORKDIR /code


RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
EXPOSE 1111
EXPOSE 7000
CMD ["flask", "run", "--host", "0.0.0.0"]