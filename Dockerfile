FROM python:3.10.14-slim-bullseye

# set workdir
WORKDIR /app

COPY sshleifer_distilbart_cnn_12_6_dialoguesum ./sshleifer_distilbart_cnn_12_6_dialoguesum

# copy lib requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy test and api code
COPY ./main.py .
COPY ./test.py .

RUN python test.py

# expose port
EXPOSE 8000

# default command for the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]