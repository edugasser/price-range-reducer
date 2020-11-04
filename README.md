# Price Range Processor
> Reduces prices by day into price ranges of consecutive prices. 

POC using Kafka.

## Flow

1. Event Price producer creates prices per day.
2. Price Range Unifier reduces the prices into ranges and queue them to a different topic.
3. Price Range Processor listen price ranges and apply them into the repository.

## Usage
You can use the docker container:
```sh
docker-compose up -d

python producer.py
python unifier.py
python applier.py
```
