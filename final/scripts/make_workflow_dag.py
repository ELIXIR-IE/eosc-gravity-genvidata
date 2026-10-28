"""Draw the workflow as a graph (DAG), from workflow/genvidata.ga itself.

Writes:
- workflow/genvidata_dag.png and .svg   picture: inputs -> steps -> outputs, with the main tools inside each subworkflow
- workflow/genvidata_dag.md             the same graph in Mermaid, which VS Code's Markdown preview and GitHub draw

Run from the final/ folder:  python scripts/make_workflow_dag.py   (after scripts/make_native_workflow.py)
"""
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "none"

GREY, TEAL, PINK, INK, LINE = "#6B7280", "#00868B", "#D6457A", "#1F2933", "#9AA5AB"
GREEN, BLUE = "#145424", "#006AA7"

# helper tools inside the IWC workflows that only reshape files; left out of the picture to keep it readable
HELPERS = {"Add_a_column1", "tp_replace_in_column", "tp_find_and_replace", "datamash_ops", "param_value_from_file",
           "__FILTER_FAILED_DATASETS__", "__FLATTEN__", "compose_text_param", "Filter1", "gops_concat_1",
           "gops_merge_1", "gops_subtract_1", "collapse_dataset", "samtools_stats", "qualimap_bamqc"}
# readable names for the tools that are shown
NAMES = {"fastp": "fastp (read QC, length filter)", "minimap2": "minimap2 (map to reference)",
         "samtools_view": "samtools view (filter)", "bamleftalign": "BamLeftAlign", "ivar_trim": "ivar trim (primers)",
         "medaka_consensus": "medaka consensus", "medaka_variant": "medaka variant", "bedtools_intersectbed":
         "bedtools intersect", "multiqc": "MultiQC (QC report)", "bcftools_annotate": "bcftools annotate",
         "snpeff_sars_cov_2": "SnpEff (annotate variants)", "lofreq_filter": "lofreq filter (strand bias)",
         "bedtools_genomecoveragebed": "bedtools genomecov (depth)", "snpSift_filter": "SnpSift filter",
         "snpSift_extractFields": "SnpSift extract fields", "bcftools_consensus": "bcftools consensus (masked)",
         "tp_cat": "Concatenate", "nextclade": "Nextclade", "snp_dists": "snp-dists"}
LABELS = {"irish_variation": "Variation (IWC ONT ARTIC)", "swedish_variation": "Variation (IWC ONT ARTIC)",
          "irish_consensus": "Consensus (IWC)", "swedish_consensus_from_reads": "Consensus (IWC)",
          "irish_variant_table": "Variant table\nSnpSift extract fields",
          "swedish_variant_table": "Variant table\nSnpSift extract fields",
          "collapse_swedish_ena": "Collapse into one FASTA", "join_sequences": "Join all sequences\nConcatenate",
          "lineage": "Lineage and mutations\nNextclade", "distances": "SNP distances\nsnp-dists"}

workflow = json.load(open("workflow/genvidata.ga"))
steps = {int(k): v for k, v in workflow["steps"].items()}


def short_tool(tool_id):
    return tool_id.split("/")[-2] if "/" in tool_id else tool_id


def main_tools(subworkflow):
    """The tools inside a subworkflow, in step order, without the helpers and without repeats."""
    names = []
    for _, step in sorted(subworkflow["steps"].items(), key=lambda item: int(item[0])):
        if step["type"] == "tool":
            name = short_tool(step["tool_id"])
            if name not in HELPERS and NAMES.get(name, name) not in names:
                names.append(NAMES.get(name, name))
    return names


# ---------- the graph: nodes, edges and a column (layer) for each node ----------
parents = {i: sorted({c["id"] for conns in s.get("input_connections", {}).values()
                      for c in (conns if isinstance(conns, list) else [conns])}) for i, s in steps.items()}
layer = {}
for i in sorted(steps):
    layer[i] = 0 if not parents[i] else 1 + max(layer[p] for p in parents[i])
children = {i: [j for j in steps if i in parents[j]] for i in steps}
for i in sorted(steps, reverse=True):
    if children[i] and (parents[i] or len(children[i]) == 1):   # inputs used by one step move next to it
        layer[i] = min(layer[c] for c in children[i]) - 1

# draw the four read-length numbers as one node per country, to keep the input column short
merged = {}
for i, s in steps.items():
    if s["type"] == "parameter_input":
        country = s["label"].split("_")[0]
        merged[i] = next(j for j, t in steps.items() if t.get("label") == f"{country}_reads")


def node_text(i):
    s = steps[i]
    if s["type"] in ("data_input", "data_collection_input"):
        extra = "\n+ min/max read length" if s["label"].endswith("_reads") else ""
        if s["label"] == "reference":
            extra = "\nNC_045512.2, used by every\nmapping and consensus step"
        return s["label"].replace("_", " ") + extra
    return LABELS.get(s["label"], s["label"])


def node_colour(i):
    s = steps[i]
    if s["type"] in ("data_input", "data_collection_input"):
        return GREY
    return TEAL if s["type"] == "subworkflow" else PINK


