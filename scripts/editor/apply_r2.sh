#!/bin/bash
# apply_r2.sh DIR READER: apply the anchor verdicts of round-2 reader READER (data/verification/DIR/round2/out_reader<N>.json)
set -e
cd "$(dirname "$0")/../.."
D=data/verification/$1/round2; N=$2
python3 -I -c "
import json;t=json.load(open('$D/tasks_reader$N.json'));json.dump(t['anchors'],open('$D/tasks_reader${N}_anchors.json','w'),ensure_ascii=False,indent=1)"
python3 -I scripts/apply_targeted.py $D/tasks_reader${N}_anchors.json $D/out_reader$N.json $D/patch_reader$N.json --apply 2>&1 | grep -v "^CORRECTED\|^WRONG" | tail -4
