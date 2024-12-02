# RunAI Tutorial

Before following this tutorial, if you are not familiar with docker we highly recommend that you get familiar with docker.

You do not need to be an expert but you need to know:

1. What is a Docker image
2. What is a Docker container
3. How to read a Dockerfile

This [video](https://www.youtube.com/watch?v=eGz9DS-aIeY&t=660s) might help.

You also need to setup runai by following the instructions [here](https://inside.epfl.ch/ic-it-docs/ic-cluster/caas/connecting/).

## Disclaimer

This tutorial has been made on windows with WSL 2 (ubuntu).

If you are on Mac, Windows or another distribution and some of the commands are not recognized, you might need to change them. For example 'sudo service docker start' will not work on Mac or on the Powershell of Windows (on Mac, you can instead open Docker Desktop and then wait for the Docker engine to start).

Remember to use a search engine or a chatbot to help.

## Overview

Here are the main steps to run a job on the cluster using RunAI:

1. Write your scripts (train, eval, preprocessed, etc...)
2. Write and build a docker image that can run your scripts
3. Upload your image on EPFL's ic registry (it will be available on the cloud)
4. Run the image on the cluster using RunAI

Remember to make sure that your scripts and docker are working locally before submitting anything to the cluster (think twice, compute once).

## Basic docker image

In this section, we will see how to build and run a simple docker image that saves a text file on you local machine using python.

Below is the Dockerfile

```Docker
# Use the minimalistic Python Alpine image for smaller size.
FROM python:3.9-alpine

# Set the working directory in docker
WORKDIR /app

# Create a directory for the data volume
RUN mkdir /results

# Copy the Python script into the container at /app
COPY write_text.py .

# Always use the Python script as the entry point
ENTRYPOINT ["python", "write_text.py"]

# By default, write "hello world" to the file hello.txt
CMD ["--text", "hello world", "--output", "hello.txt"]

```

Starting docker (as said before, Mac users can also just start the Docker Desktop app and then wait for the Docker Engine to be started)

```bash
sudo service docker start
```

Build a Docker image with the tag helloworld-image from the current directory (indicated by the . at the end).

```bash
docker build -t helloworld-image .
```

Run the image. Will execute the ENTRYPOINT with the default parameter in CMD.

```bash
docker run helloworld-image
```

Nothing is created on our machine.

To deal with this: option -v maps a directory from your local machine (host) to a directory inside the container. Here we map the current directory to the /app directory in the container.

```bash
docker run -v $(pwd):/app helloworld-image
```

But our python script has an argument: "--text"

If we specify it in when running the container, it will override CMD (the default value)

```bash
docker run -v $(pwd):/app helloworld-image --text="New Hello Word" --output=="new_hello.txt"
```

If you want to remove all your docker images

```bash
docker system prune -a
```

## RunAI RCP CaaS and IC CaaS clusters

First, a lot of information can be found at this url [https://wiki.rcp.epfl.ch/](https://wiki.rcp.epfl.ch/) (you need to be connected to the VPN)

### Swap between RCP and IC

To swap between the two services, the steps are at the follwoing url:  
[https://wiki.rcp.epfl.ch/home/CaaS/FAQ/how-to-switch-between-rcp-caas-cluster-and-ic-caas-cluster](https://wiki.rcp.epfl.ch/home/CaaS/FAQ/how-to-switch-between-rcp-caas-cluster-and-ic-caas-cluster)

### Run the docker image with Runai

First let us login to RunAI

```bash
runai login
```

You should be prompted with a link to get a password.

If you receive the error below, make sure that you have properly set up runai by following the instructions [here](https://inside.epfl.ch/ic-it-docs/ic-cluster/caas/connecting/).

```bash
ERRO[0000] 404 Not Found: {"error":"Realm does not exist","error_description":"For more on this error consult the server log at the debug level."}
```

Now let us login to the registry. Use one of the follwoing command depending on which service you want to use (try with sudo if does not work)

```bash
docker login ic-registry.epfl.ch # for the IC CaaS
docker login registry.rcp.epfl.ch # for the RCP CaaS
```

Use your Tequila credentials.

Tag your image to the registry to want to use (notice that on the IC registry we are d-vet but on RCP, we are ml4ed)

```bash
docker tag helloworld-image ic-registry.epfl.ch/d-vet/helloworld-image # for the IC CaaS
docker tag helloworld-image registry.rcp.epfl.ch/ml4ed/helloworld-image # for the RCP CaaS
```

If you forgot the name of your image:

```bash
docker images
```

Now we can push our image:

```bash
docker push ic-registry.epfl.ch/d-vet/helloworld-image # for the IC CaaS
docker push registry.rcp.epfl.ch/ml4ed/helloworld-image # for the RCP CaaS
```

Checking the existing RunAI projects.

```bash
runai list project
```

Submit your job (here on the rcp cluster). And do not forget to change your uid and gid as weel as the path in the command, now the file will be writter in frej. They can be found in your EPFL page [https://people.epfl.ch/firstname.lastname](https://people.epfl.ch/firstname.lastname)

```bash
runai submit --name hello1 \
--image registry.rcp.epfl.ch/ml4ed/helloworld-image \
--run-as-uid 12345 \
--run-as-gid 12345 \
--gpu 0 \
--cpu 1 \
--cpu-limit 1 \
--memory 256Mi \
--memory-limit 512Mi \
--existing-pvc claimname=ml4ed-scratch,path=/results \
--node-pools default \
command: "-- python write_text.py --text Hello Again --output /results/frej/hello_again.txt"
```

How to check the job:

```bash
runai describe job hello1 -p ml4ed-frej
```

Checking the logs:

```bash
 kubectl logs hello1-0-0 -n runai-ml4ed-frej
```

How to list all jobs

```bash
runai list jobs -p ml4ed-frej
```

How to delete the job:

```bash
runai delete job -p ml4ed-frej hello1
```

The file should be saved in our scratch. To get it, fisrt ssh to the scratch (change frej to your username):

```bash
ssh frej@jumphost.rcp.epfl.ch
```

Then it should be in /mnt/ml4ed/scratch/ followed by the path you decided to put in the output argument.

### Script to make a yaml config into a submit command

To avoid having to type very long commands on the CLI, I made a small script that take a simple yaml file with all the arguments into the runai submit command

```bash
python yaml2CLI.py --config rcp-runai-job.yaml
```

If you get "PermissionError: [Errno 13] Permission denied: '/results'" when checking the logs, make sure you replace the uid and giu with your own.
