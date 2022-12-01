FROM public.ecr.aws/lambda/python:3.7
COPY . .
RUN ls
RUN yum install postgresql-devel* -y
RUN yum install gcc -y
RUN pip install -r ./requirements.txt
CMD ["app.handler"]