def country_colour(i):
    label = steps[i].get("label", "")
    return GREEN if label.startswith("irish") else BLUE if label.startswith("swedish") else None


# ---------- picture ----------
shown = [i for i in sorted(steps) if i not in merged]
columns = {}
for i in sorted(shown, key=lambda i: (steps[i]["type"].endswith("input"), i)):   # steps above inputs
    columns.setdefault(layer[i], []).append(i)

BOX_W, COL_GAP, LINE_H, TOOL_H = 34.0, 10.0, 2.6, 2.1
heights = {}
for i in shown:
    heights[i] = 3.4 + (node_text(i).count("\n") + 1) * LINE_H
    if steps[i]["type"] == "subworkflow":
        heights[i] += 0.6 + len(main_tools(steps[i]["subworkflow"])) * TOOL_H

total_h = max(sum(heights[i] + 3.0 for i in col) for col in columns.values()) + 6.0
width = len(columns) * (BOX_W + COL_GAP) + 4.0
fig = plt.figure(figsize=(width / 6.5, total_h / 6.5), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, width)
ax.set_ylim(0, total_h)
ax.axis("off")

box = {}
for c, col in sorted(columns.items()):
    x = 2.0 + c * (BOX_W + COL_GAP)
    column_h = sum(heights[i] + 3.0 for i in col)
    y = total_h - (total_h - column_h) / 2 - 1.5
    for i in col:
        h = heights[i]
        y -= h
        edge = country_colour(i) or node_colour(i)
        ax.add_patch(FancyBboxPatch((x, y), BOX_W, h, boxstyle="round,pad=0,rounding_size=1.2",
                                    facecolor="white", edgecolor=edge, linewidth=2.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y + h - 1.3), BOX_W, 1.3, boxstyle="round,pad=0,rounding_size=0.6",
                                    facecolor=node_colour(i), edgecolor="none", zorder=3))
        title = node_text(i)
        ax.text(x + 1.5, y + h - 2.6, title, ha="left", va="top", fontsize=11, fontweight="bold", color=INK,
                zorder=4, linespacing=1.35)
        if steps[i]["type"] == "subworkflow":
            tools = main_tools(steps[i]["subworkflow"])
            top = y + h - 2.6 - (title.count("\n") + 1) * LINE_H - 0.6
            for k, tool in enumerate(tools):
                ax.text(x + 2.2, top - k * TOOL_H, "· " + tool, ha="left", va="top", fontsize=9.4, color=INK,
                        zorder=4)
        box[i] = (x, y, h)
        y -= 3.0

for i in shown:
    for p in parents[i]:
        p = merged.get(p, p)
        if p not in box or steps[p].get("label") == "reference":
            continue
        px, py, ph = box[p]
        cx, cy, ch = box[i]
        arrow = FancyArrowPatch((px + BOX_W, py + ph / 2), (cx, cy + ch / 2), arrowstyle="-|>", mutation_scale=10,
                                color=LINE, linewidth=1.1, connectionstyle="arc3,rad=0.0", zorder=1)
        ax.add_patch(arrow)

ax.text(2.0, 1.6, "Grey: inputs   Teal: IWC subworkflows (main tools listed)   Pink: added tools   "
        "Green outline: Irish branch   Blue outline: Swedish branch", fontsize=9.5, color=GREY, ha="left")

for ext in ("png", "svg"):
    fig.savefig(f"workflow/genvidata_dag.{ext}", facecolor="white", dpi=200)
print("Saved workflow/genvidata_dag.png and .svg")

# ---------- Mermaid version ----------
mermaid = ["```mermaid", "graph LR"]
for i in shown:
    text = node_text(i).replace("\n", "<br/>")
    if steps[i]["type"] == "subworkflow":
        mermaid.append(f'    subgraph s{i}["{steps[i]["label"]}: {text}"]')
        tools = main_tools(steps[i]["subworkflow"])
        for k, tool in enumerate(tools):
            mermaid.append(f'        s{i}_{k}["{tool}"]')
            if k:
                mermaid.append(f"        s{i}_{k - 1} --> s{i}_{k}")
        mermaid.append("    end")
    elif steps[i]["type"] in ("data_input", "data_collection_input"):
        mermaid.append(f'    n{i}[/"{text}"/]')
    else:
        mermaid.append(f'    n{i}["{text}"]')


def mermaid_id(i):
    return f"s{i}" if steps[i]["type"] == "subworkflow" else f"n{i}"


for i in shown:
    for p in sorted({merged.get(p, p) for p in parents[i]}):
        mermaid.append(f"    {mermaid_id(p)} --> {mermaid_id(i)}")
mermaid.append("```")

with open("workflow/genvidata_dag.md", "w") as handle:
    handle.write("# GenViData workflow graph\n\nMade by `scripts/make_workflow_dag.py` from `workflow/genvidata.ga`. "
                 "The picture version is `genvidata_dag.png`.\n\n" + "\n".join(mermaid) + "\n")
print("Saved workflow/genvidata_dag.md")
