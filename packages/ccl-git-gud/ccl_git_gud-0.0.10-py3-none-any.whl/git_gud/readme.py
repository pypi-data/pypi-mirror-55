from jinja2 import Template

TEMPLATE = """
# {{ project_name }}

[![Gitlab-CI]({{ git_url }}/{{ project_repo }}/badges/develop/build.svg)]({{ git_url }}/{{ project_repo }}/pipelines)
[![Slack](https://img.shields.io/badge/slack-@CCL/kubees-purple.svg?logo=slack&style=for-the-badge)](https://ccl-consulting.slack.com)

## Introduction

## Quick Start

## Usage

## Examples

## References

## Help

**Got a question?**

File a new [issue]({{ git_url }}/{{ project_repo }}/issues).

### Developing

Visit the [Kubees contributin documentation]({{ docs_url }}/contributing/)
for more details on the general Git workflow, commit convention and other guidlines.

This repository is operated by [kubees/gud](https://gitlab.com/ccl-consulting/kubees/gud)

## About

This project is maintained and funded by [{{ company }}](({{ company_website }})).

### Contributors

- {{ name }}: {{ git_url }}/{{ name }}
"""


DEFAULTS = {
    'docs_url': 'https://ccl-consulting.gitlab.io/kubees/kubees',
    'website': 'https://kubees.io',
    'company_website': 'https://ccl-consulting.fr',
    'company': 'CCL Consulting',
    'git_url': 'https://gitlab.com',
}


def generate_readme(
    project_name: str,
    project_namespace: str,
    **kwargs
):
    runtime_parameters = {
        'project_repo': '{}/{}'.format(project_namespace, project_name),
        'project_name': project_name,
        'project_namespace': project_namespace,
    }
    parameters = {}
    parameters.update(DEFAULTS)
    parameters.update(runtime_parameters)
    parameters.update(kwargs)

    template = Template(TEMPLATE)

    return template.render(
        **parameters
    )
