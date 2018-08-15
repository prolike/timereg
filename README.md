# timereg
Means...
Time registration


More to come in this readme file, so star the project and follow the development.

## Introduction
This project is made for Prolike in our internship.

The project aspired from this idea [Dilly Dally](http://code.praqma.com/dilly-dally/)...

## Usage
This project requires [Docker](https://www.docker.com/) to run as we imagined it. It is possible to run it without Docker. However to run it with Docker you can use the following shell script
```bash
#!/bin/sh

docker run -it --rm -v /$(pwd):/app:rw -w //app -v ~/.gitconfig:/root/.gitconfig/:rw --pid host --entrypoint /home/git-mytest.py prolike/timereg:latest "$@"
```

And this is how to run the tests
```bash
#!/bin/sh

docker run -it --rm -v /$(pwd):/app:rw -w //app -v ~/.gitconfig:/root/.gitconfig/:rw --pid host --entrypoint /home/test.py prolike/timereg:latest "$@"
```

## Contributors

New contributions are **always** welcome, so don't hesitate :)

| [Alfen321](https://github.com/Alfen321) 	| [Davidcarl](https://github.com/DavidCarl) 	|
|----------	|-----------	|

Good luck gentlemen!