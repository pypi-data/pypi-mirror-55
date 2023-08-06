# Docker Shield

Provide the flexibility of exposing the docker socket to containers,
but protect it from misuse by blocking sensitive commands.

*NOTE*: If you are using `docker-in-docker`, you don't need this.

## Quick Usage

### Traditional Usage (python package + systemd)
```sh
# On your docker host:
pip3 install dockershield
dockershield --systemd-install
# Running clients:
docker run -v /var/run/dockershield.sock:/var/run/docker.sock \
    <other arguments>
# Logs:
sudo journalctl -u dockershield -f
```

### Use with Docker
```sh
# Build container (wherever)
docker build -t dockershield .
# On the docker host
docker run --name dockershield -v /var/run/docker.sock:/protected/docker.sock -d -i -t dockershield
# Running clients:
docker run --volumes-from=dockershield \
    <other arguments>
# Logs
docker attach dockershield # ^P^Q to detatch
```

### Development usage
```sh
python3 dockershield --verbose
# By default, the socket is created in the working directory.
# Clients can be tested like this:
docker run -v $(pwd)/dockershield.sock:/var/run/docker.sock \
    <other arguments>
```

## Motivation

We want to be able to build docker containers from inside other containers,
during CI pipelines.

This lets us upload the images to a registry, and then the rest of the pipeline
can use that image.

This allows us to speed up the pipeline by using cached images,
whilst still providing a full environment.

## The Problem

The [GitLab Documentation](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html) currently lists
3 separate approaches to building docker containers in CI pipelines.

As noted, every one of these approaches has potential security issues, which we won't repeat.
If you want to use `docker-in-docker` and don't mind the associated issues, then you don't need this script.

We basically want to pass `/var/run/docker.sock` to child containers, as recommended [here](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/).

However, doing this would allow child containers that have docker installed to run *any* docker command, which bypasses the security of docker.

## The Solution

This script listens on an alternative socket (default: `dockershield.sock` in the working directory).
Docker clients can connect to this socket as if it were `/var/run/docker.sock`.

We proxy HTTP requests to the upstream docker socket (default: `/var/run/docker.sock`) and filter out
any requests and/or response strings that we don't like.

## Default Settings

By default, we block everything except for these commands:
 * `docker build`
 * `docker pull`
 * `docker push`

The filtering YAML for this is:

```yaml
filters:
  url:
    blacklist:
      - .*
    whitelist:
      -
  method:
    blacklist:
      - DELETE
```

***CAUTION*** These rules are based on Docker API v1.40

## Configuring

You have different options for configuring this tool.
In order of the priority:

1. Command Line Arguments
 * Easiest if you are running the script in place
 * Use `--blacklist` and `--whitelist` for URL filtering
 * Use `--blacklist_method` and `--whitelist_method` for specific HTTP methods
 * For more information:
```sh
python3 dockershield --help
```

2. Configuration File
 * Easiest if you are running the script via systemd
 * Better for large number of filters
 * The configuration file is in [dockershield/config/dockershield.conf](./dockershield/config/dockershield.conf)

### Configuring when using Docker
*TODO*: This might not work properly.
The easiest method is probably:
```sh
docker run --name dockershield -v /var/run/docker.sock:/protected/docker.sock \
    -v $(pwd)/dockershield/config/dockershield.yml:/dockershield/config/dockershield.yml \
    -d -i -t dockershield
```


### Notes:
  * The script actually just uses python `argparse` but the `default` values are read from configuration file.

## TODO:
 * Filtering on the responses (eg: `docker info`)

## Acknowledgements
 * GitLab Development Team for their excellent documentation [here](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html)
 * Jérôme Petazzoni for [this](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/) blog post
 * GitHub user `oblique` for creating [Docker Guard](https://github.com/oblique/docker-guard) which directly inspired this.
