# PyMdown pymdown-env extension

*Replaces `~~~${ENV_VAR_HERE}~~~` with the content of the environment variable `ENV_VAR_HERE`*

## Installation
``` bash
pip install pymdown-env
```

In `mkdocs.yml`:

``` yml
markdown_extensions:
    - pymdown-env
```

## Example
before
``` markdown
[Download version ~~~${VERSION}~~~](/binaries/~~~${VERSION}~~~/myapp.exe)
```

after
``` markdown
[Download version 1.0.0](/binaries/1.0.0/myapp.exe)
```

## [License](LICENSE.md)