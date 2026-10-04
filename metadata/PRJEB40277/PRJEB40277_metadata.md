# PRJEB40277: what this data is, and where every fact comes from

Compiled on 2026-10-04 by Claude Code (an AI coding assistant) working for Gavin Farrell.
Every value below was read from a named source or measured from a file, and the source is given beside it.
No person has yet checked this document line by line.

**Status: complete.** ENA's record for every run, experiment and sample in the study was fetched.

## 1. In short

- **The study.** PRJEB40277 is the "Irish Coronavirus Sequencing Consortium" study in the European Nucleotide Archive (ENA). It holds sequencing reads of SARS-CoV-2, the virus that causes COVID-19, from swabs taken from people in Ireland.
- **Its size.** 80,892 sequencing runs from 80,892 samples, one run per sample. ENA's records count 21,270,413,522 reads and 3,553,411,432,580 bases. The files add up to well over 1 TB.
- **When and where.** Swabs collected from 2020-03-13 to 2024-01-09; 56.8% in 2021 and 37.2% in 2022. Every sample is recorded as from Ireland and from a human host. Dublin is the largest county, at 30.1%.
- **How it was sequenced.** All amplicon sequencing, one file per run. 78.9% Oxford Nanopore MinION; 20.6% Illumina MiSeq; 0.5% Oxford Nanopore GridION. The laboratory protocol is recorded as "Artic protocol version 3" on 47.2% of experiments and is not recorded at all on 52.8%. Section 9 explains why the recorded protocol should not be trusted as it stands.
- **What is on this machine.** Five of those runs, 75 MB in total, in `data/PRJEB40277/`. They are five Oxford Nanopore MinION runs from swabs collected on 2 and 3 September 2021 in Dublin, Meath and Kildare.
- **Samples are not patients.** No record gives a patient identifier, so the number of patients cannot be counted. See section 6.

## 2. Sources

Each fact in this document cites one of these sources by its code.

| Code | Source | What it gave | How it was reached | Retrieved (UTC) |
|---|---|---|---|---|
| S1 | ENA Browser API, EMBL-EBI | ENA's own record for the study, and for every run, experiment and sample in it | `https://www.ebi.ac.uk/ena/browser/api/xml/<accession>`, up to 500 accessions per request | 2026-10-04, from 20:26 |
| S2 | ENA file server, EMBL-EBI | The FASTQ files themselves, and the original files the laboratory submitted | `https://ftp.sra.ebi.ac.uk/vol1/fastq/...` and `https://ftp.sra.ebi.ac.uk/vol1/run/...` | 2026-10-04, 20:06 and 20:26 |
| S3 | NCBI Sequence Read Archive run table | A second copy of the run list for the whole study, with NCBI's own read counts and file sizes | NCBI E-utilities, `efetch` with `db=sra`, `rettype=runinfo`, search term `PRJEB40277` | 2026-10-04, 20:08 to 20:14 |
| S4 | EBI Search, EMBL-EBI | An independent count of the runs in the study | `https://www.ebi.ac.uk/ebisearch/ws/rest/sra-run?query=PRJEB40277` | 2026-10-04, about 20:05 |
| S5 | Measured on this machine | Read counts, read lengths, quality and checksums, calculated from the downloaded files | Python, reading each `.fastq.gz` file | 2026-10-04, 20:15 to 20:30 |

**Which source is used for what.** ENA is where this study was submitted, so ENA holds the original records. Everything in sections 3 to 7 comes from ENA's own records (S1) unless a row says otherwise. NCBI's archive receives a copy of ENA's records through the international exchange between the archives (INSDC). That copy (S3) is used here only to cross-check ENA's figures and to estimate file sizes.

**The source that could not be used.** ENA's normal route for metadata is the ENA Portal API (`https://www.ebi.ac.uk/ena/portal/api/`). Its "file report" is the metadata file ENA offers for download for a study. On 2026-10-04 this service returned "HTTP 500 Internal Server Error" at every check, the latest at 20:25 UTC, on every address including its own documentation page. The fault is at EMBL-EBI. Until it is fixed:

- ENA's file report for this study has **not** been downloaded. The same metadata was instead read from ENA's individual records (S1).
- ENA's own MD5 checksums and file sizes for the FASTQ files have **not** been obtained. Section 8 explains what was checked instead.

When the service is back, this address returns ENA's file report for the study:

```
https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB40277&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv
```

ENA's own study record links to exactly this address, which is how its form is known.

## 3. The study record

Evidence for every row: S1, saved as `ena_records/PRJEB40277.study.xml`.

| Fact | Value |
|---|---|
| Study accession | PRJEB40277 |
| Second accession for the same study | ERP123896 |
| Name | Irish Coronavirus Sequencing Consortium |
| Title | Interinstitutional effort to sequence SARS-CoV-2 circulating genomes in Ireland during the Covid-19 global pandemic. |
| Submitting centre | Irish Consortium for Sequencing Covid |
| Submitter's own label | ena-STUDY-UCD National Virus Reference Laboratory-09-09-2020-12:55:26:785-965 |
| Status at ENA | PUBLIC |
| First made public | 2020-10-14 |
| Parent project | PRJEB39908, "INSDC SARS-CoV-2 Viral Sequencing Data", the umbrella project that groups all public SARS-CoV-2 sequencing data |

The study's own description, quoted from ENA:

> This project aims to discover the genetic makeup of coronavirus (SARS-CoV-2), the virus that is causing the current pandemic of Covid-19, by looking at the DNA sequence of the virus from samples taken from Covid–positive patients throughout Ireland. Coronaviruses can mutate or change the proteins on their surface, making it more difficult to develop an effective vaccine against them. These mutations or changes have not been observed as much in the coronavirus causing Covid19 (SARS-CoV-2). However, it is important to keep monitoring this to ensure the coronavirus doesn't change in such a way that makes it even more difficult to treat or vaccinate against. Additionally, by sequencing samples from all over the country, we will be able to help show how the virus is spreading in the community and also between Ireland and other countries.

## 4. The whole study: runs and sequencing

Evidence for this section, unless a row says otherwise: S1, ENA's own run records (all 80,892 runs) and experiment records (all 80,892 experiments), saved as `full_study_tables/ena_runs.csv` and `full_study_tables/ena_experiments.csv`.

