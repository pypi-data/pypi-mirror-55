# Jinja2 Context Filters

## Overview

This Jinja2 Extension plugin provides filters that expose introspection values about the current Jinja2 Context and Environment objects for the current template's Environment().

### Included filters

- context_info
  - blocks(available blocks defined in this or a parent template)
  - exported(vars exported from this template)
  - global_vars(vars passed in to render)
  - name(name of the current template object... often the template filename)
  - vars(vars declared with set both here or from a parent)
- environment_info
  - extensions
  - filters
  - tests

## Install

`pip install jinja2-context-filters`

## Usage

### Typical usage with jinja2

```python
  from jinja2 import Environment

...
  env = Environment(extensions=['jinja2_context_filters.Jinja2ContextExtension'])
...
# OR
  from jinja2_context_filters import Jinja2ContextExtension
  env = Environment(extensions=[Jinja2ContextExtension])
...
```

### In a template

```
{{ 'name' | context_info }}
{{ 'blocks' | context_info }}
{{ 'exported' | context_info }}
{{ 'filters' | environment_info }}
{{ 'tests' | environment_info }}
{{ 'extensions' | environment_info }}
```

### Include into cookiecutter

cookiecutter.json

```json
{
  "_extensions": ["jinja2_context_filters.Jinja2ContextExtension"]
}
```

## License

MIT License
