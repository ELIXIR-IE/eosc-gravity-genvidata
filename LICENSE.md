# Licence

## Original content of this repository

The original content of this repository is licensed under the
**Creative Commons Attribution 4.0 International licence (CC BY 4.0)**.

- Summary: <https://creativecommons.org/licenses/by/4.0/>
- Full legal text: <https://creativecommons.org/licenses/by/4.0/legalcode>

"Original content" means what was written for this use case: the notebooks, the documentation and the configuration files.

You may share and adapt it for any purpose, including commercially, as long as you give credit, link to the licence and say if you made changes.

Suggested credit:

> eosc-gravity-genvidata, ELIXIR Ireland, <https://github.com/ELIXIR-IE/eosc-gravity-genvidata>, licensed under CC BY 4.0.

## What this licence does not cover

This use case chains together existing data, software and services. It is mostly reuse.

CC BY 4.0 applies only to the original content described above. It does **not** cover anything that is reused, and it cannot change the licence of anything that is reused. Each reused resource keeps its own licence and terms of use. If you use this repository, you must follow those too.

Sequence data downloaded by the notebooks is not stored in this repository and is not covered by this licence.

## Reused resources

This table is filled in as the use case grows. Every row must be checked before the use case is finished (see the checklist below).

| Resource | What is reused | Licence or terms | Status |
|---|---|---|---|
| European Nucleotide Archive (ENA) data, EMBL-EBI | Sequence reads and their metadata, downloaded by `01_ena_download.ipynb` | [EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use) and the [INSDC policy](https://www.insdc.org/policy/). An individual record may carry its own conditions. | To verify |
| ENA study [PRJEB40277](https://www.ebi.ac.uk/ena/browser/view/PRJEB40277), Irish Coronavirus Sequencing Consortium | Five runs downloaded (ERR7112279, ERR7112281, ERR7112289, ERR7112290, ERR7112291) and the metadata of the whole study. Described in `metadata/PRJEB40277/PRJEB40277_metadata.md` | As for ENA data above. Submitted by the Irish Consortium for Sequencing Covid | To verify |
| ENA Portal API, EMBL-EBI | The file report service, used to find the files of a record | [EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use) | To verify |
| ENA Browser API and ENA file server, EMBL-EBI | ENA's records for the study, and the sequence files | [EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use) | To verify |
| EBI Search, EMBL-EBI | The count and list of runs in the study | [EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use) | To verify |
| NCBI Sequence Read Archive, through NCBI E-utilities | A second copy of the run table for the study, used as a cross-check | [NCBI policies and disclaimers](https://www.ncbi.nlm.nih.gov/home/about/policies/) and the [E-utilities usage guidelines](https://www.ncbi.nlm.nih.gov/books/NBK25497/) | To verify |
| Python | The programming language | [Python Software Foundation License](https://docs.python.org/3/license.html) | To verify |
| Requests | Python package that sends the web requests | [Apache License 2.0](https://github.com/psf/requests/blob/main/LICENSE) | To verify |
| JupyterLab | The notebook application | [BSD 3-Clause License](https://github.com/jupyterlab/jupyterlab/blob/main/LICENSE) | To verify |
| FastQC | Read quality report (step 2). Installed from Bioconda | [GPL v3 or later](https://github.com/s-andrews/FastQC/blob/master/LICENSE) | To verify |
| fastplong | Nanopore read quality numbers, trimming and filtering (step 2). Installed from Bioconda | [OpenGene/fastplong](https://github.com/OpenGene/fastplong), see its licence file | To verify |
| minimap2 | Mapping reads and contigs (steps 3 and 4). Installed from Bioconda | [MIT](https://github.com/lh3/minimap2/blob/master/LICENSE.txt) | To verify |
| samtools | Sorting, mapping statistics, coverage and consensus (step 3). Installed from Bioconda | [MIT/Expat](https://github.com/samtools/samtools/blob/develop/LICENSE) | To verify |
| Flye | De novo assembly (step 4). Installed from Bioconda | [BSD 3-Clause](https://github.com/mikolmogorov/Flye/blob/flye/LICENSE) | To verify |
| Nextclade | Clade and lineage calls (step 5). Installed from Bioconda | [Nextclade licence](https://github.com/nextstrain/nextclade/blob/master/LICENSE) | To verify |
| Nextclade SARS-CoV-2 dataset, Nextstrain | Reference and tree, downloaded by `nextclade dataset get` (step 5) | See the dataset's own terms at <https://github.com/nextstrain/nextclade_data> | To verify |
| Bioconda | The conda channel the tools above come from | [MIT](https://github.com/bioconda/bioconda-recipes/blob/master/LICENSE) for the recipes. Each tool keeps its own licence | To verify |
| NCBI RefSeq viral genomes | All RefSeq virus genomes, used to identify the virus (step 3) | [NCBI policies and disclaimers](https://www.ncbi.nlm.nih.gov/home/about/policies/) | To verify |
| SARS-CoV-2 reference genome MN908947.3 | Reference for mapping (step 3). Downloaded from ENA | As for ENA data above | To verify |
| ENA SARS-CoV-2 consensus sequences, produced by ENA's analysis pipeline | ENA's own consensus for run ERR7112279, used as a comparison (step 5) | As for ENA data above | To verify |
| ENA SARS-CoV-2 Nanopore analysis workflow | Its commands (trim 30 bases at each end, minimap2, samtools) are repeated in steps 2 and 3. Its code is not copied | [enasequence/covid-sequence-analysis-workflow](https://github.com/enasequence/covid-sequence-analysis-workflow), see its licence file | To verify |
| EMBL-EBI Job Dispatcher (BLAST) and the COVID-19 Data Portal consensus database | Search for the closest matches (step 5) | [EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use) | To verify |
| Swedish SARS-CoV-2 sequences held in ENA | Five records pulled to show the cross-border method (step 5). Accessions are printed by the notebook. Submitted by Swedish data providers | As for ENA data above | To verify |
| ENA Webin test service | Optional validation of the submission file (step 5) | [ENA Webin terms](https://ena-docs.readthedocs.io/en/latest/submit/general-guide.html) | To verify |
| Other packages installed by `environment.yml` | Installed automatically from conda-forge because the packages above need them | Each package has its own licence | To verify |

## To review before this use case is finished

- [ ] Check every row in the table above against the resource's own licence page, and change its status to "Verified" with the date.
- [ ] Add a row for everything reused after step 1. For example: Galaxy and its tools, R and Bioconductor packages, reference databases, Docker base images.
- [ ] For every ENA record used, note its accession and who submitted it, and credit them.
- [ ] Check whether any reused resource limits how its data or outputs may be shared, and whether that affects what this repository may publish.
- [ ] Confirm the name used in the suggested credit, and who holds the copyright in the original content.
- [ ] Decide whether the code should also carry a software licence. Creative Commons [advises against](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software) using its licences for software.