| Fact | Value | Evidence |
|---|---|---|
| Runs in the study | 80,892 | S4 (`hitCount` 80,892), S3 (80,892 rows), and NCBI's own search count (80,892). ENA run records fetched: 80,892 |
| Experiments | 80,892 | S1 run record, `EXPERIMENT_REF`. S3 gives 80,892 |
| Samples | 80,892 | S1 run record, link `ENA-SAMPLE`. S3 gives 80,892 |
| Runs per sample | Exactly 1, for every one of the 80,892 samples | S1 run record, link `ENA-SAMPLE`. S3 shows the same |
| Submissions (batches uploaded to ENA) | 290 | S1 run record, link `ENA-SUBMISSION`. S3 gives 290 |
| Study named on each run | ERP123896 (80,892) | S1 run record, link `ENA-STUDY`. ERP123896 is PRJEB40277 |
| Status at ENA | PUBLIC (80,892) | S1 run record, `ENA-STATUS` |
| Organism | Severe acute respiratory syndrome coronavirus 2, taxonomy ID 2697049 (80,892) | S1 sample record, `SAMPLE_NAME` (all 80,892 samples). S3 gives taxonomy ID 2697049 for all 80,892 runs |
| Library strategy | AMPLICON (80,892) | S1 experiment record, `LIBRARY_STRATEGY` |
| Library source | GENOMIC (80,892) | S1 experiment record, `LIBRARY_SOURCE` |
| Library selection | unspecified (80,892) | S1 experiment record, `LIBRARY_SELECTION` |
| Library layout | SINGLE (80,892) | S1 experiment record, `LIBRARY_LAYOUT` |
| Format of the files the laboratories submitted | fastq (80,892 files) | S1 run record, `DATA_BLOCK/FILES/FILE`, attribute `filetype` |
| Submitted files per run | Exactly 1, for every run | S1 run record, `DATA_BLOCK/FILES/FILE` |

**Sequencing instruments** (S1 experiment record, `PLATFORM` and `INSTRUMENT_MODEL`; all 80,892 experiments):

| Platform, instrument | Count | Share |
|---|---|---|
| OXFORD_NANOPORE, MinION | 63,842 | 78.9% |
| ILLUMINA, Illumina MiSeq | 16,681 | 20.6% |
| OXFORD_NANOPORE, GridION | 369 | 0.5% |

Cross-check: S3 gives, for all 80,892 runs, OXFORD_NANOPORE, MinION 63,842 (78.9%); ILLUMINA, MiSeq 16,681 (20.6%); OXFORD_NANOPORE, GridION 369 (0.5%).

**Centre name on each run record** (S1 run record, attribute `center_name`; all 80,892 runs):

| Centre name | Count | Share |
|---|---|---|
| Irish Consortium for Sequencing Covid | 80,892 | 100.0% |

**Year each run was first made public at ENA** (S1 run record, `ENA-FIRST-PUBLIC`; all 80,892 runs):

| Year | Count | Share |
|---|---|---|
| 2020 | 802 | 1.0% |
| 2021 | 41,478 | 51.3% |
| 2022 | 34,801 | 43.0% |
| 2023 | 3,773 | 4.7% |
| 2024 | 38 | 0.0% |

**Amount of sequence** (S1 run record, `ENA-SPOT-COUNT` for reads and `ENA-BASE-COUNT` for bases; all 80,892 runs):

| Fact | Value |
|---|---|
| Runs with a read count in ENA's record | 80,867 of 80,892 |
| Total reads | 21,270,413,522 |
| Total bases | 3,553,411,432,580 |

**Per run, by instrument** (same fields, joined to the experiment record for the instrument). "Typical" is the median. The range is the 5th to the 95th percentile. Mean read length is bases divided by reads.

| Instrument | Runs | Typical reads per run | Typical mean read length | Typical nominal depth | Range of nominal depth |
|---|---|---|---|---|---|
| OXFORD_NANOPORE, MinION | 63,817 | 21,753 | 962 bases | 703x | 482x to 1,358x |
| ILLUMINA, Illumina MiSeq | 16,681 | 1,252,048 | 90 bases | 3,847x | 640x to 8,483x |
| OXFORD_NANOPORE, GridION | 369 | 19,600 | 509 bases | 334x | 312x to 1,307x |
| All instruments | 80,867 | 22,189 | 949 bases | 721x | 485x to 8,388x |

**File size.** ENA's own file sizes come from the Portal API and are not available. NCBI's copies add up to 1,301 GB for the 80,199 runs NCBI has loaded (S3, column `size_MB`). ENA's files are a different format, and ENA holds more reads than NCBI for some runs (section 9), so treat this only as a rough guide: **the study is well over 1 TB.**

**Cross-check of ENA's counts against NCBI's** (S1 `ENA-SPOT-COUNT` and `ENA-BASE-COUNT` against S3 `spots` and `bases`, for runs that have counts in both):

| Instrument | Runs compared | Reads and bases identical | ENA has more reads | ENA has fewer reads |
|---|---|---|---|---|
| OXFORD_NANOPORE, MinION | 63,817 | 63,724 (99.9%) | 93 | 0 |
| ILLUMINA, Illumina MiSeq | 15,988 | 5,198 (32.5%) | 10,790 | 0 |
| OXFORD_NANOPORE, GridION | 369 | 369 (100.0%) | 0 | 0 |

**What "nominal depth" means.** It is the total number of bases in a run divided by 29,903, the length of the SARS-CoV-2 reference genome (MN908947.3). It says how many times the genome would be covered if every read were viral and the reads were spread evenly. Neither is guaranteed. Amplicon sequencing covers some regions far more than others. Real coverage has **not** been measured: that needs the reads to be aligned to the reference genome, which has not been done.

## 5. The whole study: samples and laboratory protocol

**Samples.** Evidence: S1, ENA's sample record for all 80,892 samples, saved as `full_study_tables/ena_samples.csv`. The field named in each heading is the field in ENA's record.

| Fact | Value | Evidence |
|---|---|---|
| Earliest collection date | 2020-03-13 | Sample attribute `collection date` (written `collection_date` on some records) |
| Latest collection date | 2024-01-09 | Same |
| Samples with a usable collection date | 80,701 of 80,892 | Same |
| Samples with a patient identifier | 0 of 80,892 | Sample attribute `host subject id`: "not provided" on 80,892 |
| Latitude and longitude | The same on every sample: 53.1424 and 7.6921 | Sample attributes `geographic location (latitude)` and `geographic location (longitude)` |

Collection year (`collection date`):

| Year | Count | Share |
|---|---|---|
| 2020 | 1,576 | 1.9% |
| 2021 | 45,973 | 56.8% |
| 2022 | 30,055 | 37.2% |
| 2023 | 3,062 | 3.8% |
| 2024 | 35 | 0.0% |
| not a usable date (see section 9) | 191 | 0.2% |

Country (`geographic location (country and/or sea)`):

| Value | Count | Share |
|---|---|---|
| Ireland | 80,892 | 100.0% |

County (`geographic location (region and locality)`, with the leading "Europe / Ireland /" removed):

