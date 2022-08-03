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

# Todo
