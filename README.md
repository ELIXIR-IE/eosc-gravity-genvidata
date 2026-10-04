# eosc-gravity-genvidata

A life-science use case for EOSC Gravity, focused on pathogen sequence data and led by ELIXIR Ireland.

**Status: work in progress.** Only step 1 exists so far, and it is still being tested.

## Aim

Show a simple flow that identifies a pathogen from sequence data.

The flow chains together existing tools and resources. It does not build anything new. Where possible it reuses resources from several EOSC nodes and is shown with Irish data.

The code is kept deliberately simple, so that every line can be read and explained.

## Steps

| Step | Notebook | What it does | Resource reused |
|---|---|---|---|
| 1 | [01_ena_download.ipynb](01_ena_download.ipynb) | Downloads raw sequence reads (FASTQ) for an ENA accession and checks the files are complete | [European Nucleotide Archive (ENA)](https://www.ebi.ac.uk/ena/browser/home), EMBL-EBI |

## How to run

You need [conda](https://docs.conda.io/) and git.

```bash
git clone https://github.com/ELIXIR-IE/eosc-gravity-genvidata.git
cd eosc-gravity-genvidata
conda env create -f environment.yml
conda activate ls-use-case
jupyter lab 01_ena_download.ipynb
```

Then, in the notebook:

1. Paste an ENA accession into the cell under "2. Your input".
2. Run the cells one at a time, from top to bottom.
3. Check the total download size printed in step 5 before you run the download in step 6.

Downloaded files are saved in a `data/` folder. That folder is not part of this repository.

## What is in this repository

| File | Purpose |
|---|---|
| `01_ena_download.ipynb` | Step 1 notebook |
| `environment.yml` | The conda environment: Python, JupyterLab and Requests |
| `LICENSE.md` | The licence of this repository, and the licences of everything it reuses |
| `README.md` | This file |

## Reuse and licensing

This use case is mostly reuse.

The original content of this repository is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The data, software and services it reuses are **not** covered by that licence. Each keeps its own licence and terms.

[LICENSE.md](LICENSE.md) lists every reused resource. The list is filled in as the use case grows and will be checked in full before the use case is finished.

## Where this is going

None of this is built yet.

- More steps that identify the pathogen in the downloaded reads, using existing tools.
- A Galaxy workflow that runs the steps, with the notebooks turned into Python or Bash scripts. Some steps may use R and Bioconductor.
- Docker, so the whole use case runs the same way on any machine.

## Questions

Please open an [issue](https://github.com/ELIXIR-IE/eosc-gravity-genvidata/issues).
