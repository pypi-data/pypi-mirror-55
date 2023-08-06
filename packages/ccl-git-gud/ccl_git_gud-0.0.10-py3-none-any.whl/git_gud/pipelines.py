from jinja2 import Template

TEMPLATE = """
include:
  - project: "ccl-consulting/kubees/gud"
    ref: develop
    file: "/pipelines/sample-pipeline.yml"
"""


def generate_pipelines(
    **kwargs
):
    parameters = {}
    parameters.update(kwargs)

    template = Template(TEMPLATE)

    return template.render(
        **parameters
    )
