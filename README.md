


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/repo_logo_dark.png" width='100%'>
  <source media="(prefers-color-scheme: light)" srcset="./assets/repo_logo_light.png" width='100%'>
  <img alt="Project logo" src="/assets/" width="100%">
</picture>

<br>

[![tests](https://github.com/schwallergroup/rambo-I/actions/workflows/tests.yml/badge.svg)](https://github.com/schwallergroup/rambo-I)
[![Documentation Status](https://readthedocs.org/projects/rambo/badge/?version=latest)](https://rambo.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Cookiecutter template from @SchwallerGroup](https://img.shields.io/badge/Cookiecutter-schwallergroup-blue)](https://github.com/schwallergroup/liac-repo)
[![Learn more @SchwallerGroup](https://img.shields.io/badge/Learn%20%0Amore-schwallergroup-blue)](https://schwallergroup.github.io)




<h1 align="center">
  rambo
</h1>


<br>


Retrieval AugMented Bayesian Optimization

> How to select the first few experiments for your optimization campaign?
>
> RAMBO leverages previous data to suggest promising first steps, and then optimizes from there using BO.



## 🔥 Usage

```bash
rambo suggest \
    --prompt="Suzuki coupling between primary halide and boronic acid." \
    --retrieval_type=embedding
```

This code will suggest initial conditions that are well suited to your specs, leveraging internal data and literature.



## 👩‍💻 App

See a live demonstration [here](https://shorturl.at/jnxzE)!

[![demo](https://github.com/schwallergroup/rambo-I/assets/32375632/5d89617e-cd67-4508-9028-5d98eee3d0f5)](https://shorturl.at/jnxzE)



## 👩‍💻 Installation

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/schwallergroup/rambo-I.git
```

Set the following environment variables in your `.env` file:

```bash
OPENAI_API_KEY = '...'
CHROMA_DB_PATH = '...' # path to persistent chroma db. This is given as a chroma.sqlite3 file and should be set to /path/to/rambo-I/chroma
```


## Poster

Check out our poster for the [AC-BO-Hackathon](https://ac-bo-hackathon.github.io/).
![rambo_clean-1](https://github.com/schwallergroup/rambo-I/assets/32375632/9ac0ae1d-050f-4990-aa8b-32e46d1d0064)


## ✅ Citation

```bibtex
@Misc{rambo,
  author = { Bojana Rankovic, Andres M Bran, Magdalena Lederbauer, Anna Borisova, Geemie Wellawette, Philippe Schwaller },
  title = { rambo - Retrieval augmented Bayesian optimization },
  howpublished = {Github},
  year = {2024},
  url = {https://github.com/schwallergroup/rambo-I }
}
```
