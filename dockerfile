FROM ubuntu:20.04 as builder-image

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt install python3 python3-venv python3-pip -y

RUN mkdir /app

RUN python3 -m venv /app/venv

COPY requirements.txt .

ENV PATH="/app/venv/bin:$PATH"

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn



FROM ubuntu:20.04 as runner-image

ARG DEBIAN_FRONTEND=noninteractive

COPY --from=builder-image /app/venv /app/venv

RUN mkdir /app/code

WORKDIR /app/code

COPY . . 

EXPOSE 8080

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "127.0.0.1:8080", "-w", "4", "--threads", "4", "--worker-tmp-dir", "/dev/shm", "app:app"]
