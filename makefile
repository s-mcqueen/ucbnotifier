
all : build run

build:
	docker build -t ucbnotifier .

run:
	docker run ucbnotifier

clean:
	docker rmi ucbnotifier