| Value | Count | Share |
|---|---|---|
| Dublin | 24,375 | 30.1% |
| Cork | 6,093 | 7.5% |
| Kildare | 4,907 | 6.1% |
| Louth | 4,085 | 5.0% |
| Meath | 3,655 | 4.5% |
| Tipperary | 3,116 | 3.9% |
| Limerick | 2,825 | 3.5% |
| Galway | 2,811 | 3.5% |
| Kilkenny | 2,546 | 3.1% |
| Donegal | 2,375 | 2.9% |
| Carlow | 2,028 | 2.5% |
| Laois | 1,981 | 2.4% |
| Wicklow | 1,981 | 2.4% |
| Offaly | 1,945 | 2.4% |
| Wexford | 1,880 | 2.3% |
| Waterford | 1,836 | 2.3% |
| Westmeath | 1,795 | 2.2% |
| Cavan | 1,760 | 2.2% |
| Monaghan | 1,682 | 2.1% |
| Kerry | 1,448 | 1.8% |
| Clare | 1,207 | 1.5% |
| Roscommon | 1,139 | 1.4% |
| Sligo | 1,115 | 1.4% |
| Mayo | 1,083 | 1.3% |
| Longford | 657 | 0.8% |
| Leitrim | 375 | 0.5% |
| Leinster | 175 | 0.2% |
| Europe / Ireland | 16 | 0.0% |
| #N/A | 1 | 0.0% |

Host (`host scientific name`):

| Value | Count | Share |
|---|---|---|
| Homo sapiens | 80,892 | 100.0% |

Host sex (`host sex`):

| Value | Count | Share |
|---|---|---|
| female | 42,987 | 53.1% |
| male | 37,447 | 46.3% |
| not provided | 458 | 0.6% |

Host age band (`host age`):

| Value | Count | Share |
|---|---|---|
| 0-100 | 15,048 | 18.6% |
| 31-40 | 14,503 | 17.9% |
| 21-30 | 13,652 | 16.9% |
| 41-50 | 13,509 | 16.7% |
| 51-60 | 9,460 | 11.7% |
| 61-70 | 5,242 | 6.5% |
| 11-20 | 4,389 | 5.4% |
| 71-80 | 2,616 | 3.2% |
| 85+ | 838 | 1.0% |
| 81-90 | 712 | 0.9% |
| 1-100 | 105 | 0.1% |
| 41 - 50 | 75 | 0.1% |
| 51 - 60 | 70 | 0.1% |
| 31 - 40 | 69 | 0.1% |
| 20-29 | 66 | 0.1% |
| 81 - 90 | 65 | 0.1% |
| 30-39 | 60 | 0.1% |
| 21 - 30 | 58 | 0.1% |
| 18-100 | 56 | 0.1% |
| 61 - 70 | 51 | 0.1% |
| (22 other values) | 248 | 0.3% |

Host health state (`host health state`):

| Value | Count | Share |
|---|---|---|
| not provided | 80,892 | 100.0% |

What was swabbed (`isolation source host-associated`):

| Value | Count | Share |
|---|---|---|
| Oro-Nasopharyngeal swab | 80,892 | 100.0% |

Why the sample was taken (`sample capture status`):

| Value | Count | Share |
|---|---|---|
| active surveillance in response to outbreak | 80,892 | 100.0% |

Collecting institution (`collecting institution`):

| Value | Count | Share |
|---|---|---|
| National Virus Reference Laboratory | 80,752 | 99.8% |
| CEPHR / Vincent's Hospital | 130 | 0.2% |
| CEPHR / Mater Hospital | 10 | 0.0% |

Centre name on the sample record (attribute `center_name`):

| Value | Count | Share |
|---|---|---|
| NVRL | 78,724 | 97.3% |
| Irish Consortium for Sequencing Covid | 1,568 | 1.9% |
| Teagasc Moorepark | 447 | 0.6% |
| UCD National Virus Reference Laboratory | 132 | 0.2% |
| Teagasc Oakpark | 21 | 0.0% |

ENA sample checklist (`ENA-CHECKLIST`):

| Value | Count | Share |
|---|---|---|
| ERC000011 | 42,731 | 52.8% |
| ERC000033 | 38,161 | 47.2% |

**Laboratory protocol.** Evidence: S1, ENA's experiment record for all 80,892 experiments, saved as `full_study_tables/ena_experiments.csv`. This is what the submitter wrote. It has not been checked against the reads, and section 9 gives a reason to doubt it.

Instrument and `LIBRARY_CONSTRUCTION_PROTOCOL`:

| Instrument: protocol as recorded | Count | Share |
|---|---|---|
| OXFORD_NANOPORE, MinION: (none given) | 33,876 | 41.9% |
| OXFORD_NANOPORE, MinION: Artic protocol version 3 | 29,952 | 37.0% |
| ILLUMINA, Illumina MiSeq: (none given) | 8,855 | 10.9% |
| ILLUMINA, Illumina MiSeq: Artic protocol version 3 | 7,826 | 9.7% |
| OXFORD_NANOPORE, GridION: Artic protocol version 3 | 369 | 0.5% |
| OXFORD_NANOPORE, MinION: Artic protocol, a version other than 3 (see the note below) | 14 | 0.0% |

`DESIGN_DESCRIPTION`:

| Design description as recorded | Count | Share |
|---|---|---|
| (none given) | 42,731 | 52.8% |
| hCov-19 MinION reads obtained following the Artic v3 protocol | 28,971 | 35.8% |
| hCov-19 Illumina reads obtained following the Artic v3 protocol | 4,403 | 5.4% |
| hCov-19 Illumina MiSeq reads obtained following the Artic v3 protocol | 3,423 | 4.2% |
| hCoV-19 ONT reads obtained following the Artic protocol | 652 | 0.8% |
| nCoV19 GridION reads obtained following the Artic v3 protocol | 368 | 0.5% |
| hCov-19 Oxford Nanopore MinION reads obtained following the Artic v3 protocol | 244 | 0.3% |
| nCoV19 MinION reads obtained following the Artic v3 protocol | 100 | 0.1% |

14 experiments give a protocol version other than 3: ERX4723841 to ERX4723854, with versions 4 to 17. The accessions are consecutive and the version rises by one on each. That is the pattern a spreadsheet makes when a cell is dragged down, so these are probably a slip in the submission and not real protocol versions.

## 6. Runs, samples and patients

- A **run** is one output of a sequencing machine. Here, one run is one file.
- A **sample** is one swab. In this study every sample has exactly one run, so 80,892 runs means 80,892 samples.
- A **patient** is a person. One person can be swabbed more than once.

ENA's sample records have a field for a patient identifier, `host subject id`. In all 80,892 sample records, that field holds no identifier (S1; the values are listed in section 5). NCBI's table has a `Subject_ID` column and it is empty for all 80,892 runs (S3).

**So the number of patients cannot be counted from the public records.** It cannot be more than 80,892, and it may be fewer, because repeat swabs of the same person cannot be detected.

## 7. The five downloaded files

