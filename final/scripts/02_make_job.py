"""Step 2: write the Galaxy job file.

Reads and Swedish consensus sequences are given as web addresses, so Galaxy downloads them itself:
- reads from ENA, checked against ENA's MD5 checksum
- Swedish consensus sequences from the ENA Browser API
- the reference genome from the Zenodo record that the IWC workflow tests use
The primer files are small and kept in workflow/primers/ (sources in workflow/primers/SOURCES.md).

Run from the final/ folder:  python scripts/02_make_job.py
Reads inputs/samples.tsv, writes inputs/job.yml
"""
import csv
from pathlib import Path

import yaml

REFERENCE = "https://zenodo.org/record/4555735/files/NC_045512.2_reference.fasta?download=1"

config = yaml.safe_load(open("config.yml"))
samples = list(csv.DictReader(open("inputs/samples.tsv"), delimiter="\t"))


def reads_element(sample):
    return {"class": "File", "identifier": sample["accession"], "location": sample["file_url"],
            "filetype": "fastqsanger.gz", "hashes": [{"hash_function": "MD5", "hash_value": sample["md5"]}]}


def local_file(path, filetype):
    # planemo uploads local files; the path must be absolute or relative to the job file
    return {"class": "File", "path": str(Path(path).resolve()), "filetype": filetype}


irish_reads = [reads_element(s) for s in samples if s["role"] == "irish_sample_of_concern"]
swedish_reads = [reads_element(s) for s in samples if s["role"] == "swedish_raw_reads"]
swedish_consensus = [{"class": "File", "identifier": s["accession"], "location": s["file_url"], "filetype": "fasta"}
                     for s in samples if s["role"] == "swedish_consensus"]

job = {
    "reference": {"class": "File", "location": REFERENCE, "filetype": "fasta"},
    "irish_reads": {"class": "Collection", "collection_type": "list", "elements": irish_reads},
    "irish_primers": local_file(config["irish_primers"], "bed"),
    "irish_min_read_length": config["irish_min_read_length"],
    "irish_max_read_length": config["irish_max_read_length"],
    "swedish_reads": {"class": "Collection", "collection_type": "list", "elements": swedish_reads},
    "swedish_primers": local_file(config["swedish_primers"], "bed"),
    "swedish_min_read_length": config["swedish_min_read_length"],
    "swedish_max_read_length": config["swedish_max_read_length"],
    "swedish_consensus": {"class": "Collection", "collection_type": "list", "elements": swedish_consensus},
}

with open("inputs/job.yml", "w") as output_file:
    yaml.safe_dump(job, output_file, sort_keys=False)

print("Saved inputs/job.yml")
print("  Irish reads:      ", ", ".join(e["identifier"] for e in irish_reads), "| primers", config["irish_primers"])
print("  Swedish reads:    ", ", ".join(e["identifier"] for e in swedish_reads), "| primers", config["swedish_primers"])
print("  Swedish consensus:", ", ".join(e["identifier"] for e in swedish_consensus))
