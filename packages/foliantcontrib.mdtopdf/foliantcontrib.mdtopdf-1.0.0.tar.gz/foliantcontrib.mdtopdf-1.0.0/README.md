[![](https://img.shields.io/pypi/v/foliantcontrib.mdtopdf.svg)](https://pypi.org/project/foliantcontrib.mdtopdf/)

# MdToPdf backend for Foliant

This backend generates a single PDF document from your Foliant project. It uses [md-to-pdf](https://github.com/simonhaenisch/md-to-pdf) library under the hood.

md-to-pdf supports styling with CSS, automatic syntax highlighting by [highlight.js](https://github.com/highlightjs/highlight.js), and PDF generation with [Puppeteer](https://github.com/GoogleChrome/puppeteer).

MdToPdf backend for Foliant operates the `pdf` target.


## Installation

First install md-to-pdf on your machine:

```bash
$ node install -g md-to-pdf
```

Then install the backend:

```shell
$ pip install foliantcontrib.mdtopdf
```

## Usage

```shell
$ foliant make pdf --with mdtopdf
Parsing config... Done
Applying preprocessor flatten... Done
Applying preprocessor mdtopdf... Done
Applying preprocessor _unescape... Done
Making pdf with md-to-pdf... Done
────────────────────
Result: MyProject.pdf
```

## Config

You don't have to put anything in the config to use MdToPdf backend. If it's installed, Foliant will detect it.

You can however customize the backend with options in `backend_config.mdtopdf` section:

```yaml
backend_config:
  mdtopdf:
    mdtopdf_path: md-to-pdf
    options:
      stylesheet: https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/2.10.0/github-markdown.min.css
      body_class: markdown-body
      css: |-
        .page-break { page-break-after: always; }
        .markdown-body { font-size: 11px; }
        .markdown-body pre > code { white-space: pre-wrap; }
```

`mdtopdf_path`
:   is the path to `md-to-pdf` executable. Default: `md-to-pdf`

`options`
:   is a mapping of options which then will be converted into JSON and fed to the md-to-pdf command. For all possible options consult the [md-to-pdf documentation](https://github.com/simonhaenisch/md-to-pdf#usage).
