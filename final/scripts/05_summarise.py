"""Step 5: summarise the results in plain language.

Reads the outputs downloaded by step 4 and inputs/samples.tsv, and writes, in the same results folder:
- summary.md   what was found, per sample, and how close the Irish sample is to each Swedish sequence
- summary.tsv  the same per-sample numbers as a table

Run from the final/ folder:  python scripts/05_summarise.py              (the newest folder in results/)
                         or  python scripts/05_summarise.py results/<run folder>
"""
import csv
import json
import sys
from pathlib import Path

GENOME_LENGTH = 29903        # NC_045512.2
MIN_DEPTH = 5                # the depth below which the IWC consensus workflow masks a position with N
CONSENSUS_AF = 0.75          # the allele frequency from which the IWC consensus workflow puts a variant in the consensus

folder = Path(sys.argv[1]) if len(sys.argv) > 1 else sorted(Path("results").iterdir())[-1]
outputs = json.load(open(folder / "outputs.json"))["outputs"]
samples = {row["accession"]: row for row in csv.DictReader(open("inputs/samples.tsv"), delimiter="\t")}


def file_of(dataset):
    """The downloaded file of one Galaxy dataset (files are named '<name>__<uuid>.<ext>')."""
    return next(folder.glob(f"*__{dataset['uuid']}.*"))


def files_per_sample(label):
    """For a collection output: {accession: file}. Missing outputs give an empty dict."""
    if label not in outputs:
        return {}
    return {element["element_identifier"]: file_of(element["object"]) for element in outputs[label]["elements"]}


def single_file(label):
    return folder / outputs[label]["path"] if "path" in outputs[label] else file_of(outputs[label])


def accession_of(sequence_name):
    """'ENA|MZ846201|MZ846201.1 Severe acute ...' -> 'MZ846201'; 'ERR7112279' -> 'ERR7112279'."""
    first_word = sequence_name.split()[0]
    return first_word.split("|")[1] if first_word.startswith("ENA|") else first_word


# ---------- read the outputs ----------
lineage = {accession_of(row["seqName"]): row
           for row in csv.DictReader(open(single_file("lineage_report")), delimiter="\t")}

with open(single_file("snp_distances")) as handle:
    rows = [line.rstrip("\n").split("\t") for line in handle]
names = [accession_of(name) for name in rows[0][1:]]
distances = {accession_of(row[0]): dict(zip(names, map(int, row[1:]))) for row in rows[1:]}

mapping_stats, coverage, variant_tables = {}, {}, {}
for country in ("irish", "swedish"):
    mapping_stats.update(files_per_sample(f"{country}_mapping_stats"))
    coverage.update(files_per_sample(f"{country}_coverage_depth"))
    variant_tables.update(files_per_sample(f"{country}_variant_table"))


def reads_mapped(path):
    for line in open(path):
        if line.startswith("SN\treads mapped:"):
            return int(line.split("\t")[2])


def depth_summary(path):
    """Share of the genome covered by at least MIN_DEPTH reads, and the mean depth (from a bedGraph file)."""
    covered = total = 0
    for line in open(path):
        chrom, start, end, depth = line.split("\t")
        length = int(end) - int(start)
        total += length * int(depth)
        if int(depth) >= MIN_DEPTH:
            covered += length
    return 100 * covered / GENOME_LENGTH, total / GENOME_LENGTH


def variants(path):
    """Variants at or above the consensus allele frequency, and the spike (S gene) protein changes among them."""
    rows = [row for row in csv.DictReader(open(path), delimiter="\t") if float(row["AF"]) >= CONSENSUS_AF]
    spike = [row["EFF[0].AA"] for row in rows if row["EFF[0].GENE"] == "S" and row["EFF[0].AA"] not in ("", ".")]
    return len(rows), spike


# ---------- one row per sequence ----------
table = []
for accession, sample in samples.items():
    nextclade = lineage.get(accession, {})
    row = {"accession": accession, "role": sample["role"], "country": sample["country"],
           "collection_date": sample["collection_date"],
           "pango_lineage": nextclade.get("Nextclade_pango", ""), "clade": nextclade.get("clade", ""),
           "nextclade_qc": nextclade.get("qc.overallStatus", ""),
           "reads_mapped": "", "genome_covered_pct": "", "mean_depth": "", "variants": "", "spike_changes": ""}
    if accession in mapping_stats:
        row["reads_mapped"] = reads_mapped(mapping_stats[accession])
        covered, mean = depth_summary(coverage[accession])
        row["genome_covered_pct"] = f"{covered:.1f}"
        row["mean_depth"] = f"{mean:.0f}"
        count, spike = variants(variant_tables[accession])
        row["variants"] = count
        row["spike_changes"] = " ".join(spike)
    table.append(row)

