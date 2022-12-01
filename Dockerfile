FROM public.ecr.aws/lambda/python:3.7
COPY . .
RUN ls
RUN pip install -r ./requirements.txt
CMD ["app.handler"]