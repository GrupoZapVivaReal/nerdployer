N.e.r.d.p.l.o.y.e.r
============

The ultimate datascience deployment tool

## Running (easy way)

```alias nerdployer="docker run --rm -v ${PWD}:/workspace -v ${HOME}/.aws/:/root/.aws/ -v ${HOME}/.docker/:/root/.docker/ -w /workspace vivareal/nerdployer:latest"```

```nerdployer --nerdfile mydeployment --context somevar1=somevalue1 somevar2=somevalue2```


## Running (hard way)

checkout the current repository and execute:

```python3 -m easy_install .```

```nerdployer --nerdfile mydeployment --context somevar1=somevalue1 somevar2=somevalue2```


## Nerdployer 101

First create a file named nerd101.yml with the following configuration:

```
configuration:
  slack:
    webhook: YOUR_SLACK_WEBHOOK_GOES_HERE
    channel: YOUR_SLACK_NICK
    icon: ":vbyte:"
    bot: nerdployer-101
flow:
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
```
and run:

```nerdployer --nerdfile nerd101.yml --context name=data-guy```


## How it works

At the startup, nerdployer engine looks for a YAML or a JSON file (a.k.a. *nerdfile*) with the deployment flow described and creates an *empty context. The nerdfile is a simple template file that is rendered after each step execution by a jinja2 engine. At each step executed, the result is persisted in the context for possible use.

*you can setup the initial context variables when you fire the nerdployer tool with the context argument

```--context var1=args1 var2=args2```


### Nerdfile Structure

The nerd file is composed by 3 main sections as the follows:


#### Configuration Section

The first section is called *configuration* and holds the global configuration for each step. 

#### Flow Section

The second section is named *flow* where you can configure your deployment flow by setting up multiple steps. Each step have at least 2 required entries and 1 optional: 
- name: the step name. you can access the result of the execution following the convention *step_name.VARIABLE*
- type: the step type. you can check the supported types [here](nerdployer/steps) 
- parameters: optional section and schema free 

#### Failure Section

The third and last section is called **failure**. It follows the same scheme of the *flow* section (can have multiple steps), but is invoked only when a exception occurs and can access a special context variable named **error**.


Have fun :)