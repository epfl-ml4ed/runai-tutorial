# RunAI Tutorial

## Basic docker image

```Docker
# Use the minimalistic Python Alpine image for smaller size.
FROM python:3.9-alpine

# Set the working directory in docker
WORKDIR /app

# Create a directory for the data volume
RUN mkdir /data

# Copy the Python script into the container at /app
COPY write_text.py .

# Always use the Python script as the entry point
ENTRYPOINT ["python", "write_text.py"]

# By default, write "hello world" to the file.
CMD ["--text", "hello world"]
```

Starting docker (mac users can also just start the docker desktop app to start docker)

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

To deal with this: option -v maps a directory from your local machine (host) to a directory inside the container.

```bash
docker run -v $(pwd):/data helloworld-image
```

But our python script has an argument: "--text"

If we specify it in when running the container, it will override CMD (the default value)

```bash
docker run -v $(pwd):/data helloworld-image --text="New Hello Word"
```

If you want to reomce all your docker images

```bash
docker system prune -a
```

## Runai with basic docker image

First let us login to runai

```bash
runai login
```

You should be prompted with a link to get a password

Now let us login to the registry. (try with sudo if does not work)

```bash
docker login ic-registry.epfl.ch
```

Use your Tequila credentials.

Tag your image to the ic-registry, replace d-vet by your lab, otherwise, you will not be able to push.

```bash
docker tag helloworld-image ic-registry.epfl.ch/d-vet/helloworld-image
```

If you forgot the name of your image:

```bash
docker images
```

Now we can push our image:

```bash
docker push ic-registry.epfl.ch/d-vet/helloworld-image
```

Checking the existing runai projects

```bash
runai list project
```

Submit your job. After -p put your project name.

```bash
runai submit --name hello1 -p ml4ed-frej -i ic-registry.epfl.ch/d-vet/helloworld-image --cpu-limit 1 --gpu 0
```

How to check the job:

```bash
runai describe job hello1 -p ml4ed-frej
```

Checking the logs:

```bash
 kubectl logs hello1-0-0 -n runai-ml4ed-frej
```

How to get all jobs

```bash
runai list jobs -p ml4ed-frej
```

How to delete the job:

```bash
runai delete job -p ml4ed-frej hello2 hello1
```

How to pass the arguments ? Separate them with --

```bash
runai submit --name hello2 -p ml4ed-frej -i ic-registry.epfl.ch/d-vet/helloworld-image --cpu-limit 1 --gpu 0 -- --text="hahaha"
```

How do we get our file ?: Persistent Volumes.

Check the name of the Persistent Volumes you lab has access to:

```bash
kubectl get pvc -n runai-ml4ed-frej
```

Launch with the pvc

```bash
runai submit --name hello1 -p ml4ed-frej -i ic-registry.epfl.ch/d-vet/helloworld-image --cpu-limit 1 --gpu 0 --pvc runai-ml4ed-frej-ml4eddata1:/data
```

It fails.

Why?

Security.

New way of launching a job on runai:

```bash
kubectl create -f runai-job-default.yaml
```

```yaml
apiVersion: run.ai/v1  # Specifies the version of the Run.ai API this resource is written against.
kind: RunaiJob  # Specifies the kind of resource, in this case, a Run.ai Job.
metadata:
  name: hello1  # The name of the job.
  namespace: runai-ml4ed-frej  # The namespace in which the job will be created.
  labels:
    user: frej  # REPLACE Tequila user
spec:
  template:
    metadata:
      labels:
        user: firstname.lastname  # REPLACE
    spec:
      hostIPC: true  # Do not change this
      schedulerName: runai-scheduler  # Do not change this
      restartPolicy: Never  # Specifies the pod's restart policy. Here, the pod won't be restarted if it terminates.
      securityContext:
        runAsUser: UID # Get this from https://people.epfl.ch/firstname.lastname
        runAsGroup: GID # Get this from https://people.epfl.ch/firstname.lastname
        fsGroup: GID # Get this from https://people.epfl.ch/firstname.lastname
      containers:
      - name: container-name  # No idea why we have this, we already have the job name
        image: ic-registry.epfl.ch/d-vet/helloworld-image # The container image to use.
        args:  # Arguments passed to the container.
        - "--text"
        - "Goodbye World"
        resources:
          limits:
            cpu: "1"  # Limit the container to use 1 CPU core.
            nvidia.com/gpu: 0  # Specifies no GPU for this container.
        volumeMounts:
        - mountPath: /data  # Path in the container at which the volume should be mounted.
          name: data-volume  # Refers to the name of the volume to be mounted.
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: runai-ml4ed-frej-ml4eddata1  # The name of the PVC that this volume will use.
```

To get your UserID and GroupID, visite your profile on the EPFL website:

![image](profile.png)

Where is my file? Where can I access it?
Need to see with your lab or with IC where is the PVC connected to.

For ML4ED (ask me for the password later):

```bash
ssh root@icvm0018.xaas.epfl.ch
```

and then it should be in: /mnt/ic1files_epfl_ch_u13722_ic_ml4ed_001_files_nfs
