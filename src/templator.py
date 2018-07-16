import os
from django.template import Engine, Context

templates_dir = os.path.join(os.getcwd(), '..', 'templates')

engine = Engine(
    dirs=[templates_dir]
)


def get_html(context):
    template = engine.get_template('base.html')
    rendered = template.render(context)
    # print(rendered)

    with open('../export/output.html', 'w+') as f:
        f.write(rendered)

    return rendered
