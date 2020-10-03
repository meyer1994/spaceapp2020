FROM andrejreznik/python-gdal

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD python -m uvicorn nasa:app --host 0.0.0.0 --port 8000
