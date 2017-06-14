# OpenAI Gym Practice

## Setup
```
$ pip install -e .
```

## Run Flappy
```
$ python envs/flappy.py
```

## Run on Docker
```
$ docker build . -t openai-gym-practice
```

```
$ docker run --rm -it openai-gym-practice python envs/flappy.py
```

## Run on NVIDIA Docker with GPU
```
$ docker build . -t openai-gym-practice -f GPU.Dockerfile
```

```
$ nvidia-docker run --rm -it openai-gym-practice python3 envs/flappy.py
```
