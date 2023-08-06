# apep Quickstart

## Prerequisites

- **apep** Installed [No!](installing.md)

## Nutshell

**apep** is simply a collection of python utility methods and classes used the elioWay. We will stick anything here used by more than one python project in our collection of apps and projects.

## `dictioners`

Methods for dealing with dictionaries.

### `filter_or` and `filter_and`

Both methods accept two dictionaries as parameters. The first dictionary is the target data, the second the filter object.

```
from apep.dictioners import filter_or, filter_and

# True if the filter matches 1 or more of the key+values.
filter_or({"f1": 1, "f2": 2, "f3": 3}, {"f1": 1, "f2": 1})  # True
filter_or({"f1": 1, "f2": 2, "f3": 3}, {"f1": 0, "f2": 1})  # False


# True if the filter matches all the key+values of the search object.
filter_and({"f1": 1, "f2": 2, "f3": 3}, {"f1": 1, "f2": 1})  # False
filter_and({"f1": 1, "f2": 2, "f3": 3}, {"f1": 1, "f2": 2})  # True
```

### `multikeysort`

A utility method for sorting a dictionary list against multiple fields.

```
from apep.dictioners import multikeysort

target =   [
    {"f1": 1, "f2": 1, "f3": 2},
    {"f1": 2, "f2": 1, "f3": 2},
    {"f1": 3, "f2": 2, "f3": 1}
]

multikeysort(target, ["f3", "f2"])

# result == [
#    {"f1": 3, "f2": 1, "f3": 1}
#    {"f1": 2, "f2": 1, "f3": 2},
#    {"f1": 1, "f2": 2, "f3": 2},
# ]

multikeysort(target, ["-f3", "f2"])

# result == [
#    {"f1": 2, "f2": 1, "f3": 2},
#    {"f1": 1, "f2": 2, "f3": 2},
#    {"f1": 3, "f2": 1, "f3": 1}
# ]
```

## `env_var`

### `get_env_variable` and `get_env_variable_bool`

A way to safely retrieve enviroment variables in python; for example in a settings file. Use `get_env_variable_bool` when you are expecting the enviroment variable to resolve to a `True` or `False` value.

```
from apep.env_var import get_env_variable, get_env_variable_bool

HOST_NAME = get_env_variable("HOST_NAME")
IS_FEATURE_ACTIVE = get_env_variable("get_env_variable_bool")
```

## `PickleJar`

A lightweight wrapper for dealing with pickle files. Does little more than handle the reading and writing of pickles.

```
from apep.picklejar import PickleJar
chutney_pj = PickleJar('projectpath/appfolder/optionalfolder', 'cucumber')

# See whether there is anything in the pickle or whether it is about to be created:
if chutney_pj.ripe:
  # there is fruitful data!
  print("Data found in pickle.")

# Pickle some data.
chutney_pj.pickle({'fruit': 'Mango'})

# Open the current data. Parameter accepts a default starting value if empty.
data = chutney_pj.open({})
data['fruit'] = 'Banana'
assert data == {'fruit': 'Banana'}

# Overwrite the data with any data.
chutney_pj.pickle(['Clove', 'Cinnamon', 'Pepper'])
assert chutney_pj.open() == ['Clove', 'Cinnamon', 'Pepper']
```
