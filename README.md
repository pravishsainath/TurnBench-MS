# TurnBench-MS

## Requirement
[uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Usage
Firstly, clone the project with:
```{bash}
git clone https://github.com/grantzyr/TurnBench-MS
```
Then you can install all the dependencies with:
```{bash}
uv sync
```
Then you can activate the virtual environment with:
```{bash}
source .venv/bin/activate
```
Make sure your editor is using the correct Python virtual environment.

Then setup the environment variables:
```{bash}
$ cp .env.example .env
```
ADD YOUR OWEN API KEY OR LOCALHOST BASEURL

Then you can try sample game with:
```{bash}
python main.py
```
All experiment settings in `configs/game_config.yaml` and `configs/model_mapping.yaml`

## Annotation Usage
```{bash}
uvicorn annotation.simple_local_version.main:app --reload
```
then open http://127.0.0.1:8000