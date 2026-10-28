# GenViData results: ERR7112279

Run folder: `results/2026-10-28_1552`. Galaxy run id: `d071e794759ab192`.

## The Irish sample of concern

- **ERR7112279**, collected 2021-09-02 in Ireland.
- Lineage **AY.4** (Nextstrain clade 21J). Nextclade quality: good.
- 22868 reads mapped; 99.4% of the genome covered by at least 5 reads (mean depth 581).
- 46 variants with allele frequency of at least 0.75. Spike protein changes: T19R T95I G142D EFR156G L452R T478K D614G P681R D950N.

## Closest Swedish sequence

**OP458823** (swedish consensus, collected 2021-07-12, lineage AY.122) differs from the Irish sample at **14** positions.

SNP differences between the Irish sample and every Swedish sequence (fewer differences = more closely related):

| Swedish sequence | Data used | Collected | Lineage | SNP differences |
|---|---|---|---|---|
| OP458823 | consensus from ENA | 2021-07-12 | AY.122 | 14 |
| SRR27033646 | raw reads, processed here | 2021-07-26 | AY.122 | 17 |
| SRR27033647 | raw reads, processed here | 2021-07-24 | AY.94 | 19 |
| SRR27033648 | raw reads, processed here | 2021-07-23 | AY.9.2 | 34 |
| MZ848129 | consensus from ENA | 2021-08-10 | AY.9.2 | 38 |
| MZ846201 | consensus from ENA | 2021-08-10 | AY.9.2 | 41 |

## All sequences

| Accession | Country | Collected | Lineage | Clade | Nextclade QC | Genome covered (%) | Variants | Spike changes |
|---|---|---|---|---|---|---|---|---|
| ERR7112279 | Ireland | 2021-09-02 | AY.4 | 21J | good | 99.4 | 46 | T19R T95I G142D EFR156G L452R T478K D614G P681R D950N |
| SRR27033646 | Sweden: Uppsala County | 2021-07-26 | AY.122 | 21J | mediocre | 98.1 | 52 | T19R IHV68I R78K? D80I P82P? PV82PI A93S? G107W? Q115 Q115* L117 I119Y? EFR156G L452R T478K D614G P681R D950N |
| SRR27033647 | Sweden: Uppsala County | 2021-07-24 | AY.94 | 21J | good | 99.7 | 43 | T19R EFR156G L452R A475 T478K D614G P681R D950N |
| SRR27033648 | Sweden: Uppsala County | 2021-07-23 | AY.9.2 | 21I | good | 98.9 | 35 | T19R EFR156G A222V I410 L452R T478K D614G P681R D950N |
| MZ846201 | Sweden | 2021-08-10 | AY.9.2 | 21I | mediocre | - | - | - |
| MZ848129 | Sweden | 2021-08-10 | AY.9.2 | 21I | good | - | - | - |
| OP458823 | Sweden | 2021-07-12 | AY.122 | 21J | good | - | - | - |

Genome coverage, variants and spike changes are only available for samples processed from raw reads.

## Where the data came from

| Accession | ENA record | European Pathogens Portal |
|---|---|---|
| ERR7112279 | [link](https://www.ebi.ac.uk/ena/browser/view/ERR7112279) | - |
| SRR27033646 | [link](https://www.ebi.ac.uk/ena/browser/view/SRR27033646) | - |
| SRR27033647 | [link](https://www.ebi.ac.uk/ena/browser/view/SRR27033647) | - |
| SRR27033648 | [link](https://www.ebi.ac.uk/ena/browser/view/SRR27033648) | - |
| MZ846201 | [link](https://www.ebi.ac.uk/ena/browser/view/MZ846201) | [link](https://www.pathogensportal.org/sequences?db=embl-covid19&query=MZ846201) |
| MZ848129 | [link](https://www.ebi.ac.uk/ena/browser/view/MZ848129) | [link](https://www.pathogensportal.org/sequences?db=embl-covid19&query=MZ848129) |
| OP458823 | [link](https://www.ebi.ac.uk/ena/browser/view/OP458823) | [link](https://www.pathogensportal.org/sequences?db=embl-covid19&query=OP458823) |

## Output files in this folder

| File name starts with | What it is |
|---|---|
| `Multisample consensus FASTA` | Consensus genome of each processed sample (one file for Irish, one for Swedish) |
| `Final (SnpEff-) annotated variants` | Variants of one sample, with SnpEff annotation (VCF) |
| `SnpSift Extract Fields` | Variant table of one sample: position, change, allele frequency, depth, gene, protein change |
| `Nextclade ... (TSV report)` | Lineage, clade, mutations and quality of every sequence |
| `Nextclade ... (FASTA alignment)` | All sequences aligned to the reference |
| `SNP distance matrix` | Number of SNP differences between every pair of sequences |
| `Concatenate datasets` | All sequences compared, in one FASTA file |
| `Preprocessing and mapping reports` | MultiQC report: read quality and mapping (open in a browser) |
| `Samtools stats` | Mapping statistics of one sample |
| `Depth of coverage` | Read depth along the genome for one sample (bedGraph) |
| `summary.tsv` | The per-sample table above |
