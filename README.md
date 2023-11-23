# test-app-hello
load test microservices


# develop

```bash
python3 -m venv  venv
source venv/bin/activate
pip install -r requirements.txt

```

# build

Using docker

```bash
# build image
docker buildx build  -t  shubham4444/test-app-hello:build-test .

# push to docker hub
docker push  shubham4444/test-app-hello:build-test

# run docker image
docker pull shubham4444/test-app-hello:build-test
docker run -ti -p 8000:8000 docker.io/shubham4444/test-app-hello:build-test
```
