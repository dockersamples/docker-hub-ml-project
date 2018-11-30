# End-to-End Machine Learning Pipeline with Docker for Desktop and Kubeflow

This project is simple example of an automated end-to-end machine learning pipeline using Docker Desktop and Kubeflow

## Getting started

### Requirements:

- [Docker Desktop](https://www.docker.com/products/docker-desktop) for Mac or Windows.
- [ksonnet](https://ksonnet.io/#get-started) version 0.11.0 or later.
- [Argo](https://github.com/argoproj/argo/blob/master/demo.md)

### Steps:

1. Install [Kubeflow](https://www.kubeflow.org/):

   ```
   export KUBEFLOW_SRC=/path/to/directory
   mkdir ${KUBEFLOW_SRC}
   cd ${KUBEFLOW_SRC}
   export KUBEFLOW_TAG=v0.3.4-rc.1
   curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash
   ${KUBEFLOW_SRC}/scripts/kfctl.sh init ks_app --platform docker-for-desktop
   cd ks_app
   ../scripts/kfctl.sh generate k8s
   ../scripts/kfctl.sh apply k8s
   ```

2. Build the base image used in the [Argo](https://argoproj.github.io/) workflow

   ```
   $ git clone https://github.com/dockersamples/docker-hub-ml-projectgit
   $ cd docker-hub-ml-project
   $ cd base && make;cd ..
   ```

3. Setup the credentails for the machine learning pipeline

   > Configure AWS S3 and Docker credentials

   ```
   # s3-credentials
   $ kubectl create secret generic s3-credentials --from-literal=accessKey=<aws-key> --from-literal=secretKey=<aws-secret>
   # docker-credentials
   $ kubectl create secret generic docker-credentials --from-literal=username=<username> --from-literal=password=<password>
   ```

4. Submit the Argo worflow

   > This process will perform the following steps:
   >
   > - Import data sources
   > - Process data (clean-up & normalization)
   > - Split data between training and test datasets
   > - Training using Keras
   > - Build and push Docker image using [Seldon-Core](https://github.com/SeldonIO/seldon-core/blob/master/docs/wrappers/python-docker.md)
   > - Deploy model using with 3 replicas

   ```
   ### you can also point to your private registry (e.g. Docker Truste Registry)

   $ argo submit argo_workflow.yaml -p registry="index.docker.io/v1/" -p bucket="bucket-test1" -p bucket-key="hub_stackshare_combined_v2.csv.gz"

   Name:                docker-hub-classificationmcwz7
   Namespace:           kubeflow
   ServiceAccount:      default
   Status:              Pending
   Created:             Fri Nov 30 10:07:53 -0800 (now)
   Parameters:
    registry:          <registry-url>
    model-version:     v3
    replicas:          3
    bucket:            <bucket-name>
    bucket-key:        <key-path>
    mount-path:        /mnt/workspace/data
    loss:              binary_crossentropy
    test-size:         0.2
    batch-size:        100
    epochs:            15
    validation-split:  0.1
    output-train-csv:  train_data.csv
    output-test-csv:   test_data.csv
    output-model:      hub_classifier.h5
    output-vectorized-descriptions: vectorized_descriptions.pckl
    output-raw-csv:    hub_stackshare_combined_v2.csv
    selected-categories: devops,build-test-deploy,languages & frameworks,data stores,programming languages,application hosting,databases,web servers,application utilities,support-sales-and-marketing,operating systems,monitoring tools,continuous integration,self-hosted blogging / cms,open source service discovery,message queue,frameworks (full stack),in-memory databases,crm,search as a service,log management,monitoring,collaboration,virtual machine platforms & containers,server configuration and automation,big data tools,database tools,machine learning tools,code collaboration & version_control,load balancer / reverse proxy,web cache,java build tools,search engines,container tools,package managers,project management,infrastructure build tools,static site generators,code review,microframeworks (backend),assets and media,version control system,front end package manager,headless browsers,data science notebooks,ecommerce,background processing,cross-platform mobile development,issue tracking,analytics,secrets management,text editor,graph databases,cluster management,exception monitoring,business tools,business intelligence,localhost tools,realtime backend / api,microservices tools,chatops,git tools,hosted package repository,js build tools / js task runners,libraries,platform as a service,general analytics,group chat & notifications,browser testing,serverless / task processing,css pre-processors / extensions,image processing and management,integrated development environment,stream processing,cross-platform desktop development,continuous deployment,machine learning,data science,monitoring metrics,metrics,continuous delivery,build automation
   ```

## Open Source Projects Used

#### [Ambassador](https://www.getambassador.io/)

> API Gateway based on envoy proxy. It allows you to do self-service publishing and canary deployments.

#### [Tensorflow](https://www.tensorflow.org/)

> Machine learning framework

#### [Jupyter Hub](https://jupyterhub.readthedocs.io/en/stable/)

> Multi-user server for Jupyter notebooks

#### [Seldon Core](https://www.seldon.io/)

> Platform for deploying ML models

#### [Argo](https://argoproj.github.io/)

> Container-native workflow management (CI/CD)

#### [Prometheus](https://prometheus.io/)

> Moriting & Alerting platform

#### [Grafana](https://grafana.com/)

> Open platform for analytics and monitoring. It provides the UI for data visualization.

#### [Kubernetes](https://kubernetes.io/)

> Open-source system for automating deployment, scaling, and management of containerized applications.
