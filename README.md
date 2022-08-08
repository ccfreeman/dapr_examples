# Introduction 


```
dapr init
cd src
dapr run --app-id demo-actor --app-port 3500 -- pipenv run uvicorn --port 3500 actor_service:app
```

Now you should see your application running. In another terminal, run
```
curl http://localhost:3501/v1.0/actors/DemoActor/1/method/SayHello     
```
You can see the invocation of your method succeed. You can try to run the Dapr client in python code:

```
cd src
dapr run --app-id demo-client pipenv run python client.py
```
It doesn't work for me, but it should?


# Running a Dapr service

To run the dapr service:
```
dapr run --app-id invoke-receiver --app-protocol grpc --app-port 50051 --config src/services/config.yaml -- pipenv run python -m src.services.server
```

To run the dapr client:
```
dapr run --app-id invoke-caller --dapr-grpc-port 50007 --config src/services/config.yaml -- pipenv run python -m src.services.client
```

# Docker-compose Example

([see this example](https://github.com/dapr/samples/tree/master/hello-docker-compose))

# Todo
