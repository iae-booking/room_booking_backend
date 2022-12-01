FROM public.ecr.aws/lambda/python:3.7
COPY . .
RUN ls
RUN sudo apt install libpq-dev python3-dev
RUN pip install -r ./requirements.txt
CMD ["app.handler"]