# **Official Repository for**:  
📄 [*TurnBench-MS: A Benchmark for Evaluating Multi-Turn, Multi-Step Reasoning in Large Language Models*](https://aclanthology.org/2025.findings-emnlp.1084.pdf)

🪶 *Accepted at EMNLP 2025 Findings*  

---

## 🔥 News

- **Nov 2025** [Paper published on ACL Anthology](https://aclanthology.org/2025.findings-emnlp.1084/)
- **Oct 2025** Code released
- **Aug 2025** TurnBench-MS accepted at EMNLP 2025 Findings! 🎉

---

## 🎯 Overview

**TurnBench-MS** is a novel benchmark designed to evaluate **multi-turn, multi-step reasoning** in large language models (LLMs). Unlike traditional benchmarks that test single-turn, single-step tasks, TurnBench simulates **iterative reasoning** through an interactive **code-breaking game** inspired by a "Turing Machine Board Game."

---

## 📚 Tasks

### Task 1: Multi-Turn Reasoning

Models must iteratively propose codes, query verifiers, and deduce the correct code across rounds.

### Task 2: Intermediate Reasoning Evaluation

Beyond final correctness, models’ inferred verifier rules are compared against ground truth to assess reasoning quality.

---

## 🧠 Key Findings

- **Finding 1: LLMs significantly lag behind humans in multi-turn, multi-step reasoning**
- **Finding 2: Once LLMs make a mistake in multi-turn reasoning, they struggle to recover**

---

## ⚡ Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) for Python package and environment management.

### 1. Clone Repository

```{bash}
git clone https://github.com/grantzyr/TurnBench-MS
```

### 2. Install dependencies

```{bash}
uv sync
```

### 3. Activate the virtual environment

```{bash}
source .venv/bin/activate
```

Make sure your editor is using the correct Python virtual environment.

### 4. Setup the environment variables:
```{bash}
$ cp .env.example .env
```
ADD YOUR OWEN API KEY OR LOCALHOST BASEURL

### 5. Try sample game

```{bash}
python main.py
```

All experiment settings in `configs/game_config.yaml` and `configs/model_mapping.yaml`

### Annotation Usage
```{bash}
uvicorn annotation.simple_local_version.main:app --reload
```
then open http://127.0.0.1:8000

## 📝 Citation

If you use TurnBench in your research, please cite:

```
@inproceedings{zhang-etal-2025-turnbench,
    title = "{T}urn{B}ench-{MS}: A Benchmark for Evaluating Multi-Turn, Multi-Step Reasoning in Large Language Models",
    author = "Zhang, Yiran  and
      Wang, Mo  and
      Li, Xiaoyang  and
      Ren, Kaixuan  and
      Zhu, Chencheng  and
      Naseem, Usman",
    editor = "Christodoulopoulos, Christos  and
      Chakraborty, Tanmoy  and
      Rose, Carolyn  and
      Peng, Violet",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2025",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-emnlp.1084/",
    doi = "10.18653/v1/2025.findings-emnlp.1084",
    pages = "19892--19924",
    ISBN = "979-8-89176-335-7"
}
```
