#!/bin/bash
# Blockchain signing script for all files

AUTHOR="Jaejin Yoon"

# Core files
python3 pham_sign_v4.py core/v3_event.py --author "$AUTHOR" --desc "Standard HH neuron with RK4 integration"

# Experiments
python3 pham_sign_v4.py experiments/hippo_ultimate.py --author "$AUTHOR" --desc "Complete hippocampal circuit integration"
python3 pham_sign_v4.py experiments/hippo_dream_final.py --author "$AUTHOR" --desc "Wake-Sleep-Recall cycle with theta replay"
python3 pham_sign_v4.py experiments/hippo_seq_v2_fast.py --author "$AUTHOR" --desc "Multi-sequence memory with 9x speedup"
python3 pham_sign_v4.py experiments/hippo_seq_v3_fast.py --author "$AUTHOR" --desc "Long sequence memory with 28x speedup"
python3 pham_sign_v4.py experiments/hippo_alphabet.py --author "$AUTHOR" --desc "26-letter memory system"
python3 pham_sign_v4.py experiments/hippo_words.py --author "$AUTHOR" --desc "Word sequence memory (CAT, DOG, etc)"
python3 pham_sign_v4.py experiments/hippo_branching.py --author "$AUTHOR" --desc "Winner-Take-All decision making"
python3 pham_sign_v4.py experiments/hippo_branching_v2.py --author "$AUTHOR" --desc "Parallel branching activation"
python3 pham_sign_v4.py experiments/hippo_ca1_temporal.py --author "$AUTHOR" --desc "CA1 temporal encoding with time cells"
python3 pham_sign_v4.py experiments/hippo_ca1_novelty.py --author "$AUTHOR" --desc "CA1 novelty detection system"
python3 pham_sign_v4.py experiments/hippo_subiculum_gate.py --author "$AUTHOR" --desc "Subiculum context-based gating"

echo ""
echo "==================================="
echo "✅ All files signed on blockchain!"
echo "==================================="
