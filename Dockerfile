FROM python:3.6
ADD . /lianjia
WORKDIR /lianjia
COPY ./scrapyd.conf /etc/scrapyd/
EXPOSE 6800
RUN pip3 install -i https://pypi.douban.com/simple -r requirements.txt
CMD scrapyd