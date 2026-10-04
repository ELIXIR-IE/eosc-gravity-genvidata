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
| ENA Portal API, EMBL-EBI | The file report service, used to find the files of a record | [EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use) | To verify |
| Python | The programming language | [Python Software Foundation License](https://docs.python.org/3/license.html) | To verify |
| Requests | Python package that sends the web requests | [Apache License 2.0](https://github.com/psf/requests/blob/main/LICENSE) | To verify |
| JupyterLab | The notebook application | [BSD 3-Clause License](https://github.com/jupyterlab/jupyterlab/blob/main/LICENSE) | To verify |
| Other packages installed by `environment.yml` | Installed automatically from conda-forge because the packages above need them | Each package has its own licence | To verify |

## To review before this use case is finished

- [ ] Check every row in the table above against the resource's own licence page, and change its status to "Verified" with the date.
- [ ] Add a row for everything reused after step 1. For example: Galaxy and its tools, R and Bioconductor packages, reference databases, Docker base images.
- [ ] For every ENA record used, note its accession and who submitted it, and credit them.
- [ ] Check whether any reused resource limits how its data or outputs may be shared, and whether that affects what this repository may publish.
- [ ] Confirm the name used in the suggested credit, and who holds the copyright in the original content.
- [ ] Decide whether the code should also carry a software licence. Creative Commons [advises against](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software) using its licences for software.
