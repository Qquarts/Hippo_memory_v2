#!/bin/bash
################################################################################
# PHAM Blockchain Signing Script - Enhanced Version
################################################################################
#
# 모든 핵심 파일을 블록체인에 서명합니다.
# 
# Usage: ./sign_all.sh
#
################################################################################

set -e  # 에러 시 종료

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# 카운터
TOTAL=0
SUCCESS=0
FAILED=0

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo -e "${BOLD}${CYAN}🔗 PHAM BLOCKCHAIN SIGNING PROCESS${NC}"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# Core 엔진 파일
echo -e "${BOLD}${BLUE}[1/3] Core Engine Files${NC}"
echo "────────────────────────────────────────────────────────────────────────"

FILES_CORE=(
    "experiments/v3_event.py:GNJz:Standard HH neuron with RK4 integration"
    "experiments/v4_event.py:GNJz:High-speed HH neuron with 28x speedup"
)

for item in "${FILES_CORE[@]}"; do
    IFS=':' read -r file author desc <<< "$item"
    TOTAL=$((TOTAL + 1))
    
    if [ -f "$file" ]; then
        echo -e "${CYAN}[${TOTAL}]${NC} Signing: ${BOLD}$(basename $file)${NC}"
        echo "    Author: $author"
        echo "    Desc:   $desc"
        
        if python3 pham_sign_v4.py "$file" --author "$author" --desc "$desc" > /dev/null 2>&1; then
            SUCCESS=$((SUCCESS + 1))
            echo -e "    ${GREEN}✓ Success${NC}"
        else
            FAILED=$((FAILED + 1))
            echo -e "    ${RED}✗ Failed${NC}"
        fi
    else
        FAILED=$((FAILED + 1))
        echo -e "${RED}✗ File not found: $file${NC}"
    fi
    echo ""
done

# Experiment 파일
echo -e "${BOLD}${BLUE}[2/3] Experiment Files${NC}"
echo "────────────────────────────────────────────────────────────────────────"

FILES_EXP=(
    "experiments/hippo_ultimate.py:GNJz:Complete hippocampal circuit integration"
    "experiments/hippo_dream_final.py:GNJz:Sleep consolidation with theta replay"
    "experiments/hippo_seq_v2_fast.py:GNJz:Multi-sequence memory with 9x speedup"
    "experiments/hippo_seq_v3_fast.py:GNJz:Long sequence A-H with 28x speedup"
    "experiments/hippo_alphabet.py:GNJz:26-letter alphabet memory storage"
    "experiments/hippo_words.py:GNJz:Word sequence memory (CAT DOG BAT RAT)"
    "experiments/hippo_branching.py:GNJz:Winner-Take-All branching (CAR vs CAT)"
    "experiments/hippo_branching_v2.py:GNJz:Parallel branching (ANT ARC AIM)"
    "experiments/hippo_ca1_temporal.py:GNJz:CA1 temporal encoding experiment"
    "experiments/hippo_ca1_novelty.py:GNJz:CA1 novelty detection experiment"
    "experiments/hippo_subiculum_gate.py:GNJz:Subiculum context gating experiment"
)

for item in "${FILES_EXP[@]}"; do
    IFS=':' read -r file author desc <<< "$item"
    TOTAL=$((TOTAL + 1))
    
    if [ -f "$file" ]; then
        echo -e "${CYAN}[${TOTAL}]${NC} Signing: ${BOLD}$(basename $file)${NC}"
        echo "    Author: $author"
        echo "    Desc:   $desc"
        
        if python3 pham_sign_v4.py "$file" --author "$author" --desc "$desc" > /dev/null 2>&1; then
            SUCCESS=$((SUCCESS + 1))
            echo -e "    ${GREEN}✓ Success${NC}"
        else
            FAILED=$((FAILED + 1))
            echo -e "    ${RED}✗ Failed${NC}"
        fi
    else
        FAILED=$((FAILED + 1))
        echo -e "${RED}✗ File not found: $file${NC}"
    fi
    echo ""
done

# 최종 결과
echo "════════════════════════════════════════════════════════════════════════"
echo -e "${BOLD}${CYAN}📊 SIGNING SUMMARY${NC}"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "  ${GREEN}✓ Success:${NC} $SUCCESS / $TOTAL"
echo -e "  ${RED}✗ Failed:${NC}  $FAILED / $TOTAL"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}${BOLD}🎉 All files signed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Some files failed to sign. Check the output above.${NC}"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo -e "${BOLD}${BLUE}[3/3] Verification${NC}"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "Running chain viewer to verify..."
echo ""

python3 view_chains.py

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}${BOLD}✅ BLOCKCHAIN SIGNING COMPLETE!${NC}"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
