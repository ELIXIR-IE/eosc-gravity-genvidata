# eosc-gravity-genvidata

A life-science use case for EOSC Gravity, focused on pathogen sequence data and led by ELIXIR Ireland.

**Status: work in progress.** Steps 1 to 5 exist. Step 1 has been run. Steps 2 to 5 were checked on one file and still need a full run.

## Aim

Show a simple flow that takes pathogen sequence data from a national provider, checks it, builds a genome, identifies it, compares it across borders and prepares it for deposition, with its metadata.

The flow chains together existing tools and resources. It does not build anything new. Where possible it reuses resources from several EOSC nodes and is shown with Irish data.

The code is kept deliberately simple, so that every line can be read and explained.

## Steps

| Step | Notebook | What it does | Resource reused |
|---|---|---|---|
| 1 | [01_ena_download.ipynb](01_ena_download.ipynb) | Downloads raw sequence reads (FASTQ) for an ENA accession and checks the files are complete | [European Nucleotide Archive (ENA)](https://www.ebi.ac.uk/ena/browser/home), EMBL-EBI |
| 2 | [02_metadata_and_qc.ipynb](02_metadata_and_qc.ipynb) | Saves ENA's metadata next to each file, runs quality checks, suggests where to cut the reads, trims and filters | ENA Browser API, [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/), [fastplong](https://github.com/OpenGene/fastplong) |
| 3 | [03_reference_mapping.ipynb](03_reference_mapping.ipynb) | Identifies the virus, maps the reads to a reference, reports the percentage mapped, writes the consensus genome | [minimap2](https://github.com/lh3/minimap2), [samtools](https://www.htslib.org/), NCBI RefSeq viral genomes, the commands of [ENA's SARS-CoV-2 pipeline](https://github.com/enasequence/covid-sequence-analysis-workflow) |
| 4 | [04_de_novo_assembly.ipynb](04_de_novo_assembly.ipynb) | Tries to build the genome without a reference. Expected to fail on this data, and explains why | [Flye](https://github.com/mikolmogorov/Flye) |
| 5 | [05_compare_and_deposit.ipynb](05_compare_and_deposit.ipynb) | Lineage calls, comparison with ENA's own consensus and with Swedish sequences, BLAST against the COVID-19 Data Portal, deposition metadata and submission file | [Nextclade](https://clades.nextstrain.org/), EBI Search, EMBL-EBI BLAST, ENA Webin test service |

## How to run

You need [conda](https://docs.conda.io/) and git.

```bash
git clone https://github.com/ELIXIR-IE/eosc-gravity-genvidata.git
cd eosc-gravity-genvidata
conda env create -f environment.yml
conda activate ls-use-case
jupyter lab
```

Then open the notebooks in order, 01 to 05, and in each one:

1. Check the "Your input" cell and set the values.
2. Run the cells one at a time, from top to bottom.
3. In notebook 1, check the total download size printed in step 5 before you run the download in step 6.
4. Choose the `ls-use-case` kernel (top right of the notebook). The first cells of notebooks 2 to 5 check the tools can be found.

If you already made the environment, update it with `conda env update -n ls-use-case -f environment.yml`. The tools added for steps 2 to 5 take about 1 GB of disk.

Notebook 3 downloads the RefSeq viral genomes (about 180 MB, once). Everything is saved in a `data/` folder, in one subfolder per ENA accession plus `data/reference/`. That folder is not part of this repository. Notebook 2 writes a `README.txt` into it that explains every file.

Step 5 never submits anything to ENA's real service.

## What is in this repository

| File | Purpose |
|---|---|
| `01_ena_download.ipynb` to `05_compare_and_deposit.ipynb` | Notebooks for steps 1 to 5 |
| `environment.yml` | The conda environment: Python, JupyterLab, Requests, FastQC, fastplong, minimap2, samtools, Flye and Nextclade |
| `LICENSE.md` | The licence of this repository, and the licences of everything it reuses |
| `README.md` | This file |

## Reuse and licensing

This use case is mostly reuse.

The original content of this repository is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The data, software and services it reuses are **not** covered by that licence. Each keeps its own licence and terms.

[LICENSE.md](LICENSE.md) lists every reused resource. The list is filled in as the use case grows and will be checked in full before the use case is finished.

## Where this is going

None of this is built yet.

- Deposition of a real consensus with its metadata, once the placeholders in notebook 5 are replaced with a study and sample you own.
- A Galaxy workflow that runs the steps, with the notebooks turned into Python or Bash scripts. Some steps may use R and Bioconductor.
- Docker, so the whole use case runs the same way on any machine.

## Questions

Please open an [issue](https://github.com/ELIXIR-IE/eosc-gravity-genvidata/issues).
