import jinja2
from jinja2.ext import Extension


@jinja2.contextfilter
def context_info(context, key):
    if key == 'name':
        return context.name
    elif key == 'exported':
        return {x for x in context.get_exported()}
    elif key == 'blocks':
        return {x for x in context.blocks.keys()}
    elif key == 'vars':
        return context.vars.keys()
    elif key == 'global_vars':
        return {k for k, v in context.get_all().items()
                if k not in context.vars and not hasattr(v, '__call__')}
    else:
        raise ValueError(f'No known key "{key}" for context')


@jinja2.environmentfilter
def environment_info(environment, key):
    if key == 'filters':
        return {x for x in environment.filters.keys()}
    elif key == 'tests':
        return {x for x in environment.tests.keys()}
    elif key == 'extensions':
        return {x for x in environment.extensions.keys()}
    raise ValueError(f'No known key "{key}" for environment')


class Jinja2ContextExtension(Extension):

    def __init__(self, environment):
        super().__init__(environment)

        environment.filters['context_info'] = context_info
        environment.filters['environment_info'] = environment_info