These are the first five runs that EBI Search (S4) returned for the study. They were chosen only because they came first. **They are not a representative sample of the study.** All five are from the same submission, the same laboratory, the same instrument type and the same two days.

| File | Size | Reads | Bases | Median read length | Nominal depth | Collected | County | Host sex, age band |
|---|---|---|---|---|---|---|---|---|
| `ERR7112279.fastq.gz` | 16.3 MB | 22,868 | 22,836,099 | 1,045 bases | 764x | 2021-09-02 | Dublin | male, 41-50 |
| `ERR7112281.fastq.gz` | 15.9 MB | 22,109 | 22,247,836 | 1,059 bases | 744x | 2021-09-02 | Dublin | female, 11-20 |
| `ERR7112289.fastq.gz` | 14.4 MB | 20,922 | 20,009,790 | 995 bases | 669x | 2021-09-03 | Meath | male, 41-50 |
| `ERR7112290.fastq.gz` | 13.0 MB | 18,742 | 18,110,726 | 1,005 bases | 606x | 2021-09-02 | Meath | female, 0-100 |
| `ERR7112291.fastq.gz` | 15.7 MB | 22,208 | 21,846,289 | 1,025 bases | 731x | 2021-09-02 | Kildare | male, 41-50 |

Total on disk: 75.4 MB. Every value in this table is repeated, with its evidence, in the descriptor for each file below.

### `ERR7112279.fastq.gz`

**In one sentence:** Oxford Nanopore MinION amplicon reads of SARS-CoV-2 from one oro-nasopharyngeal swab collected on 2021-09-02 in Dublin, Ireland, recorded as from a male person in age band 41-50; 22,868 reads, 22,836,099 bases.

ENA's records for this file (S1), saved in `ena_records/`:

- Run record: `ERR7112279.run.xml`
- Experiment record: `ERR7112279.experiment_ERX6681205.xml`
- Sample record: `ERR7112279.sample_ERS7696215.xml`

| Field | Value | Evidence |
|---|---|---|
| **Identity** |  |  |
| Run accession | ERR7112279 | Run record |
| Experiment accession | ERX6681205 | Run record, `EXPERIMENT_REF` |
| Sample accession | ERS7696215 (also known as SAMEA10017991) | Run record, link `ENA-SAMPLE`; sample record |
| Study | PRJEB40277 (also known as ERP123896) | Run record, link `ENA-STUDY` |
| Submission | ERA6738186 | Run record, link `ENA-SUBMISSION` |
| Laboratory's own sample name | M36IRL91859 | Sample record, attribute `alias` |
| Virus name | hCoV-19/Ireland/D-NVRL-M36IRL91859/2021 | Sample record, `virus identifier` |
| **The sample** |  |  |
| Organism | Severe acute respiratory syndrome coronavirus 2 (taxonomy ID 2697049) | Sample record, `SAMPLE_NAME` |
| Host | Homo sapiens | Sample record, `host scientific name` |
| What was swabbed | Oro-Nasopharyngeal swab | Sample record, `isolation source host-associated` |
| Collection date | 2021-09-02 | Sample record, `collection date` |
| Country | Ireland | Sample record, `geographic location (country and/or sea)` |
| Region and locality | Europe / Ireland / Dublin | Sample record, `geographic location (region and locality)` |
| Latitude, longitude as recorded | 53.1424, 7.6921 (a placeholder, see section 9) | Sample record, `geographic location (latitude)` and `(longitude)` |
| Host sex | male | Sample record, `host sex` |
| Host age band | 41-50 | Sample record, `host age` |
| Host health state | not provided | Sample record, `host health state` |
| Patient identifier | not provided | Sample record, `host subject id` |
| Why the sample was taken | active surveillance in response to outbreak | Sample record, `sample capture status` |
| Collecting institution | National Virus Reference Laboratory | Sample record, `collecting institution` |
| **The sequencing** |  |  |
| Platform and instrument | OXFORD_NANOPORE, MinION | Experiment record, `PLATFORM` |
| Library strategy | AMPLICON | Experiment record, `LIBRARY_STRATEGY` |
| Library source | GENOMIC | Experiment record, `LIBRARY_SOURCE` |
| Library selection | unspecified | Experiment record, `LIBRARY_SELECTION` |
| Library layout | SINGLE (one file, not paired) | Experiment record, `LIBRARY_LAYOUT` |
| Protocol as recorded | Artic protocol version 3 (does not match the read lengths, see section 9) | Experiment record, `LIBRARY_CONSTRUCTION_PROTOCOL` |
| Design description as recorded | hCov-19 MinION reads obtained following the Artic v3 protocol | Experiment record, `DESIGN_DESCRIPTION` |
| First made public at ENA | 2021-10-18 | Run record, `ENA-FIRST-PUBLIC` |
| **The reads** |  |  |
| Reads, by ENA's record | 22,868 | Run record, `ENA-SPOT-COUNT` |
| Reads, counted in the file | 22,868 (equal) | S5 |
| Bases, by ENA's record | 22,836,099 | Run record, `ENA-BASE-COUNT` |
| Bases, counted in the file | 22,836,099 (equal) | S5 |
| Read length: shortest, median, mean, longest | 250, 1,045, 999, 1,494 bases | S5 |
| Read length N50 | 1,081 bases (half of all bases are in reads at least this long) | S5 |
| Mean base quality | Q13.7 (Phred scale, averaged over error probabilities) | S5 |
| Nominal depth | 764x (bases divided by 29,903; not measured coverage, see section 4) | S5 |
| **The file** |  |  |
| Path on this machine | `data/PRJEB40277/ERR7112279.fastq.gz` | S5 |
| Downloaded from | https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR711/009/ERR7112279/ERR7112279.fastq.gz | S2 |
| Downloaded at | 2026-10-04 20:06 UTC | S5, the file's timestamp |
| Format | FASTQ, gzip-compressed, one file, 4 lines per read | S5 |
| Size | 16,313,331 bytes (equal to the size on the ENA file server) | S5 against S2 |
| MD5 of the file on disk | `3dbd29bc69ed67195b649e5be8e9fc17` | S5. Not yet compared with ENA's own MD5, see section 8 |
| Original submitted file | M36IRL91859.fastq.gz | Run record, `DATA_BLOCK/FILES/FILE` |
| MD5 of the submitted file, by ENA's record | `9f93a8227fd5a90e004044df1ed1ca84` | Run record, attribute `checksum` |
| Submitted file fetched and its MD5 checked | Yes, it matches | S2 against the run record |
| Reads identical to the submitted file | Yes, every read, in sequence and quality | S5 |

### `ERR7112281.fastq.gz`

**In one sentence:** Oxford Nanopore MinION amplicon reads of SARS-CoV-2 from one oro-nasopharyngeal swab collected on 2021-09-02 in Dublin, Ireland, recorded as from a female person in age band 11-20; 22,109 reads, 22,247,836 bases.

