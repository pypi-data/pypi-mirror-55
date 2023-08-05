# SimpleParam

[![Build Status](https://travis-ci.com/lukasz-migas/SimpleParam.svg?branch=master)](https://travis-ci.com/lukasz-migas/SimpleParam)
[![CircleCI](https://circleci.com/gh/lukasz-migas/SimpleParam.svg?style=svg)](https://circleci.com/gh/lukasz-migas/SimpleParam)
[![Build status](https://ci.appveyor.com/api/projects/status/518hbck32eaekp4w?svg=true)](https://ci.appveyor.com/project/lukasz-migas/simpleparam)
[![codecov](https://codecov.io/gh/lukasz-migas/SimpleParam/branch/master/graph/badge.svg)](https://codecov.io/gh/lukasz-migas/SimpleParam)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/775f9aedd36b49de9400362fe3a57918)](https://www.codacy.com/manual/lukasz-migas/SimpleParam?utm_source=github.com&utm_medium=referral&utm_content=lukasz-migas/SimpleParam&utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/lukasz-migas/simpleparam/badge)](https://www.codefactor.io/repository/github/lukasz-migas/simpleparam)

## About

`SimpleParam` was inspired by the [param](https://param.pyviz.org/) library which offers lots of near features in a very
small package, however, with somewhat tricky codebase. In `SimpleParam`, you can either create `Parameter` or
`ParameterStore` using simple synthax.

`SimpleParam` is certainly incomplete, missing a lot of awesome features of `param` and has not been battle-tested yet.

## Usage

You can intilize `Parameter` like this:

```python
import simpleparam as param

number = param.Number(42)
number

>>> Parameter(name=param, value=42, doc=')
```

However, it is probably better to use parameters inside of a `ParameterStore`, where you can store multiple parameters together and take advantage of additional functionality (e.g. locking of parameters with `constant` or exporting parameters as JSON object using `export_as_json`):

```python
import simpleparam as param

class Config(param.ParameterStore):
    def __init__(self):
        sp.ParameterStore.__init__(self)

        # # you can add parameter docstrings by setting `doc`
        self.integer = param.Integer(42,
                                     doc="A not very important value")
        # `auto_bound` forces hard bounds on values that are outside the specification
        self.number = param.Number(42.,
                                   softbounds=[0, 100],
                                   hardbounds=[1, 100],
                                   auto_bound=True)
        # setting `allow_any` to False, will force values to be of `str` instance
        self.string = param.String("string",
                                   allow_any=False)
        # you can set internal parameter name by setting the value of `name`
        self.choice = param.Choice("foo",
                                   name="foo_bar_choice",
                                   choices=["foo", "bar"],
                                   )
        # parameters can be prevented from being changed by setting value of `constant
        self.color = param.Color("#FFFFFF",
                                 constant=True)
        self.bool = param.Boolean(True)

config = Config()
config

>>> ParameterStore(count=6)
```

`ParameterStore` can be exported as JSON dictionary by simply calling `config.export_as_json()` to give:

```python
>>> {
'integer': {'name': 'param',
  'value': 42,
  'doc': 'A not very important value',
  'softbounds': None,
  'hardbounds': None,
  'kind': 'Integer'},
 'number': {'name': 'param',
  'value': 42.0,
  'doc': '',
  'softbounds': [0, 100],
  'hardbounds': [1, 100],
  'kind': 'Number'},
 'string': {'name': 'param', 'value': 'string', 'doc': '', 'kind': 'String'},
 'choice': {'name': 'foo_bar_choice',
  'value': 'foo',
  'doc': '',
  'choices': ['foo', 'bar'],
  'kind': 'Choice'},
 'color': {'name': 'param', 'value': '#FFFFFF', 'doc': '', 'kind': 'Color'},
 'bool': {'name': 'param', 'value': True, 'doc': '', 'kind': 'Boolean'}
 }
```

Built-in type-checking

```python
number = param.Number("42")
[ ... ]
>>> ValueError: Parameter 'param' only takes numeric values
```

Built-in range-checking

```python
number = param.Number(42, hardbounds=[0, 41])
[ ... ]
>>> ValueError: Parameter 'param' must be at most 41
```

Which can be relaxed to allow value correction if its set outside of the hard boundary

```python
number = param.Number(42, hardbounds=[0, 41], auto_bound=True)
[ ... ]
>>> Parameter(name='param', value=41, doc='')
```

## Instalation

Directly from GitHub

```python
pip install git+https://github.com/lukasz-migas/SimpleParam.git
```

or in development mode

```python
git clone git+https://github.com/lukasz-migas/SimpleParam.git

cd SimpleParam

python setup.py develop
```

## Requirements

SimpleParam has no external requirements and works in py2 and py3.


## Planned features

- add 'List', 'Dict' classes
- rename 'Color' to 'ColorHEX' or add 'modes': RGB or HEX
- add Array class
