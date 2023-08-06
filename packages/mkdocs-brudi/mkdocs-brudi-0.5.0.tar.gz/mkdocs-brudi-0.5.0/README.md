[![Travis][travis-image]][travis-link]
[![Downloads][downloads-image]][downloads-link]
[![Gitter][gitter-image]][gitter-link]
[![PyPI][pypi-image]][pypi-link]
[![dependabot][dependabot-image]][dependabot-link]

  [travis-image]: https://travis-ci.org/brudi/mkdocs-brudi.svg?branch=master
  [travis-link]: https://travis-ci.org/brudi/mkdocs-brudi
  [downloads-image]: https://img.shields.io/pypi/dm/mkdocs-brudi.svg
  [downloads-link]: https://pypistats.org/packages/mkdocs-brudi
  [gitter-image]: https://badges.gitter.im/brudi/mkdocs-brudi.svg
  [gitter-link]: https://gitter.im/brudi/mkdocs-brudi
  [pypi-image]: https://img.shields.io/pypi/v/mkdocs-brudi.svg
  [pypi-link]: https://pypi.python.org/pypi/mkdocs-brudi
  [dependabot-image]: https://img.shields.io/badge/dependabot-enabled-06f.svg
  [dependabot-link]: https://dependabot.com

# Material for MkDocs

A Material Design theme for [MkDocs][1].

[![Material for MkDocs](https://raw.githubusercontent.com/brudi/mkdocs-brudi/master/docs/assets/images/material.png)][2]

  [1]: https://www.mkdocs.org
  [2]: https://github.com/brudi/mkdocs-brudi/

## Quick start

Install the latest version of Material with `pip`:

``` sh
pip install mkdocs-brudi
```

Append the following line to your project's `mkdocs.yml`:

``` yaml
theme:
  name: 'brudi'
```

## Build and release
```
npm run build
pip install wheel twine
python setup.py build sdist bdist_wheel --universal
```


## What to expect

* Responsive design and fluid layout for all kinds of screens and devices,
  designed to serve your project documentation in a user-friendly way in 39
  languages with optimal readability.

* Easily customizable primary and accent color, fonts, favicon and logo;
  straight forward localization through theme extension; integrated with Google
  Analytics, Disqus and GitHub.

* Well-designed search interface accessible through hotkeys (<kbd>F</kbd> or
  <kbd>S</kbd>), intelligent grouping of search results, search term
  highlighting and lazy loading.

For detailed installation instructions and a demo, visit
https://github.com/brudi/mkdocs-brudi/

## License

**MIT License**

Copyright (c) 2016-2019 Martin Donath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