ENA's records for this file (S1), saved in `ena_records/`:

- Run record: `ERR7112281.run.xml`
- Experiment record: `ERR7112281.experiment_ERX6681207.xml`
- Sample record: `ERR7112281.sample_ERS7696217.xml`

| Field | Value | Evidence |
|---|---|---|
| **Identity** |  |  |
| Run accession | ERR7112281 | Run record |
| Experiment accession | ERX6681207 | Run record, `EXPERIMENT_REF` |
| Sample accession | ERS7696217 (also known as SAMEA10017993) | Run record, link `ENA-SAMPLE`; sample record |
| Study | PRJEB40277 (also known as ERP123896) | Run record, link `ENA-STUDY` |
| Submission | ERA6738186 | Run record, link `ENA-SUBMISSION` |
| Laboratory's own sample name | M36IRL93075 | Sample record, attribute `alias` |
| Virus name | hCoV-19/Ireland/D-NVRL-M36IRL93075/2021 | Sample record, `virus identifier` |
| **The sample** |  |  |
| Organism | Severe acute respiratory syndrome coronavirus 2 (taxonomy ID 2697049) | Sample record, `SAMPLE_NAME` |
| Host | Homo sapiens | Sample record, `host scientific name` |
| What was swabbed | Oro-Nasopharyngeal swab | Sample record, `isolation source host-associated` |
| Collection date | 2021-09-02 | Sample record, `collection date` |
| Country | Ireland | Sample record, `geographic location (country and/or sea)` |
| Region and locality | Europe / Ireland / Dublin | Sample record, `geographic location (region and locality)` |
| Latitude, longitude as recorded | 53.1424, 7.6921 (a placeholder, see section 9) | Sample record, `geographic location (latitude)` and `(longitude)` |
| Host sex | female | Sample record, `host sex` |
| Host age band | 11-20 | Sample record, `host age` |
| Host health state | not provided | Sample record, `host health state` |
| Patient identifier | not provided | Sample record, `host subject id` |
| Why the sample was taken | active surveillance in response to outbreak | Sample record, `sample capture status` |
| Collecting institution | National Virus Reference Laboratory | Sample record, `collecting institution` |
| **The sequencing** |  |  |
| Platform and instrument | OXFORD_NANOPORE, MinION | Experiment record, `PLATFORM` |
| Library strategy | AMPLICON | Experiment record, `LIBRARY_STRATEGY` |
| Library source | GENOMIC | Experiment record, `LIBRARY_SOURCE` |
| Library selection | unspecified | Experiment record, `LIBRARY_SELECTION` |
| Library layout | SINGLE (one file, not paired) | Experiment record, `LIBRARY_LAYOUT` |
| Protocol as recorded | Artic protocol version 3 (does not match the read lengths, see section 9) | Experiment record, `LIBRARY_CONSTRUCTION_PROTOCOL` |
| Design description as recorded | hCov-19 MinION reads obtained following the Artic v3 protocol | Experiment record, `DESIGN_DESCRIPTION` |
| First made public at ENA | 2021-10-18 | Run record, `ENA-FIRST-PUBLIC` |
| **The reads** |  |  |
| Reads, by ENA's record | 22,109 | Run record, `ENA-SPOT-COUNT` |
| Reads, counted in the file | 22,109 (equal) | S5 |
| Bases, by ENA's record | 22,247,836 | Run record, `ENA-BASE-COUNT` |
| Bases, counted in the file | 22,247,836 (equal) | S5 |
| Read length: shortest, median, mean, longest | 254, 1,059, 1,006, 1,487 bases | S5 |
| Read length N50 | 1,089 bases (half of all bases are in reads at least this long) | S5 |
| Mean base quality | Q13.7 (Phred scale, averaged over error probabilities) | S5 |
| Nominal depth | 744x (bases divided by 29,903; not measured coverage, see section 4) | S5 |
| **The file** |  |  |
| Path on this machine | `data/PRJEB40277/ERR7112281.fastq.gz` | S5 |
| Downloaded from | https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR711/001/ERR7112281/ERR7112281.fastq.gz | S2 |
| Downloaded at | 2026-10-04 20:06 UTC | S5, the file's timestamp |
| Format | FASTQ, gzip-compressed, one file, 4 lines per read | S5 |
| Size | 15,901,994 bytes (equal to the size on the ENA file server) | S5 against S2 |
| MD5 of the file on disk | `4a14275ab221c850c3c3969120702bf2` | S5. Not yet compared with ENA's own MD5, see section 8 |
| Original submitted file | M36IRL93075.fastq.gz | Run record, `DATA_BLOCK/FILES/FILE` |
| MD5 of the submitted file, by ENA's record | `1b887737256b94c98a4793919e7a059d` | Run record, attribute `checksum` |
| Submitted file fetched and its MD5 checked | Yes, it matches | S2 against the run record |
| Reads identical to the submitted file | Yes, every read, in sequence and quality | S5 |

### `ERR7112289.fastq.gz`

**In one sentence:** Oxford Nanopore MinION amplicon reads of SARS-CoV-2 from one oro-nasopharyngeal swab collected on 2021-09-03 in Meath, Ireland, recorded as from a male person in age band 41-50; 20,922 reads, 20,009,790 bases.

ENA's records for this file (S1), saved in `ena_records/`:

- Run record: `ERR7112289.run.xml`
- Experiment record: `ERR7112289.experiment_ERX6681215.xml`
- Sample record: `ERR7112289.sample_ERS7696225.xml`

