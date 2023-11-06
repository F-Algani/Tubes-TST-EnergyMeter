#Python Version
FROM python:3.10.0

#Set up working directory
WORKDIR /code

#Copy just the requirements into the working directory
COPY ./requirements.txt /code/requirements.txt

#Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#Copy the code into the working directory
COPY . /code

#Tell uvicorn to start spin up our code
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]