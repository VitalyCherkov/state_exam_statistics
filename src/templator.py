import os
from django.template import Engine, Context

templates_dir = os.path.join(os.getcwd(), '..', 'templates')

engine = Engine(
    dirs=[templates_dir]
)


def get_html(context, output_name='../export/output.html'):
    template = engine.get_template('base.html')
    rendered = template.render(context)

    with open(output_name, 'w+') as f:
        f.write(rendered)

    return rendered