| Field | Value | Evidence |
|---|---|---|
| **Identity** |  |  |
| Run accession | ERR7112289 | Run record |
| Experiment accession | ERX6681215 | Run record, `EXPERIMENT_REF` |
| Sample accession | ERS7696225 (also known as SAMEA10018001) | Run record, link `ENA-SAMPLE`; sample record |
| Study | PRJEB40277 (also known as ERP123896) | Run record, link `ENA-STUDY` |
| Submission | ERA6738186 | Run record, link `ENA-SUBMISSION` |
| Laboratory's own sample name | M37IRL03760 | Sample record, attribute `alias` |
| Virus name | hCoV-19/Ireland/MH-NVRL-M37IRL03760/2021 | Sample record, `virus identifier` |
| **The sample** |  |  |
| Organism | Severe acute respiratory syndrome coronavirus 2 (taxonomy ID 2697049) | Sample record, `SAMPLE_NAME` |
| Host | Homo sapiens | Sample record, `host scientific name` |
| What was swabbed | Oro-Nasopharyngeal swab | Sample record, `isolation source host-associated` |
| Collection date | 2021-09-03 | Sample record, `collection date` |
| Country | Ireland | Sample record, `geographic location (country and/or sea)` |
| Region and locality | Europe / Ireland / Meath | Sample record, `geographic location (region and locality)` |
| Latitude, longitude as recorded | 53.1424, 7.6921 (a placeholder, see section 9) | Sample record, `geographic location (latitude)` and `(longitude)` |
| Host sex | male | Sample record, `host sex` |
| Host age band | 41-50 | Sample record, `host age` |
| Host health state | not provided | Sample record, `host health state` |
| Patient identifier | not provided | Sample record, `host subject id` |
| Why the sample was taken | active surveillance in response to outbreak | Sample record, `sample capture status` |
| Collecting institution | National Virus Reference Laboratory | Sample record, `collecting institution` |
| **The sequencing** |  |  |
| Platform and instrument | OXFORD_NANOPORE, MinION | Experiment record, `PLATFORM` |
| Library strategy | AMPLICON | Experiment record, `LIBRARY_STRATEGY` |
| Library source | GENOMIC | Experiment record, `LIBRARY_SOURCE` |
| Library selection | unspecified | Experiment record, `LIBRARY_SELECTION` |
| Library layout | SINGLE (one file, not paired) | Experiment record, `LIBRARY_LAYOUT` |
| Protocol as recorded | Artic protocol version 3 (does not match the read lengths, see section 9) | Experiment record, `LIBRARY_CONSTRUCTION_PROTOCOL` |
| Design description as recorded | hCov-19 MinION reads obtained following the Artic v3 protocol | Experiment record, `DESIGN_DESCRIPTION` |
| First made public at ENA | 2021-10-18 | Run record, `ENA-FIRST-PUBLIC` |
| **The reads** |  |  |
| Reads, by ENA's record | 20,922 | Run record, `ENA-SPOT-COUNT` |
| Reads, counted in the file | 20,922 (equal) | S5 |
| Bases, by ENA's record | 20,009,790 | Run record, `ENA-BASE-COUNT` |
| Bases, counted in the file | 20,009,790 (equal) | S5 |
| Read length: shortest, median, mean, longest | 253, 995, 956, 1,487 bases | S5 |
| Read length N50 | 1,044 bases (half of all bases are in reads at least this long) | S5 |
| Mean base quality | Q13.5 (Phred scale, averaged over error probabilities) | S5 |
| Nominal depth | 669x (bases divided by 29,903; not measured coverage, see section 4) | S5 |
| **The file** |  |  |
| Path on this machine | `data/PRJEB40277/ERR7112289.fastq.gz` | S5 |
| Downloaded from | https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR711/009/ERR7112289/ERR7112289.fastq.gz | S2 |
| Downloaded at | 2026-10-04 20:06 UTC | S5, the file's timestamp |
| Format | FASTQ, gzip-compressed, one file, 4 lines per read | S5 |
| Size | 14,428,927 bytes (equal to the size on the ENA file server) | S5 against S2 |
| MD5 of the file on disk | `2ad668ae30c9c78332ca0016706b69c2` | S5. Not yet compared with ENA's own MD5, see section 8 |
| Original submitted file | M37IRL03760.fastq.gz | Run record, `DATA_BLOCK/FILES/FILE` |
| MD5 of the submitted file, by ENA's record | `c397a4e5c586806875cec508efcf0802` | Run record, attribute `checksum` |
| Submitted file fetched and its MD5 checked | Yes, it matches | S2 against the run record |
| Reads identical to the submitted file | Yes, every read, in sequence and quality | S5 |

### `ERR7112290.fastq.gz`

**In one sentence:** Oxford Nanopore MinION amplicon reads of SARS-CoV-2 from one oro-nasopharyngeal swab collected on 2021-09-02 in Meath, Ireland, recorded as from a female person in age band 0-100; 18,742 reads, 18,110,726 bases.

ENA's records for this file (S1), saved in `ena_records/`:

- Run record: `ERR7112290.run.xml`
- Experiment record: `ERR7112290.experiment_ERX6681216.xml`
- Sample record: `ERR7112290.sample_ERS7696226.xml`

| Field | Value | Evidence |
|---|---|---|
| **Identity** |  |  |
| Run accession | ERR7112290 | Run record |
| Experiment accession | ERX6681216 | Run record, `EXPERIMENT_REF` |
| Sample accession | ERS7696226 (also known as SAMEA10018002) | Run record, link `ENA-SAMPLE`; sample record |
| Study | PRJEB40277 (also known as ERP123896) | Run record, link `ENA-STUDY` |
| Submission | ERA6738186 | Run record, link `ENA-SUBMISSION` |
| Laboratory's own sample name | M36IRL92731 | Sample record, attribute `alias` |
| Virus name | hCoV-19/Ireland/MH-NVRL-M36IRL92731/2021 | Sample record, `virus identifier` |
| **The sample** |  |  |
| Organism | Severe acute respiratory syndrome coronavirus 2 (taxonomy ID 2697049) | Sample record, `SAMPLE_NAME` |
| Host | Homo sapiens | Sample record, `host scientific name` |
| What was swabbed | Oro-Nasopharyngeal swab | Sample record, `isolation source host-associated` |
| Collection date | 2021-09-02 | Sample record, `collection date` |
| Country | Ireland | Sample record, `geographic location (country and/or sea)` |
| Region and locality | Europe / Ireland / Meath | Sample record, `geographic location (region and locality)` |
| Latitude, longitude as recorded | 53.1424, 7.6921 (a placeholder, see section 9) | Sample record, `geographic location (latitude)` and `(longitude)` |
| Host sex | female | Sample record, `host sex` |
| Host age band | 0-100 (covers every age, so gives no information) | Sample record, `host age` |
| Host health state | not provided | Sample record, `host health state` |
| Patient identifier | not provided | Sample record, `host subject id` |
| Why the sample was taken | active surveillance in response to outbreak | Sample record, `sample capture status` |
| Collecting institution | National Virus Reference Laboratory | Sample record, `collecting institution` |
| **The sequencing** |  |  |
| Platform and instrument | OXFORD_NANOPORE, MinION | Experiment record, `PLATFORM` |
| Library strategy | AMPLICON | Experiment record, `LIBRARY_STRATEGY` |
| Library source | GENOMIC | Experiment record, `LIBRARY_SOURCE` |
| Library selection | unspecified | Experiment record, `LIBRARY_SELECTION` |
| Library layout | SINGLE (one file, not paired) | Experiment record, `LIBRARY_LAYOUT` |
| Protocol as recorded | Artic protocol version 3 (does not match the read lengths, see section 9) | Experiment record, `LIBRARY_CONSTRUCTION_PROTOCOL` |
| Design description as recorded | hCov-19 MinION reads obtained following the Artic v3 protocol | Experiment record, `DESIGN_DESCRIPTION` |
| First made public at ENA | 2021-10-18 | Run record, `ENA-FIRST-PUBLIC` |
| **The reads** |  |  |
| Reads, by ENA's record | 18,742 | Run record, `ENA-SPOT-COUNT` |
| Reads, counted in the file | 18,742 (equal) | S5 |
| Bases, by ENA's record | 18,110,726 | Run record, `ENA-BASE-COUNT` |
| Bases, counted in the file | 18,110,726 (equal) | S5 |
| Read length: shortest, median, mean, longest | 250, 1,005, 966, 1,442 bases | S5 |
| Read length N50 | 1,047 bases (half of all bases are in reads at least this long) | S5 |
| Mean base quality | Q13.6 (Phred scale, averaged over error probabilities) | S5 |
| Nominal depth | 606x (bases divided by 29,903; not measured coverage, see section 4) | S5 |
| **The file** |  |  |
| Path on this machine | `data/PRJEB40277/ERR7112290.fastq.gz` | S5 |
| Downloaded from | https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR711/000/ERR7112290/ERR7112290.fastq.gz | S2 |
| Downloaded at | 2026-10-04 20:06 UTC | S5, the file's timestamp |
| Format | FASTQ, gzip-compressed, one file, 4 lines per read | S5 |
| Size | 13,038,654 bytes (equal to the size on the ENA file server) | S5 against S2 |
| MD5 of the file on disk | `1184ff6a6ba03e5e6e4715e6ba6ee5cf` | S5. Not yet compared with ENA's own MD5, see section 8 |
| Original submitted file | M36IRL92731.fastq.gz | Run record, `DATA_BLOCK/FILES/FILE` |
| MD5 of the submitted file, by ENA's record | `cb4d97199e6c266440c76f0607db9166` | Run record, attribute `checksum` |
| Submitted file fetched and its MD5 checked | Yes, it matches | S2 against the run record |
| Reads identical to the submitted file | Yes, every read, in sequence and quality | S5 |

