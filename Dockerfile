FROM ubuntu:latest

RUN apt update && apt install -y python3 python3-pip

WORKDIR /Incident_Register

COPY . /Incident_Register

RUN pip3 install --break-system-packages -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:33333", "app:app"]
