# ActionKit Template Runner
---

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/dsa-ntc/actionkit-templates)

> This is a public fork of the [MoveOnOrg/actionkit-templates](https://github.com/MoveOnOrg/actionkit-templates) repository, reproduced with permission via MIT License. All code contained is open-source. Contributors MUST abide by the DSA NTC's [Code of Conduct](https://docs.google.com/document/d/12JOWHitVxx8ZR15Ea46JrD1fTpqO2xhBzag1cHRmFwE/edit?usp=sharing).

## Getting Started

There are two separate quickstart instructions depending on what you're trying to do.

- [I want to render ActionKit templates with a simple shell command]
- [I want to work on this project's internals]

## What is this repo?

As mentioned in the note above, this repo is a fork of MoveOn.org's `actionkit-templates` repo. This repo has served as the baseline thus far for DSA staff and volunteers to render [ActionKit Templates](https://docs.actionkit.com/docs/manual/developer/templates_index.html) in a local development environment. However, that repo is no longer maintained and contains severe deprecations. Additionally, the unconventional project layout of the MoveOn repo obfuscates the ways that the package acts like a Django project and is inaccessible to many Python/Django developers.

Thus, this repo has *two primary aims*:

1) Replace the primary functionality of the MoveOn repo by reproducing its internals and upgrading key dependencies to stable and secure version. In other words, this repo will:
  - Publish a package to PyPI ([`dsa-actionkit`](https://pypi.org/project/dsa-actionkit/)), making the template runner *pip-installable*.
  - Allow users to view custom templates connected to a Django server with the shell command (optionally defining the host/port if necessary in the customary Django way):
  ```shell
  aktemplates runserver
  ```

2) Provide an environment that can *fully take advantage* of Django niceties by giving us full control over the server. While the backend may not necessarily be a one-to-one match to ActionKit's, we can replicate more than enough functionality using ActionKit's public documentation to build a robust template engine that mimics ActionKit's in the most important ways. For example this will allow developers to have:

- Complete control over a User model that enables the replication and testing of key authentication workflows.
- Django's test runner, which can test functionality with custom browser contexts.
- The ability to permutate many datasets and configurations with the template runner and build user-interfacing testing tools on top of them
- and much more

Importantly, all work in this repository is *fully public and open-sourced*, lowering the barrier to entry for developers who may not have privileged access to the `dsausa` GitHub Organization.  Accordingly, developers should take extra caution to avoid committing sensitive information to the repo.

### How does this repo relate to the `dsausa/actionkit-templates` repo?

Right now, the `dsausa/actionkit-templates` repo -- the repo that serves the templates live to production -- still uses the MoveOn repo upstream. At some point, when development is considered stable, the `dsausa/actionkit-templates` repo should use this project as its upstream template runner instead; obviously this change would fall fully under staff discretion.

If you are interested in directly developing *templates* at the point closest to production, you should obtain access to the `dsausa` repo and submit work against the `staging` branch. If you're interested in developing robust infrastructure around the ActionKit Templates project, including but not limited to the Django backend work, you can do everything you need to do solely within this project.

At some point, it might be preferable to link certain folders (such as the `template_sets` directory) via git or other methods to keep *template* work in-sync. For now, this repository contains example data inherited from the MoveOn repo. More DSA-specific example templates can and should be loaded after they are appropriately audited for sensitive information.

## Getting started using the `dsa-actionkit` package as a template runner

Anyone may install the command-line utility published by this repo by running `pip install dsa-actionkit` or by declaring `dsa-actionkit` in your project's `pyproject.toml` or `requirement.txt` as appropriate to your chosen installation setup/package manager.

> To make contributions and changes to the way this app runs under the hood, skip to [Developing](#developing) and work directly from the source code in this repository!

Here's an example set of commands that includes creating a directory for the project and a virtual environment to install `dsa-actionkit` in:

```console
$ mkdir myproject && cd myproject
$ python --version
Python 3.11.7
$ python -m venv .venv
$ source .venv/bin/activate
(myproject) $ pip install dsa-actionkit
(myproject) $ aktemplates runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 14, 2023 - 22:24:28
Django version 3.2.6, using settings 'dsa_actionkit.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Customize

> Note: This section copied from MoveOn, elaboration/clarification/condensation warranted

1. Put your actionkit templates in a directory called `template_set` (configurable)
2. Put your static assets (javascript, css) in a directory called `static` (configurable)

### Environment variables

You can customize your setup further by using environment variables:

`TEMPLATE_DIR`

By default we search the local directory and a directory called template_set.  If you run:

```
TEMPLATE_DIR=actionkittemplates aktemplates runserver
```

it will also look in the directory `actionkittemplates/`

`CUSTOM_CONTEXTS`

You can add additional test contexts and put them in either a file called `contexts.json` or set this environment variable to the json file to use.  JSON files should be in the form:

```json

   {"name_of_context": {
       "filename": "event_attend.html",
       "all_the_context_keys_for_this_context": {
       },
       "page": {
          "title": "My Page Title",
          "type": "Event"
       },
       "event": {
           "...": "..."
       }
   }

```

`STATIC_ROOT`

By default we serve the `./static/` directory at /static/  This goes well with code in your wrapper.html template like this:

```html
    {% if args.env == "dev" or devenv.enabled or 'devdevdev' in page.custom_fields.layout_options %}
      <!-- development of stylesheets locally -->
      <link href="/static/stylesheets/site.css" rel="stylesheet" />
    {% else %}
      <!-- production location of stylesheets -->
      <link href="https://EXAMPLE.COM/static/stylesheets/site.css" rel="stylesheet" />
    {% endif %}
```

`STATIC_FALLBACK`

In the occasional moment when you are developing without an internet connection this will fail to load:

```
{% load_js %}
//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js
{% end %}
```

In that situation, if you set STATIC_FALLBACK to a directory where, e.g. `jquery.min.js` is present, then it will look for all the internet-external files in that directory. Note that this only works with `load_js` and `load_css` template tags.

## Contributing

The easiest way to set up your development environment is to use our Codespaces/Dev Container setup. If you prefer to manually install your dependencies, as of right now this repo supports Python 3.11 and you may need to configure a few environment variables (inspect the devcontainer.json for clues)

In the project root, create a virtual environment and install the project package and all dependencies in editable mode:

  ```
  python -m venv .venv
  source .venv/bin/activate
  pip install -e .
  ```

For more info about how the project layout and how it works visit [CONTRIBUTING.md](./CONTRIBUTING.md)
