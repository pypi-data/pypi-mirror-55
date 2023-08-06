Attribute dictionary implementation that allow get access to their elements by keys (as native dict) and attributes.

Installation:
```sh
pip install attrd
```

Usage:

```python
    from attrd import AttrDict

    a = AttrDict(key1=123)

    # Set value by attribute
    a.key2 = 123

    # Set value by key
    a['key3'] = 123

    # Set and delete value by attribute
    a.key4 = 123
    del a.key4

    # Set and delete value by key
    a['key5'] = 123
    del a['key5']

    print(a) # -> {'key1': 123, 'key2': 123, 'key3': 123}
```

Convert existed dict to AttrDict:
```python
    print(AttrDict({'key1': 123, 'key2': 123})) # -> {'key1': 123, 'key2': 123}

    print(AttrDict(**{'key1': 123, 'key2': 123})) # -> {'key1': 123, 'key2': 123}
```

Nested level:
```python
    d = {
        'key1': {
            'sub_key1': 123,
            'sub_key2': {
                'deep_key': 'abc'
            }
        }
    }

    d = AttrDict(d)
    d.key1.sub_key3 = 123

    print(d.key1) # -> {'sub_key1': 123, 'sub_key2': {'deep_key': 'abc'}, 'sub_key3': 123}
    print(d.key1.sub_key1) # -> 123
    print(d.key1.sub_key2.deep_key) # -> abc

    del d.key1.sub_key2
    print(d) # -> {'key1': {'sub_key1': 123, 'sub_key3': 123}}
```

Nested values with kwargs:
```python
    d = AttrDict(key1={'sub_key1': 123, 'sub_key2': 123})

    print(d) # -> {'key1': {'sub_key1': 123, 'sub_key2': 123}}
    print(d.key1.sub_key1) # -> 123

    del d.key1.sub_key2
    print(d) # -> {'key1': {'sub_key1': 123}}
```

Dicts in lists:
```python
    d = AttrDict({
        'key1': [
            {'sub_key1': 123, 'sub_key2': 456},
            {'sub_key1': 123, 'sub_key2': 456},
        ]
    })

    del d.key1[0].sub_key2, d.key1[1].sub_key1
    print(d) # -> {'key1': [{'sub_key1': 123}, {'sub_key2': 456}]}
    print(d.key1[0].sub_key1) # -> 123
```