### `ERR7112291.fastq.gz`

**In one sentence:** Oxford Nanopore MinION amplicon reads of SARS-CoV-2 from one oro-nasopharyngeal swab collected on 2021-09-02 in Kildare, Ireland, recorded as from a male person in age band 41-50; 22,208 reads, 21,846,289 bases.

ENA's records for this file (S1), saved in `ena_records/`:

- Run record: `ERR7112291.run.xml`
- Experiment record: `ERR7112291.experiment_ERX6681217.xml`
- Sample record: `ERR7112291.sample_ERS7696227.xml`

| Field | Value | Evidence |
|---|---|---|
| **Identity** |  |  |
| Run accession | ERR7112291 | Run record |
| Experiment accession | ERX6681217 | Run record, `EXPERIMENT_REF` |
| Sample accession | ERS7696227 (also known as SAMEA10018003) | Run record, link `ENA-SAMPLE`; sample record |
| Study | PRJEB40277 (also known as ERP123896) | Run record, link `ENA-STUDY` |
| Submission | ERA6738186 | Run record, link `ENA-SUBMISSION` |
| Laboratory's own sample name | M36IRL92315 | Sample record, attribute `alias` |
| Virus name | hCoV-19/Ireland/KE-NVRL-M36IRL92315/2021 | Sample record, `virus identifier` |
| **The sample** |  |  |
| Organism | Severe acute respiratory syndrome coronavirus 2 (taxonomy ID 2697049) | Sample record, `SAMPLE_NAME` |
| Host | Homo sapiens | Sample record, `host scientific name` |
| What was swabbed | Oro-Nasopharyngeal swab | Sample record, `isolation source host-associated` |
| Collection date | 2021-09-02 | Sample record, `collection date` |
| Country | Ireland | Sample record, `geographic location (country and/or sea)` |
| Region and locality | Europe / Ireland / Kildare | Sample record, `geographic location (region and locality)` |
| Latitude, longitude as recorded | 53.1424, 7.6921 (a placeholder, see section 9) | Sample record, `geographic location (latitude)` and `(longitude)` |
| Host sex | male | Sample record, `host sex` |
| Host age band | 41-50 | Sample record, `host age` |
| Host health state | not provided | Sample record, `host health state` |
| Patient identifier | not provided | Sample record, `host subject id` |
| Why the sample was taken | active surveillance in response to outbreak | Sample record, `sample capture status` |
| Collecting institution | National Virus Reference Laboratory | Sample record, `collecting institution` |
| **The sequencing** |  |  |
| Platform and instrument | OXFORD_NANOPORE, MinION | Experiment record, `PLATFORM` |
| Library strategy | AMPLICON | Experiment record, `LIBRARY_STRATEGY` |
| Library source | GENOMIC | Experiment record, `LIBRARY_SOURCE` |
| Library selection | unspecified | Experiment record, `LIBRARY_SELECTION` |
| Library layout | SINGLE (one file, not paired) | Experiment record, `LIBRARY_LAYOUT` |
| Protocol as recorded | Artic protocol version 3 (does not match the read lengths, see section 9) | Experiment record, `LIBRARY_CONSTRUCTION_PROTOCOL` |
| Design description as recorded | hCov-19 MinION reads obtained following the Artic v3 protocol | Experiment record, `DESIGN_DESCRIPTION` |
| First made public at ENA | 2021-10-18 | Run record, `ENA-FIRST-PUBLIC` |
| **The reads** |  |  |
| Reads, by ENA's record | 22,208 | Run record, `ENA-SPOT-COUNT` |
| Reads, counted in the file | 22,208 (equal) | S5 |
| Bases, by ENA's record | 21,846,289 | Run record, `ENA-BASE-COUNT` |
| Bases, counted in the file | 21,846,289 (equal) | S5 |
| Read length: shortest, median, mean, longest | 250, 1,025, 984, 1,495 bases | S5 |
| Read length N50 | 1,066 bases (half of all bases are in reads at least this long) | S5 |
| Mean base quality | Q13.7 (Phred scale, averaged over error probabilities) | S5 |
| Nominal depth | 731x (bases divided by 29,903; not measured coverage, see section 4) | S5 |
| **The file** |  |  |
| Path on this machine | `data/PRJEB40277/ERR7112291.fastq.gz` | S5 |
| Downloaded from | https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR711/001/ERR7112291/ERR7112291.fastq.gz | S2 |
| Downloaded at | 2026-10-04 20:06 UTC | S5, the file's timestamp |
| Format | FASTQ, gzip-compressed, one file, 4 lines per read | S5 |
| Size | 15,674,682 bytes (equal to the size on the ENA file server) | S5 against S2 |
| MD5 of the file on disk | `611709a27a14adb41e0f6dbfe4de6ec1` | S5. Not yet compared with ENA's own MD5, see section 8 |
| Original submitted file | M36IRL92315.fastq.gz | Run record, `DATA_BLOCK/FILES/FILE` |
| MD5 of the submitted file, by ENA's record | `30567471a8aa1411b129accb2a1e92f4` | Run record, attribute `checksum` |
| Submitted file fetched and its MD5 checked | Yes, it matches | S2 against the run record |
| Reads identical to the submitted file | Yes, every read, in sequence and quality | S5 |

