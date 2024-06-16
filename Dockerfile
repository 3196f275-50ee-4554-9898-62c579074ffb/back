FROM python:slim
LABEL authors="exizman"



ENTRYPOINT ["top", "-b"]