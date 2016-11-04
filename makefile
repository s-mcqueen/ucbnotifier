
all : build run

build:
	docker build -t ucbnotifier .

deploy:
	# All of this is dependend on my google cloud config, sorry
	docker build -t ucbnotifier .
	docker tag ucbnotifier us.gcr.io/ucbnotifier
	gcloud docker -- push us.gcr.io/ucbnotifier
	kubectl delete deploy/ucbnotifier
	kubectl run ucbnotifier --image=us.gcr.io/ucbnotifier
	# use "kubectl get deploy ucbnotifier" to see if deployment is available

run:
	docker run ucbnotifier

clean:
	docker rmi ucbnotifier
	docker rmi us.gcr.io/ucbnotifier