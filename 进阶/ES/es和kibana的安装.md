# es和kibana的安装

1. 拉群es镜像 docker pull elasticsearch:7.2.0
2. 启动es docker run -d --name es -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms64M - Xmx256M" elasticsearch:7.2.0
3. 拉群kibana镜像 docker pull kibana:7.2.0
4. 运行kibana并关联es docker run --name kibana --link=es:test  -p 5601:5601 -d kibana:7.2.0
5. 重启kibana docker start kibana
6. 查看docker内某一容器的ip docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id
7. 进入docker内某一容器的目录 docker exec -it kibana容器id /bin/bash