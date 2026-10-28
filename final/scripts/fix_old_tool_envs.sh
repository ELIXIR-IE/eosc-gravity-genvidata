#!/usr/bin/env bash
# Part of step 3: rebuild the software of old tools that the IWC ONT workflow pins.
# - medaka 1.0.3 (consensus step) and medaka 1.3.2 (variant step): needs TensorFlow 2.2, which conda no longer has, so Galaxy fell back to a newer medaka
#   that no longer writes the file the tool expects (raw.vcf). Here medaka 1.3.4 (same 1.3 series, same
#   commands) is installed with pip on Python 3.8, with mappy and pyspoa taken from bioconda
#   and protobuf kept below 3.21 so TensorFlow 2.2 can load. The medaka 1.0.3 environment (Python 3.6)
#   cannot load TensorFlow either, so the consensus step uses the same medaka 1.3.4 (same commands and model).
# - multiqc 1.8: was built with Python 3.9 and new libraries it cannot use. Here it is rebuilt on
#   Python 3.8 with older numpy, networkx and matplotlib.
# Both are built inside the Galaxy container, as the galaxy user, in the folders Galaxy looks in.
# Run from the final/ folder (called by scripts/03_start_galaxy.sh):  bash scripts/fix_old_tool_envs.sh
set -euo pipefail

# skip if both already work (for example when step 3 is run again)
if docker exec -u galaxy genvidata-galaxy bash -c '
    E=/tool_deps/_conda/envs
    "$E/__medaka@1.3.2/bin/python" -c "import tensorflow, medaka.models" &&
    "$E/__medaka@1.0.3/bin/medaka" --version | grep -q 1.3.4 &&
    "$E/__multiqc@1.8/bin/multiqc" --version | grep -q 1.8' > /dev/null 2>&1; then
    echo "medaka and multiqc environments already fixed"
    exit 0
fi

docker exec -u galaxy genvidata-galaxy bash -c '
    set -e
    E=/tool_deps/_conda/envs
    M=/tool_deps/_conda/bin/mamba

    # medaka (the folder name must stay __medaka@1.3.2, the version the tool asks for)
    rm -rf "$E/__medaka@_uv_" "$E/__medaka@1.3.2"
    $M create -y -q -p "$E/__medaka@1.3.2" -c conda-forge -c bioconda \
        python=3.8 pip samtools=1.11 bcftools=1.11 htslib=1.11 minimap2 mappy pyspoa parasail-python
    "$E/__medaka@1.3.2/bin/pip" install -q "medaka==1.3.4" "protobuf<3.21"   # TensorFlow 2.2 needs the older protobuf
    rm -rf "$E/__medaka@1.0.3"
    ln -s "$E/__medaka@1.3.2" "$E/__medaka@1.0.3"

    # multiqc
    rm -rf "$E/__multiqc@1.8"
    $M create -y -q -p "$E/__multiqc@1.8" -c conda-forge -c bioconda \
        multiqc=1.8 python=3.8 "numpy<1.20" "networkx<2.5" "matplotlib<3.4"

    # remove downloaded package files to save disk
    $M clean -a -y -q
    rm -rf ~/.cache/pip

    "$E/__medaka@1.3.2/bin/medaka" --version
    "$E/__multiqc@1.8/bin/multiqc" --version
'
