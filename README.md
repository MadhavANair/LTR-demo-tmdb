# LTR DEMO in opensearch
## Setup is as same as hello-ltr repo 
The overall goal of this project is to demonstrate all the steps required to work with LTR in OpenSearch. There are two modes of running this project. You can run and edit notebooks in a docker container or you can do local development on the notebooks and connect to the search engine(s) running in Docker.

## No fuss setup: You just want to play with LTR

Follow these steps if you're just playing around & are OK with possibly losing some work (all notebooks exist just in the docker container)

With docker simply run

```
docker compose up (-d) if you want to detached
```

at the root dir and go to town!

This will run jupyter and all search engines in Docker containers. Check that each is up at the default ports:

only Opensearch is available here
- OpenSearch: [localhost:9201](localhost:9201)
- OpenSearch Dashboards: [localhost:5602](localhost:5602)
- Jupyter: [localhost:8888](localhost:8888)

## You want to build your own LTR notebooks
git 
Follow these steps if you want to do more serious work with the notebooks. For example, if you want to build a demo with your work's data or something you want to preserve later.

### Run your search engine with Docker

You probably just want to work with one search engine. So whichever one you're working with, launch that search engine in Docker.


#### Running OpenSearch w/ LTR

Setup OpenSearch with docker compose to work with just OpenSearch examples:

```
cd notebooks/opensearch
docker compose up
```

### Run Jupyter locally w/ Python 3 and all prereqs

#### Setup Python requirements

- Ensure Python 3.8 or later is installed on your system
- Create a virtual environment: `python3 -m venv venv`
- Start the virtual environment: `source venv/bin/activate`
- Check install tooling is up to date `python -m pip install -U pip wheel setuptools`
- Install the requirements `pip install -r requirements.txt`

__Note:__ The above commands should be run from the root folder of the project.

#### Start Jupyter notebook and confirm operation

- Run `jupyter notebook`
- Browse to notebooks/{search\_engine}/{collection} 
- Open the appropriate notebook for your search engine, run each cell, and ensure you get a graph at the last cell:

  - "ltr-tmdb (OpenSearch).ipynb"



### While developing...

For more informal development:

- Do your development
- Run the command as needed:

- Tests fail if notebooks return any errors
  - The failing notebook will be stored at `tests/last_run.ipynb`
