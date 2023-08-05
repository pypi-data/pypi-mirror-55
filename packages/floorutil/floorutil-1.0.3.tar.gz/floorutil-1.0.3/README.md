# FloorUtil
**sample method**

### packaging upload

Packaging

```
python setup.py sdist 
```

Testing

```
pip install dist/floorutil-1.0.0.tar.gz 
```

```
demo
```

Distributing

```
pip install twine

twine upload dist/floorutil-1.0.0.tar.gz 
```

newversion

```buildoutcfg
https://pypi.org/project/floorutil/
```

how to create doc?

**create md**
```buildoutcfg
python -m pydoc floorutil\email_util.py > doc.md
```

**create html**
```buildoutcfg
python -m pydoc -w floorutil\email_util.py
```