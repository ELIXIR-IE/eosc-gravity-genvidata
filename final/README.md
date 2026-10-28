# GenViData final: one Galaxy workflow, end to end

## What it does

Takes one Irish SARS-CoV-2 sample of concern, given as an ENA run accession, and compares it with Swedish samples.
Galaxy downloads the reads from ENA itself and runs every step:

1. **Variation:** IWC workflow "COVID-19: variation analysis of ARTIC ONT data" (BY-COVID collection): fastp, minimap2, ivar trim, medaka, lofreq, SnpEff
2. **Consensus:** IWC workflow "COVID-19: consensus construction" (bcftools consensus, low-coverage masking)
3. **Join:** Irish and Swedish consensus sequences, plus Swedish consensus sequences already in ENA
4. **Lineage and mutations:** Nextclade
5. **Distances:** snp-dists (SNP differences between every pair of sequences)
6. **Variant tables:** SnpSift (one row per variant, with gene and protein change)

Swedish data is found the way a researcher would find it: Swedish Pathogens Portal → European Pathogens Portal (EMBL-EBI) → ENA accessions (`scripts/01_find_data.py`).

## Input

- `config.yml`: the Irish run accession (default `ERR7112279`), the date window for Swedish data, and the primer file for each data set.
- Nothing to download by hand. The reads come from ENA, the reference from Zenodo, and the primer files are in `workflow/primers/`.

## Output

Results go to `results/<date>/`. `summary.md` explains them in plain language.

| File | What it is |
|---|---|
| `summary.md` | Lineage, clade, quality, coverage, variants and closest Swedish sequence, per sample |
| `*consensus*.fasta` | Consensus genome per sample |
| `*annotated_variants*.vcf` | Variants with SnpEff annotation |
| `*variant_table*` | One row per variant: position, change, allele frequency, depth, gene, protein change |
| `lineage_report` | Nextclade: clade, Pango lineage, mutations, quality |
| `snp_distances` | Number of SNP differences between every pair of sequences |
| `*qc_report*.html` | MultiQC report: read quality and mapping |

## Needs

- Docker
- Python 3.10 or newer
- Internet access, for ENA, the Tool Shed and the Nextclade dataset

## Recommended compute

| Where | CPU | RAM | Free disk |
|---|---|---|---|
| Laptop test, one sample | 4 cores | 16 GB | 25 GB (the Galaxy image is 4 GB, the tools about 10 GB) |
| Compute site (for example ICHEC) | 8 cores | 32 GB | 50 GB |

Measured on a 16-thread laptop with 16 GB RAM: setting up Galaxy and the tools (step 3) took about 30 minutes,
and one run of the four samples (step 4) took about 15 minutes. Galaxy's storage is about 15 GB after setup.

## Commands

Copy these lines into a terminal. The first line moves into this `final/` folder; every other command expects to run there.

```bash
cd ~/PhD_Code/LS_Use_Case/final

# once: the small Python tools that talk to Galaxy (Planemo, Ephemeris)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# every time you open a new terminal
source .venv/bin/activate

python scripts/01_find_data.py      # find the Irish run and the Swedish data -> inputs/samples.tsv
python scripts/02_make_job.py       # write the Galaxy job file -> inputs/job.yml
bash scripts/03_start_galaxy.sh     # start Galaxy in Docker and install the tools (first time about 30 minutes)
bash scripts/04_run_workflow.sh     # run the workflow and download the outputs -> results/<date_time>/ (about 15 minutes)
python scripts/05_summarise.py      # write summary.md in the newest results folder
```

Running `03_start_galaxy.sh` again is safe: it skips everything already installed and takes a few minutes.
Watch a run at http://localhost:8080 (log in as `admin@example.org`, password `password`). Galaxy is only reachable from your own computer.
Stop Galaxy with `docker stop genvidata-galaxy`. Start it again with `bash scripts/03_start_galaxy.sh`.

## Workflow graph

- **In Galaxy itself:** open http://localhost:8080, go to *Workflows*, and open the GenViData workflow in the editor. Galaxy draws the
  full graph, including every step inside the subworkflows. A run's page (*User > Workflow Invocations*) also shows the state of each step.
- **As files** (made by `python scripts/make_workflow_dag.py`):
  - `workflow/genvidata_dag.png` / `.svg`: picture with the main tools of each subworkflow
  - `workflow/genvidata_dag.md`: the same graph in Mermaid (open the Markdown preview in VS Code, or view on GitHub)
  - `workflow/genvidata_dag_interactive.html`: Galaxy's own interactive graph (made with `gxwf-viz` from gxformat2), open in a browser

## Files

| Path | Purpose |
|---|---|
| `workflow/genvidata.gxwf.yml` | The workflow (readable Galaxy Format2) |
| `workflow/iwc/` | The two IWC workflows, unchanged, used as subworkflows |
| `workflow/tools.yml` | Tool Shed repositories and revisions to install |
| `workflow/primers/` | Primer files and how the scheme of each data set was checked |
| `scripts/` | The five steps above, and the helpers they call |
| `results/<date_time>/` | Outputs of one run, with `summary.md` (two example runs are included) |

**Not in the repository**, because they are large or specific to one computer. The commands above recreate them:

| Path | Size | Made by |
|---|---|---|
| `galaxy_storage/` | about 15 GB | `03_start_galaxy.sh` (Galaxy's database, installed tools and their software) |
| `.venv/` | about 350 MB | `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` |
| `galaxy_api_key.txt`, `galaxy_invocation.txt` | tiny | `03_start_galaxy.sh` / `04_run_workflow.sh` |
| The Galaxy Docker image | 4.2 GB | downloaded by Docker the first time `03_start_galaxy.sh` runs |

## Notes

- **Primer schemes were checked from the reads.** The Irish ENA record says "Artic v3", but the reads match the
  Midnight 1200 bp scheme. The Swedish reads match ARTIC v3. Details in `workflow/primers/SOURCES.md`.
- **Two old tools needed help.** The IWC workflow pins medaka 1.0.3 / 1.3.2 and MultiQC 1.8, which conda can no
  longer build. `scripts/fix_old_tool_envs.sh` installs medaka 1.3.4 (same 1.3 series and commands) and rebuilds
  MultiQC 1.8 on Python 3.8. Nothing else in the IWC workflows was changed, apart from one empty setting that
  Galaxy 25 requires (`scripts/make_native_workflow.py`).
- **Swedish consensus sequences in ENA are few** for mid-2021 (Sweden shared most sequences through GISAID).
