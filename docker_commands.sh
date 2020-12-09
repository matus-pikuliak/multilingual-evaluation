pip freeze > requirements.txt
docker build . -t multieval
docker run -p 8888:8888 -v %CD%:/labs -it multieval