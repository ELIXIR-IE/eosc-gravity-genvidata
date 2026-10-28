# Primer files

| File | Scheme | Source | Licence |
|---|---|---|---|
| `artic_v3.bed` | ARTIC nCoV-2019 V3 (about 400 bp amplicons) | https://zenodo.org/record/4555735 (the file the IWC workflow tests use, SHA-1 d0864546dca524fc5cd057f48ee7f5671faba83a) | as in the Zenodo record |
| `midnight_1200_v1.bed` | Midnight 1200 bp amplicons, V1 (Freed et al. 2020, doi:10.1101/2020.05.28.122648) | `V1200/nCoV-2019.bed` inside `1200bp_amplicon_bed.tar.gz`, https://zenodo.org/record/3897530 | CC BY 4.0 |

## Which scheme each data set uses

Checked by mapping the reads to NC_045512.2 and counting how many reads start just after a left primer
and end just before a right primer (within 20 bp):

| Data | ARTIC v3 | ARTIC v4.1 | Midnight 1200 |
|---|---|---|---|
| Irish ERR7112279 (read median 1045 bp) | 20% / 7% | 10% / 7% | **51% / 35%** |
| Swedish SRR27033659 (read median 379 bp) | **46% / 44%** | 9% / 8% | 6% / 2% |

The Irish ENA record says "Artic v3 protocol", but the read lengths and read ends match the Midnight 1200 bp scheme.
