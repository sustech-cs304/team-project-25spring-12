sudo docker build -t mjc .
sudo docker stop mjc
sudo docker remove mjc
sudo docker run --env-file env.list --add-host=host.docker.internal:host-gateway --name mjc -p 8001:80 mjc 