# 🔗 Blockchain Registry - Hippocampus Memory System v1.0.0

All files are signed on the PHAM blockchain for contribution tracking and integrity verification.

## 📊 Blockchain Summary

**Total Files Signed**: 13  
**All Contributions**: A_HIGH (0.9998~1.0000)  
**Signing Date**: November 26, 2024  
**Author**: Jaejin Yoon  

---

## 🔐 Core Engine

### v4_event.py
- **Chain**: `pham_chain_v4_event.json`
- **Contribution**: A_HIGH (1.0000)
- **Description**: High-speed HH neuron engine with 28x speedup
- **SHA-256**: Stored in chain
- **IPFS CID**: Stored in chain

### v3_event.py
- **Chain**: `pham_chain_v3_event.json`
- **Contribution**: A_HIGH (1.0000)
- **Description**: Standard HH neuron with RK4 integration
- **SHA-256**: Stored in chain
- **IPFS CID**: Stored in chain

---

## 🧪 Experiments

### 1. hippo_ultimate.py
- **Chain**: `pham_chain_hippo_ultimate.json`
- **Contribution**: A_HIGH (0.9999)
- **Description**: Complete hippocampal circuit integration
- **Features**: DG → CA3 → CA1 → Subiculum

### 2. hippo_dream_final.py
- **Chain**: `pham_chain_hippo_dream_final.json`
- **Contribution**: A_HIGH (0.9999)
- **Description**: Wake-Sleep-Recall cycle with theta replay
- **Features**: Sleep consolidation, frequency-based replay

### 3. hippo_seq_v2_fast.py
- **Chain**: `pham_chain_hippo_seq_v2_fast.json`
- **Contribution**: A_HIGH (0.9999)
- **Description**: Multi-sequence memory with 9x speedup
- **Features**: 4 independent sequences, 0% interference

### 4. hippo_seq_v3_fast.py
- **Chain**: `pham_chain_hippo_seq_v3_fast.json`
- **Contribution**: A_HIGH (0.9999)
- **Description**: Long sequence memory with 28x speedup
- **Features**: 8-step chains (A→H)

### 5. hippo_alphabet.py
- **Chain**: `pham_chain_hippo_alphabet.json`
- **Contribution**: A_HIGH (0.9998)
- **Description**: 26-letter memory system
- **Features**: A-Z storage, 100% recall

### 6. hippo_words.py
- **Chain**: `pham_chain_hippo_words.json`
- **Contribution**: A_HIGH (0.9998)
- **Description**: Word sequence memory (CAT, DOG, etc)
- **Features**: Sequential word recall

### 7. hippo_branching.py
- **Chain**: `pham_chain_hippo_branching.json`
- **Contribution**: A_HIGH (0.9999)
- **Description**: Winner-Take-All decision making
- **Features**: Frequency-based selection (CAT vs CAR)

### 8. hippo_branching_v2.py
- **Chain**: `pham_chain_hippo_branching_v2.json`
- **Contribution**: A_HIGH (0.9999)
- **Description**: Parallel branching activation
- **Features**: Simultaneous associations (ANT, ARC, AIM)

### 9. hippo_ca1_temporal.py
- **Chain**: `pham_chain_hippo_ca1_temporal.json`
- **Contribution**: A_HIGH (0.9999)
- **Description**: CA1 temporal encoding with time cells
- **Features**: Sequence timing information

### 10. hippo_ca1_novelty.py
- **Chain**: `pham_chain_hippo_ca1_novelty.json`
- **Contribution**: A_HIGH (0.9998)
- **Description**: CA1 novelty detection system
- **Features**: Familiar vs. novel discrimination

### 11. hippo_subiculum_gate.py
- **Chain**: `pham_chain_hippo_subiculum_gate.json`
- **Contribution**: A_HIGH (0.9998)
- **Description**: Subiculum context-based gating
- **Features**: Context-relevant output filtering

---

## 🔍 Verification

To verify the blockchain integrity of any file:

```bash
# View chain for a specific file
python3 view_chain.py pham_chain_hippo_ultimate.json

# Or use pham_sign_v4.py to check
python3 pham_sign_v4.py experiments/hippo_ultimate.py --author "Jaejin Yoon" --desc "test"
# It will show if chain already exists
```

---

## 📈 Contribution Scores

All files achieved **A_HIGH** rating (0.9998~1.0000), indicating:
- ✅ High code quality
- ✅ Significant byte contribution
- ✅ Meaningful text content
- ✅ Proper AST structure
- ✅ Executable code

---

## 🔗 Blockchain Structure

Each chain file contains:

```json
{
  "index": 1,
  "timestamp": "2024-11-26T...",
  "data": {
    "title": "filename.py",
    "author": "Jaejin Yoon",
    "hash": "sha256_of_file",
    "cid": "ipfs_content_id",
    "description": "...",
    "signals": {
      "byte_signal": 1.0,
      "text_signal": 0.99,
      "ast_signal": 1.0,
      "exec_signal": 1.0
    },
    "contribution": "A_HIGH (0.9999)"
  },
  "previous_hash": "0",
  "hash": "block_hash"
}
```

---

## 🎯 Why Blockchain?

1. **Integrity**: Immutable record of file versions
2. **Attribution**: Clear authorship tracking
3. **Contribution**: Quantified code quality
4. **Transparency**: Public verification
5. **Trust**: Cryptographic proof

---

## 📝 Notes

- Chain files are NOT included in git (see `.gitignore`)
- To regenerate chains, run `./sign_all.sh`
- Each file has its own independent chain
- Chains can be extended with updates

---

## 🔮 Future

In future versions, these chains can be used for:
- Smart contract integration
- Contributor rewards
- Version tracking
- Decentralized storage (IPFS)

---

**🔗 "Code Integrity Through Blockchain"**

Last Updated: November 26, 2024

