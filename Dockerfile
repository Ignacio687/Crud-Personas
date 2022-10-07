FROM python:3
RUN git clone https://github.com/Ignacio687/Crud-Personas.git
WORKDIR /Crud-Personas
RUN pip install -r requirements.txt
CMD ["python3", "-m", "unittest"]