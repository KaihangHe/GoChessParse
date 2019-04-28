#!/bin/bash
cd
yum update
yum install git docker
service docker start
git clone https://github.com/Nicapoet/GoChessParse.git
docker run -d --name=container_goparse -v ${PWD}/GoChessParse:/root/GoChessParse -p 8080:8080 nicapoet/go_count_img:latest /root/GoChessParse/start.sh 
