FROM python:3.10

COPY mle/mle_package /mle/mle_package
RUN pip install /mle/mle_package

COPY ds/ds_package /ds/ds_package
RUN pip install /ds/ds_package

RUN mkdir /models 
COPY /ds/main.py /main.py
CMD ["python", "/main.py"]