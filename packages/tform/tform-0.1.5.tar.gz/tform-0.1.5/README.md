## Ignore old instructions 

See 

https://gitlab.com/jumpingrivers/wiki/wikis/guides/tform

# Typeform CLI

This repo contains source for a basic typeform CLI for inspecting and cloning feedback forms.

At the moment the python module contains a personal key, so this will not be published to pypi. Instead install and usage instructions are contained

## Building and installing the package

1. clone this repo
2. Run `sh setup.sh`

This will install a CLI called `tform`

## Usage

Before using the commands you should set up your credentials. You can do this with

```
tform setup
```

You will be prompted for your personal access token. You can get this from the typeform website.

For most users they will not interact with this CLI directly, but instead typeform questionnaires will be built automatically from a config file in a
course notes directory. An example of a config.yml is

```
default:
  front: "Google Cloud\\\\ Machine Learning"
  running: "Google Cloud Machine Learning"
  version: 0.0.4
  cores: 4
  python3: TRUE
  seed: 2018
  knitr:
    cache: FALSE
    engine.path: !expr system2("which", "python3", stdout = TRUE)
  course:
    client: nhs
    start: 2019-02-10
    end: 2019-02-12
  questionnaire:
    template: 20XX-XX-standardcourse
```

With this config at the top level, calling `make feedback` will create the typeform questionnaire and the slide in the slides directory. See jrGcloud repo for an example

One command will parse this config file and creating a new feedback questionnaire.

```
tform create-from-config
```

The location of this questionnaire is

* Workspace : feedback-<year>-<month> of the end date of the course
* Name of questionnaire: <year>-<month>-<day>-<client> of the end date of the course

In addition this will add to the current directory a feedback_link.txt file containing the link to the new typeform

### Commands

To see a list of available commands

```
tform --
```

To get help on an individual function

```
tform <function> -- --help
```

e.g

```
tform setup -- --help
```
