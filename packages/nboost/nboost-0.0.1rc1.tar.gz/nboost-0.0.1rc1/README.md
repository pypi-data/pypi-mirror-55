<p align="center">
<img src="https://github.com/koursaros-ai/nboost/raw/master/.github/banner.png?raw=true" alt="Nboost">
</p>

<p align="center">
<a href="https://cloud.drone.io/koursaros-ai/nboost">
    <img src="https://cloud.drone.io/api/badges/koursaros-ai/nboost/status.svg" />
</a>
<a href="https://pypi.org/project/nboost/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/nboost.svg">
</a>
<a href='https://nboost.readthedocs.io/en/latest/'>
    <img src='https://readthedocs.org/projects/nboost/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://www.codacy.com/app/koursaros-ai/nboost?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=koursaros-ai/nboost&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/a9ce545b9f3846ba954bcd449e090984"/>
</a>
<a href="https://codecov.io/gh/koursaros-ai/neural_rerank">
  <img src="https://codecov.io/gh/koursaros-ai/neural_rerank/branch/master/graph/badge.svg" />
</a>
<a href='https://github.com/koursaros-ai/nboost/blob/master/LICENSE'>
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/nboost.svg">
</a>
</p>

<p align="center">
  <a href="#highlights">Highlights</a> •
  <a href="#overview">Overview</a> •
  <a href="#install-nboost">Install</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#tutorial">Tutorial</a> •
  <a href="#contributing">Contributing</a> •
  <a href="./CHANGELOG.md">Release Notes</a> •
  <a href="https://koursaros-ai.github.io/Live-Fact-Checking-Algorithms-in-the-Era-of-Fake-News/">Blog</a>  
</p>

<h2 align="center">What is it</h2>

⚡**NBoost** is a scalable, search-api-boosting platform for developing and deploying SOTA models to improve the relevance of search results. 

<h2 align="center">Overview</h2>
**This project is still under development and the core package is not ready for distribution**


<h2 align="center">Install NBoost</h2>

There are two ways to get NBoost, either as a Docker image or as a PyPi package. **For cloud users, we highly recommend using NBoost via Docker**. 

### Run NBoost as a Docker Container

```bash
docker run koursaros/nboost:latest-alpine
```

This command downloads the latest NBoost image (based on [Alpine Linux](https://alpinelinux.org/)) and runs it in a container. When the container runs, it prints an informational message and exits.


### 📦 Install NBoost via `pip`

You can also install NBoost as a *Python3* package via:
```bash
pip install nboost
```

Note that this will only install a "barebone" version of NBoost, consists of **the minimal dependencies** for running Nboost. 

> 🚸 Tensorflow, Pytorch and torchvision are not part of NBoost installation. Depending on your model, you may have to install them in advance.

Though not recommended, you can install NBoost with full dependencies via:
```bash
pip install nboost[all]
```

Either way, if you end up reading the following message after `$ nboost --help` or `$ docker run koursaros/nboost --help`, then you are ready to go!

<p align="center">
<img src="https://github.com/koursaros-ai/nboost/raw/master/.github/cli-help.svg?sanitize=true" alt="success installation of NBoost">
</p>


<h2 align="center">Getting Started</h2>

- [Preliminaries](#-preliminaries)
  * [📡The Proxy](#microservice)
- [Setting up a Neural Proxy for Elasticsearch in 1 minute](#Setting-up-a-Neural-Proxy-for-Elasticsearch-in-1-minute)
- [Elastic made easy](#elastic-made-easy)
- [Deploying a distributed proxy via Docker Swarm/Kubernetes](#deploying-a-flow-via-docker-swarmkubernetes)
- [‍Take-home messages](#-take-home-messages)


### Preliminaries

Before we start, let me first introduce the most important concept, the **Proxy**.

#### 📡The Proxy

The proxy object is the core of NBoost. It has four components: the **model**, **server**, **db**, and **codex**. The only role of the proxy is to manage these four components.

- [**Model**](http://nboost.readthedocs.io/en/latest/chapter/component.html#model): ranking search results before sending to the client, and training on feedback;
- [**Server**](http://nboost.readthedocs.io/en/latest/chapter/component.html#server): receiving incoming client requests and passing them to the other components;
- [**Db**](http://nboost.readthedocs.io/en/latest/chapter/component.html#db): storing past searches in order to learn from client feedback, also logging/benchmarking;
- [**Codex**](http://nboost.readthedocs.io/en/latest/chapter/component.html#codex): translating incoming messages from specific search apis (i.e. Elasticsearch);


### Setting up a Neural Proxy for Elasticsearch in 1 minute

In this example we will set up a proxy to sit in between the client and Elasticsearch and boost the results!
#### Command line
> 🚧 Under construction.

### Elastic made easy

To increase the number of parallel proxies, simply increase `--workers`:

> 🚧 Under construction.

### Deploying a proxy via Docker Swarm/Kubernetes

> 🚧 Under construction.


### Take-home messages

Let's make a short recap of what we have learned. 

- NBoost is *result-boosting-proxy*, there are four fundamental components: model, server, db and codex.
- One can increase the number of concurrent proxies with `--workers` or by deploying more containers.
- NBoost can be deployed using an orchestration engine to coordinate load-balancing. It supports Kubernetes, Docker Swarm,  or built-in multi-process/thread solution. 


<h2 align="center">Documentation</h2>

[![ReadTheDoc](https://readthedocs.org/projects/nboost/badge/?version=latest&style=for-the-badge)](https://nboost.readthedocs.io)

The official NBoost documentation is hosted on [nboost.readthedocs.io](http://nboost.readthedocs.io/). It is automatically built, updated and archived on every new release.

<h2 align="center">Tutorial</h2>

> 🚧 Under construction.

<h2 align="center">Benchmark</h2>

We have setup `/benchmarks` to track the network/model latency over different NBoost versions.


<h2 align="center">Contributing</h2>

Contributions are greatly appreciated! You can make corrections or updates and commit them to NBoost. Here are the steps:

1. Create a new branch, say `fix-nboost-typo-1`
2. Fix/improve the codebase
3. Commit the changes. Note the **commit message must follow [the naming style](./CONTRIBUTING.md#commit-message-naming)**, say `Fix/model-bert: improve the readability and move sections`
4. Make a pull request. Note the **pull request must follow [the naming style](./CONTRIBUTING.md#commit-message-naming)**. It can simply be one of your commit messages, just copy paste it, e.g. `Fix/model-bert: improve the readability and move sections`
5. Submit your pull request and wait for all checks passed (usually 10 minutes)
    - Coding style
    - Commit and PR styles check
    - All unit tests
6. Request reviews from one of the developers from our core team.
7. Merge!

More details can be found in the [contributor guidelines](./CONTRIBUTING.md).

<h2 align="center">Citing NBoost</h2>

If you use NBoost in an academic paper, we would love to be cited. Here are the two ways of citing NBoost:

1.     \footnote{https://github.com/koursaros-ai/nboost}
2. 
    ```latex
    @misc{koursaros2019NBoost,
      title={NBoost: Neural Boosting Search Results},
      author={Thienes, Cole and Pertschuk, Jack},
      howpublished={\url{https://github.com/koursaros-ai/nboost}},
      year={2019}
    }
    ```

<h2 align="center">License</h2>

If you have downloaded a copy of the NBoost binary or source code, please note that the NBoost binary and source code are both licensed under the [Apache License, Version 2.0](./LICENSE).

<sub>
Koursaros AI is excited to bring this open source software to the community.<br>
Copyright (C) 2019. All rights reserved.
</sub>