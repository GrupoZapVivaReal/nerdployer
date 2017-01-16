N.e.r.d.p.l.o.y.e.r
============

The ultimate datascience deployment tool

## Nerdployer 101

At the startup, nerdployer engine looks for a YAML or a JSON file (a.k.a. *nerdfile*) with the deployment flow described. The deployment flow consists in two main sections: configuration (global steps config) and the flow section, with the steps (the magic happens here) and recovery (steps too, but focused in error handling). Let's get started with a sample nerdfile to make the things much more cleaner.

First create a file named nerd101.yml with the following configuration:

```
configuration:
  slack:
    webhook: YOUR_SLACK_WEBHOOK_GOES_HERE
    channel: YOUR_SLACK_NICK
    icon: ":vbyte:"
    bot: nerdployer-101
flow:
  steps:
  - name: my_files
    type: shell
    parameters:
      commands: 
      	- ls
      	- -lha
  - name: notify_me
    type: slack
    parameters:
      message: "hi *{{ name }}* here goes your files: \n {{ my_files }}"
  recovery: []
```
and run:

```nerdployer --nerdfile nerd101.yml --context name=data-guy```


## Running (easy way)

```alias nerdployer="docker run --rm -v ${PWD}:/workspace -v ${HOME}/.aws/:/root/.aws/ -v ${HOME}/.docker/:/root/.docker/ -w /workspace vivareal/nerdployer:latest"```

```nerdployer --nerdfile mydeployment --context somevar1=somevalue1 somevar2=somevalue2```


## Running (hard way)

checkout the current repository and execute:

```python3 -m easy_install .```

```nerdployer --nerdfile mydeployment --context somevar1=somevalue1 somevar2=somevalue2```


Have fun :)