with open(folder / "summary.tsv", "w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(table[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(table)

# ---------- plain-language summary ----------
irish = next(row for row in table if row["role"] == "irish_sample_of_concern")
others = sorted((distance, accession) for accession, distance in distances[irish["accession"]].items()
                if accession != irish["accession"])
closest_distance, closest = others[0]
closest_row = next(row for row in table if row["accession"] == closest)

lines = [
    f"# GenViData results: {irish['accession']}",
    "",
    f"Run folder: `{folder}`. Galaxy run id: `{json.load(open(folder / 'outputs.json'))['invocation_id']}`.",
    "",
    "## The Irish sample of concern",
    "",
    f"- **{irish['accession']}**, collected {irish['collection_date']} in {irish['country']}.",
    f"- Lineage **{irish['pango_lineage']}** (Nextstrain clade {irish['clade']}). Nextclade quality: {irish['nextclade_qc']}.",
    f"- {irish['reads_mapped']} reads mapped; {irish['genome_covered_pct']}% of the genome covered by at least "
    f"{MIN_DEPTH} reads (mean depth {irish['mean_depth']}).",
    f"- {irish['variants']} variants with allele frequency of at least {CONSENSUS_AF}. "
    f"Spike protein changes: {irish['spike_changes'] or 'none'}.",
    "",
    "## Closest Swedish sequence",
    "",
    f"**{closest}** ({closest_row['role'].replace('_', ' ')}, collected {closest_row['collection_date']}, "
    f"lineage {closest_row['pango_lineage']}) differs from the Irish sample at **{closest_distance}** positions.",
    "",
    "SNP differences between the Irish sample and every Swedish sequence (fewer differences = more closely related):",
    "",
    "| Swedish sequence | Data used | Collected | Lineage | SNP differences |",
    "|---|---|---|---|---|",
]
for distance, accession in others:
    row = next(r for r in table if r["accession"] == accession)
    data_used = "raw reads, processed here" if row["role"] == "swedish_raw_reads" else "consensus from ENA"
    lines.append(f"| {accession} | {data_used} | {row['collection_date']} | {row['pango_lineage']} | {distance} |")

lines += [
    "",
    "## All sequences",
    "",
    "| Accession | Country | Collected | Lineage | Clade | Nextclade QC | Genome covered (%) | Variants | Spike changes |",
    "|---|---|---|---|---|---|---|---|---|",
]
for row in table:
    lines.append(f"| {row['accession']} | {row['country']} | {row['collection_date']} | {row['pango_lineage']} | "
                 f"{row['clade']} | {row['nextclade_qc']} | {row['genome_covered_pct'] or '-'} | "
                 f"{row['variants'] if row['variants'] != '' else '-'} | {row['spike_changes'] or '-'} |")

lines += [
    "",
    "Genome coverage, variants and spike changes are only available for samples processed from raw reads.",
    "",
    "## Where the data came from",
    "",
    "| Accession | ENA record | European Pathogens Portal |",
    "|---|---|---|",
]
for accession, sample in samples.items():
    portal = f"[link]({sample['portal_link']})" if sample["portal_link"] else "-"
    lines.append(f"| {accession} | [link]({sample['ena_link']}) | {portal} |")

lines += [
    "",
    "## Output files in this folder",
    "",
    "| File name starts with | What it is |",
    "|---|---|",
    "| `Multisample consensus FASTA` | Consensus genome of each processed sample (one file for Irish, one for Swedish) |",
    "| `Final (SnpEff-) annotated variants` | Variants of one sample, with SnpEff annotation (VCF) |",
    "| `SnpSift Extract Fields` | Variant table of one sample: position, change, allele frequency, depth, gene, protein change |",
    "| `Nextclade ... (TSV report)` | Lineage, clade, mutations and quality of every sequence |",
    "| `Nextclade ... (FASTA alignment)` | All sequences aligned to the reference |",
    "| `SNP distance matrix` | Number of SNP differences between every pair of sequences |",
    "| `Concatenate datasets` | All sequences compared, in one FASTA file |",
    "| `Preprocessing and mapping reports` | MultiQC report: read quality and mapping (open in a browser) |",
    "| `Samtools stats` | Mapping statistics of one sample |",
    "| `Depth of coverage` | Read depth along the genome for one sample (bedGraph) |",
    "| `summary.tsv` | The per-sample table above |",
]

(folder / "summary.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines[:22]))
print()
print("Saved", folder / "summary.md", "and", folder / "summary.tsv")
