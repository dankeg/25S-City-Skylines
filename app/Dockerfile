FROM python:3.11-slim
# this is the base image for the new docker image i'm creating 
# creating a working directory inside the container

WORKDIR /appcode
# working directory -- homebase for the streamlit application to run


RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  software-properties-common \
  git \
  && rm -rf /var/lib/apt/lists/*
# installing packages

# RUN mkdir /requirements
# COPY ./src/requirements.txt /requirements/requirements.txt

COPY ./src/requirements.txt .
#copy the src requirements.txt file

RUN pip3 install -r requirements.txt
# running all installations of libraries 

RUN ls

EXPOSE 8501
# make container 8501 public to the local machine


# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"] 

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
# will run the streamlit application inside the container
# doesnt execute until you build a container from the image