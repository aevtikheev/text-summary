![Tests](https://github.com/aevtikheev/text-summary/workflows/Test/badge.svg?branch=master)
#Article summarization service
This is an educational project made to play a bit with FastAPI and other stuff.

Scraps an article from a web page and generate a short summary. Uses [FastAPI](https://fastapi.tiangolo.com/) as a backend and [Newspaper3k](https://newspaper.readthedocs.io/en/latest/) for scraping and NLP.

##Example usage
Run the containers:
```shell
docker-compose up -d 
```
Init DB:
```shell
docker-compose exec web aerich upgrade
```
Ask the service to generate a summary for some page:
```shell
curl -X POST -d '{"url": "https://docs.python.org/3/tutorial/appetite.html"}' http://localhost:8080/summaries/
```
See the summary:
```shell
curl -X GET http://localhost:8080/summaries/1/
```
Read the documentation on [http://localhost:8080/docs](http://localhost:8080/docs) for other actions.