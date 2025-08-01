# Hereditary Stratigraphic Surface (hsurf) Concept

[![CI](https://github.com/mmore500/hstrat-surface-concept/actions/workflows/ci.yaml/badge.svg)](https://github.com/mmore500/hstrat-surface-concept/actions/workflows/ci.yaml)
[![GitHub stars](https://img.shields.io/github/stars/mmore500/hstrat-surface-concept.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/hstrat-surface-concept)
[![DOI](https://zenodo.org/badge/652063401.svg)](https://zenodo.org/doi/10.5281/zenodo.10779240)
<!-- [![Documentation Status](https://readthedocs.org/projects/hstrat-surface-concept/badge/?version=latest)](https://hstrat-surface-concept.readthedocs.io/en/latest/?badge=latest) -->
<!-- [![documentation coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fmmore500.github.io%2Fhstrat-surface-concept%2Fdocumentation-coverage-badge.json)](https://hstrat-surface-concept.readthedocs.io/en/latest/) -->
<!-- [![code coverage status](https://codecov.io/gh/mmore500/hstrat-surface-concept/branch/master/graph/badge.svg)](https://codecov.io/gh/mmore500/hstrat-surface-concept) -->
<!-- [![dotos](https://img.shields.io/endpoint?url=https%3A%2F%2Fmmore500.com%2Fhstrat-surface-concept%2Fdoto-badge.json)](https://github.com/mmore500/hstrat-surface-concept/search?q=todo+OR+fixme&type=) -->

hsurf provides efficient, constant-space downsampling of data streams via DStream algorithms, with applications including heredity stratigraphic phylogenetic inference over distributed digital evolution populations.

-   Free software: MIT license

<!---
-   Documentation: <https://hstrat-surface-concept.readthedocs.io>.
-->

## Installation

`python3 -m pip install "git+https://github.com/mmore500/hstrat-surface-concept.git@v1.0.2#egg=hsurf"`

To set up locally,

```bash
git clone --single-branch https://github.com/mmore500/hstrat-surface-concept.git
cd hstrat-surface-concept
./submodules.sh
```

## Documentation

Slide deck & graphics for this project are at <https://hopth.ru/ce>.
Some notes are in the template manuscript skeleton in `tex/`, which is built via GitHub actions and can be downloaded as an artifact.

See `binder` for usage examples.

## Roadmap

This repository hosts prototype code for algorithm development of a lightweight fixed-length hereditary stratigraphy data structure.

Code here is designed for use in conjunction with the mainline [`hstrat`](https://github.com/mmore500/hstrat) and [`downstream`](https://github.com/mmore500/downstream) packages.
Long-term, code in this repository will migrate to the `hstrat` and `downstream` packages and this will remain only to ensure records (and reproducibility) of prototype work.

## Citing

If pecking contributes to a scientific publication, please cite it as

> Matthew Andres Moreno. (2024). mmore500/hstrat-surface-concept. Zenodo. https://zenodo.org/doi/10.5281/zenodo.10779240

```bibtex
@software{moreno2024hsurf,
  author = {Matthew Andres Moreno},
  title = {mmore500/hstrat-surface-concept},
  month = mar,
  year = 2024,
  publisher = {Zenodo},
  doi = {10.5281/zenodo.10779240},
  url = {https://zenodo.org/doi/10.5281/zenodo.10779240}
}
```

Consider also citing [hstrat](https://hstrat.readthedocs.io/en/stable/citing.html).
And don't forget to leave a [star on GitHub](https://github.com/mmore500/hstrat-surface-concept/stargazers)!

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [mmore500/cookiecutter-dishtiny-project](https://github.com/mmore500/cookiecutter-dishtiny-project) project template.

<!---
This package uses [Empirical](https://github.com/devosoft/Empirical#readme), a library of tools for scientific software development, with emphasis on also being able to build web interfaces using Emscripten.
-->
