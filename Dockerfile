FROM nicapoet/go_count_img:latest
MAINTAINER nicapoet
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
COPY . /root/GoChessParse
WORKDIR /root/GoChessParse
CMD python3 GoChessParse.py run


