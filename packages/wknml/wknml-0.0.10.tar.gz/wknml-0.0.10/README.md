# wknml

Python library for working with webKnossos NML files.

## Installation
To use wknml, you need to have Python 3 (on the system or with Anaconda) installed.

```
pip install wknml
```

## Snippets
```
# Check out the repository and go into it
git clone git@github.com:scalableminds/wknml.git
cd wknml

# Convert an NML file with unlinked nodes to one with connected trees
python -m examples.fix_unlinked_nml <unlinked>.nml <fixed>.nml

```
