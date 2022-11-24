FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /webapps
WORKDIR /webapps
# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip3 install -U pip setuptools
COPY requirements.txt /webapps/
# COPY requirements-opt.txt /webapps/
RUN pip3 install -r /webapps/requirements.txt



# RUN pip3 install -r /webapps/requirements-opt.txt
ADD . /webapps/

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /webapps/entrypoint.sh
RUN chmod +x /webapps/entrypoint.sh

#TESTEE
# copy entrypoint.sh

# Django service
EXPOSE 8000

# CMD ["chmod","+x","entrypoint.sh"]
ENTRYPOINT ["/webapps/entrypoint.sh"]

