"""Step 1: find the data.

- The Irish sample of concern: looks up the run in ENA.
- Swedish data, found the way a researcher would:
    Swedish Pathogens Portal (pathogens.se) -> European Pathogens Portal (EMBL-EBI) -> ENA accessions.
  The Swedish portal has no API. Its sequence sections show data from the European Pathogens Portal,
  and that portal searches the EBI Search index "embl-covid19". This script searches the same index,
  and searches ENA for Swedish raw reads.

Only country, collection date and the file links are kept. Personal fields in ENA sample records
(for example host sex, age and exact coordinates) are not copied: this is the "remove personal metadata" step.

Run from the final/ folder:  python scripts/01_find_data.py
Writes inputs/samples.tsv
"""
import csv
from pathlib import Path

import requests
import yaml

ENA_SEARCH = "https://www.ebi.ac.uk/ena/portal/api/search"
ENA_FILEREPORT = "https://www.ebi.ac.uk/ena/portal/api/filereport"
EBI_SEARCH = "https://www.ebi.ac.uk/ebisearch/ws/rest/embl-covid19"
SARS_COV_2 = "2697049"

config = yaml.safe_load(open("config.yml"))
rows = []


def ena_link(accession):
    return "https://www.ebi.ac.uk/ena/browser/view/" + accession


def portal_link(accession):
    return "https://www.pathogensportal.org/sequences?db=embl-covid19&query=" + accession


# ---------- 1. the Irish run ----------
fields = "run_accession,collection_date,country,instrument_platform,library_strategy,fastq_ftp,fastq_md5"
response = requests.get(ENA_FILEREPORT, params={"accession": config["irish_run"], "result": "read_run",
                                                "fields": fields, "format": "json"}, timeout=60)
response.raise_for_status()
irish = response.json()[0]
rows.append({"accession": irish["run_accession"], "role": "irish_sample_of_concern", "data_type": "raw_reads",
             "country": irish["country"], "collection_date": irish["collection_date"],
             "file_url": "https://" + irish["fastq_ftp"], "md5": irish["fastq_md5"],
             "ena_link": ena_link(irish["run_accession"]), "portal_link": ""})
print("Irish sample:", irish["run_accession"], irish["country"], irish["collection_date"],
      irish["instrument_platform"], irish["library_strategy"])

# ---------- 2. Swedish discovery ----------
print()
print("Finding Swedish data")
print("  Entry point: Swedish Pathogens Portal, https://www.pathogens.se/available-data/")
print("  Its sequence sections link to the European Pathogens Portal, https://www.pathogensportal.org")
print("  which searches the EBI Search index 'embl-covid19'. The data itself is held in ENA.")

# 2a. Swedish raw reads: same platform and method as the Irish run, so the same workflow can process them
query = (f'tax_tree({SARS_COV_2}) AND country="Sweden" AND instrument_platform="OXFORD_NANOPORE" '
         f'AND library_strategy="AMPLICON" '
         f'AND collection_date>={config["swedish_runs_from"]} AND collection_date<={config["swedish_runs_to"]}')
response = requests.get(ENA_SEARCH, params={"result": "read_run", "query": query,
                                            "fields": "run_accession,study_accession,collection_date,country,fastq_ftp,fastq_md5",
                                            "format": "json", "limit": 0}, timeout=60)
response.raise_for_status()
swedish_runs = [run for run in response.json() if run["fastq_ftp"]]   # keep runs that have a FASTQ file
swedish_runs.sort(key=lambda run: run["run_accession"])
print(f"  Swedish Nanopore amplicon runs in ENA, {config['swedish_runs_from']} to {config['swedish_runs_to']}:",
      len(swedish_runs), "found, using", min(len(swedish_runs), config["swedish_runs_max"]))
for run in swedish_runs[:config["swedish_runs_max"]]:
    rows.append({"accession": run["run_accession"], "role": "swedish_raw_reads", "data_type": "raw_reads",
                 "country": run["country"], "collection_date": run["collection_date"][:10],
                 "file_url": "https://" + run["fastq_ftp"], "md5": run["fastq_md5"],
                 "ena_link": ena_link(run["run_accession"]), "portal_link": ""})
    print("    ", run["run_accession"], run["study_accession"], run["collection_date"][:10])

# 2b. Swedish consensus sequences, from the index behind the European Pathogens Portal
date_from = config["swedish_consensus_from"].replace("-", "")
date_to = config["swedish_consensus_to"].replace("-", "")
response = requests.get(EBI_SEARCH, params={"query": f"country:Sweden AND collection_date:[{date_from} TO {date_to}]",
                                            "fields": "country,collection_date", "format": "json",
                                            "size": config["swedish_consensus_max"]}, timeout=60)
response.raise_for_status()
result = response.json()
print(f"  Swedish consensus sequences in embl-covid19, {config['swedish_consensus_from']} to "
      f"{config['swedish_consensus_to']}:", result["hitCount"], "found, using", len(result["entries"]))
for entry in result["entries"]:
    accession = entry["id"]
    date = entry["fields"]["collection_date"][0]
    rows.append({"accession": accession, "role": "swedish_consensus", "data_type": "consensus_sequence",
                 "country": "Sweden", "collection_date": f"{date[:4]}-{date[4:6]}-{date[6:]}",
                 "file_url": "https://www.ebi.ac.uk/ena/browser/api/fasta/" + accession, "md5": "",
                 "ena_link": ena_link(accession), "portal_link": portal_link(accession)})
    print("    ", accession, rows[-1]["collection_date"], portal_link(accession))

# ---------- 3. save ----------
Path("inputs").mkdir(exist_ok=True)
with open("inputs/samples.tsv", "w", newline="") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=list(rows[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)
print()
print("Saved", len(rows), "rows to inputs/samples.tsv")