## 8. How the five files were checked

ENA's own MD5 checksum for each FASTQ file is not available while the Portal API is down. These checks were done instead. All five files passed all of them.

| Check | What it shows | Evidence |
|---|---|---|
| The size of each file on disk equals the size the ENA file server reports | The download was not cut short | S5 against S2 |
| `gzip -t` reports no error for each file | The compressed file is intact | S5 |
| The read count and base count measured in each file equal `ENA-SPOT-COUNT` and `ENA-BASE-COUNT` in ENA's run record | The file holds exactly the reads ENA says the run has | S5 against S1 (`ena_records/<run>.run.xml`) |
| The same two counts equal the `spots` and `bases` columns in NCBI's run table | A second archive agrees | S5 against S3 |
| The laboratory's original submitted file was fetched and its MD5 equals the checksum in ENA's run record | The original submission is intact at ENA | S2 against S1 (`DATA_BLOCK/FILES/FILE`, attribute `checksum`) |
| Every read in the downloaded file has the same sequence and the same quality string as a read in the original submitted file, and the two files hold the same number of reads | ENA's FASTQ file is the laboratory's reads with only the read names changed | S5 |
| ENA's run record names study ERP123896 for each run | Each file belongs to PRJEB40277 | S1 |

Two files exist at ENA for each run, and they are not byte-for-byte the same:

- The **submitted file** is what the laboratory uploaded, for example `M36IRL91859.fastq.gz`. Its MD5 is in ENA's run record.
- The **ENA FASTQ file** is what ENA produced from it, for example `ERR7112279.fastq.gz`. The reads are the same, but ENA renames them (`@ERR7112279.1 ...`). This is the file on this machine.

So the MD5 of the file on disk is not expected to equal the MD5 in ENA's run record. The MD5 of each file on disk is recorded in section 7 and in `downloaded_files.tsv`, so it can be compared with ENA's file report once that service is back.

The submitted files were fetched only to make these checks and were not kept.

## 9. Things to be aware of

1. **The recorded protocol does not match the read lengths.** ENA's experiment records for the five files say "Artic protocol version 3". ARTIC version 3 produces amplicons of about 400 bases. The reads in the five files are about 1,000 bases long, with none shorter than 250 or longer than 1,495 (S5). Reads that long are not what 400-base amplicons produce. This is not limited to the five files. 29,927 MinION runs have an experiment record that says "Artic protocol version 3" (S1). Taking each run's mean read length as `ENA-BASE-COUNT` divided by `ENA-SPOT-COUNT`: in 9,361 of them (31.3%) it is 600 bases or less, typically 506, which fits the label; in 20,566 (68.7%) it is over 600 bases, typically 973, which does not. Which primer scheme was really used has **not** been established. It matters for any later step that removes primer sequences.
2. **The coordinates are a placeholder.** 80,892 of the 80,892 sample records give latitude 53.1424 and longitude 7.6921, including all five downloaded samples (S1). One value shared by so many samples does not locate any of them. As written, with a positive longitude, the point is in mainland Europe, not Ireland. The centre of Ireland is at about 53.14 north, 7.69 **west**. Use the county in "region and locality" instead.
3. **"Library source: GENOMIC" is as recorded.** SARS-CoV-2 is an RNA virus. The value is what the submitter entered.
4. **Host age "0-100" gives no information.** It covers every age. One of the five downloaded samples has this value.
5. **The files are raw reads.** They have not been filtered for human reads, trimmed or aligned by anyone in this project. Whether the laboratory removed human reads before submitting is not stated in the records.
6. **ENA and NCBI do not always agree on read counts.** For 10,790 of the 15,988 Illumina MiSeq runs compared, ENA's record counts more reads than NCBI's, typically 4.0 times as many (section 4). The reason has not been established. ENA holds the original submission, so ENA's figures are the ones used in this document. ENA's own record gives no read count for 25 of all 80,892 runs; NCBI has a count for 25 of those. Separately, NCBI holds no counts at all for 693 runs, one block of accessions from ERR9891081 to ERR9891773, all Illumina MiSeq (S3: zero reads, zero bases, no load date). ENA's own records give a read count for 693 of the 693 of those fetched (S1). Six of them were looked up on the ENA file server and each has a FASTQ file there (S2).
7. **Some collection dates are not usable.** 191 of the 80,892 sample records have a collection date that cannot be used as written: "0021-04-05" on 46; "0021-04-16" on 32; "0021-04-04" on 31; "0021-04-13" on 28; "0021-04-12" on 16; "0021-04-17" on 10; and 7 other values (S1, `collection date`). A year of "0021" is presumably a typing slip for 2021, but that is a guess and the records have not been changed.
8. **The data are about people.** The records are public and carry no names, but they do carry sex, age band, county and collection date. Handle them accordingly.

## 10. Files in this folder

| File | What it is | In git? |
|---|---|---|
| `PRJEB40277_metadata.md` | This document | Yes |
| `downloaded_files.tsv` | One row per downloaded file, 56 columns. The same facts as section 7, for a program to read | Yes |
| `ena_records/PRJEB40277.study.xml` | ENA's study record, exactly as ENA returned it (S1) | Yes |
| `ena_records/<run>.run.xml` | ENA's run record for each of the five runs (S1) | Yes |
| `ena_records/<run>.experiment_<ERX>.xml` | ENA's experiment record for each of the five runs: how it was sequenced (S1) | Yes |
| `ena_records/<run>.sample_<ERS>.xml` | ENA's sample record for each of the five runs: what was swabbed, when and where (S1) | Yes |
| `full_study_tables/ncbi_sra_run_table.csv` | NCBI's run table for the whole study, 80,892 rows (S3) | No, 41 MB |
| `full_study_tables/ena_runs.csv` | ENA's run record for every run in the study, one row each, all 80,892 rows (S1) | No, large |
| `full_study_tables/ena_experiments.csv` | ENA's experiment record for every run in the study, one row each, all 80,892 rows (S1) | No, large |
| `full_study_tables/ena_samples.csv` | ENA's sample record for every run in the study, one row each, all 80,892 rows (S1) | No, large |

The sequence files themselves are in `data/PRJEB40277/` and are not in git.

## 11. Credit and terms

The data were submitted to ENA by the Irish Consortium for Sequencing Covid. Cite the study as ENA accession PRJEB40277, and each run by its own accession. The terms that apply to ENA data are recorded in `LICENSE.md` at the top of this repository and are still to be verified there.
