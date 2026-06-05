#!/usr/bin/env bash
# Programmatic grading signals for each run: structurizr validation + syntax checks.
set -u
ITER="$(cd "$(dirname "$0")" && pwd)"

for run in eval-*/with_skill eval-*/without_skill; do
    out="$ITER/$run/outputs"
    dsl="$out/workspace.dsl"
    echo "=== $run"
    if [[ ! -f "$dsl" ]]; then
        echo "dsl_exists=false"
        continue
    fi
    echo "dsl_exists=true"
    v=$(docker run --rm -v "$out":/usr/local/structurizr structurizr/structurizr \
        validate -workspace workspace.dsl 2>&1)
    rc=$?
    echo "validate_rc=$rc"
    [[ -n "$v" ]] && echo "validate_out=$(echo "$v" | tail -5 | tr '\n' ' ')"
    # legacy / removed keywords
    grep -nEi '^\s*enterprise\s*\{|!extend|!ref\b|branding\s*\{|theme\s+default|dashed\s+(true|false)|^\s*themes\s' "$dsl" \
        | sed 's/^/legacy: /' || echo "legacy: none"
    # deprecated image suggested anywhere in response or dsl
    grep -l 'structurizr/lite' "$out/final_response.md" "$dsl" 2>/dev/null \
        | sed 's/^/lite_mention: /' || echo "lite_mention: none"
    # structural signals
    for kw in systemContext systemLandscape 'container ' 'dynamic ' 'deployment ' '!adrs' 'instances 2' 'infrastructureNode' 'scope landscape' 'scope softwaresystem' 'shape cylinder' 'shape pipe' 'shape Cylinder' 'shape Pipe'; do
        c=$(grep -ciE "$(echo "$kw" | sed 's/[!]/\\!/')" "$dsl")
        echo "count[$kw]=$c"
    done
done
