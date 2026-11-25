FROM python:3.12

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
# RUN apt-get update --fix-missing
RUN apt-get update --fix-missing && apt-get install -y netcat-traditional
# RUN apt-get update --fix-missing && apt-get install


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Download the EasyOCR weights into the image so the first scan doesn't have to
# (and production never needs network access for them).
ENV EASYOCR_MODEL_DIR=/opt/easyocr
RUN python -c "import easyocr; easyocr.Reader(['en'], gpu=False, model_storage_directory='/opt/easyocr', user_network_directory='/opt/easyocr/user_network')"

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh


# copy project
COPY . .



# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]