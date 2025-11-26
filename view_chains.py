#!/usr/bin/env python3
"""
================================================================================
PHAM Blockchain Chain Viewer - Enhanced Version
================================================================================

깔끔하고 직관적인 블록체인 체인 확인 도구

Usage:
    python3 view_chains.py                    # 모든 체인 요약
    python3 view_chains.py <chain_file.json>  # 특정 체인 상세 보기
    python3 view_chains.py --all              # 모든 체인 상세 보기

================================================================================
"""

import json
import sys
import os
import glob
from datetime import datetime
import hashlib

# ============================================================================
# 색상 출력 (터미널 지원)
# ============================================================================
class Colors:
    """ANSI 색상 코드"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def disable():
        """색상 비활성화 (파이프 출력 시)"""
        Colors.HEADER = ''
        Colors.OKBLUE = ''
        Colors.OKCYAN = ''
        Colors.OKGREEN = ''
        Colors.WARNING = ''
        Colors.FAIL = ''
        Colors.ENDC = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''

# ============================================================================
# 유틸리티 함수
# ============================================================================
def format_timestamp(timestamp_str):
    """타임스탬프를 읽기 쉽게 변환"""
    try:
        # ISO 형식 문자열인 경우
        if isinstance(timestamp_str, str):
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        # Unix 타임스탬프인 경우
        elif isinstance(timestamp_str, (int, float)):
            dt = datetime.fromtimestamp(timestamp_str)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(timestamp_str)
    except:
        return str(timestamp_str)

def format_hash(hash_str, length=16):
    """해시를 짧게 표시"""
    if len(hash_str) > length:
        return f"{hash_str[:length]}..."
    return hash_str

def format_cid(cid_str, length=20):
    """CID를 짧게 표시"""
    if len(cid_str) > length:
        return f"{cid_str[:length]}..."
    return cid_str

def get_grade_color(contribution):
    """기여도에 따른 색상"""
    if 'A_HIGH' in contribution:
        return Colors.OKGREEN
    elif 'A_MID' in contribution:
        return Colors.OKCYAN
    elif 'B' in contribution:
        return Colors.OKBLUE
    else:
        return Colors.WARNING

def verify_block_hash(block):
    """블록 해시 검증"""
    # 블록 데이터를 문자열로 변환
    block_string = f"{block['index']}{block['previous_hash']}{block['timestamp']}{json.dumps(block['data'], sort_keys=True)}"
    computed_hash = hashlib.sha256(block_string.encode()).hexdigest()
    return computed_hash == block['hash']

def verify_chain(chain):
    """체인 무결성 검증"""
    if not chain:
        return False, "Empty chain"
    
    # Genesis block (index 0은 previous_hash가 없을 수 있음)
    if len(chain) > 0 and chain[0].get('index') == 0:
        # Genesis는 체크 스킵
        pass
    
    # 각 블록 검증
    for i in range(len(chain)):
        block = chain[i]
        
        # 이전 블록 해시 연결 검증
        if i > 0:
            if 'previous_hash' in block and 'hash' in chain[i-1]:
                if block['previous_hash'] != chain[i-1]['hash']:
                    return False, f"Block {i} chain link broken"
    
    return True, "Chain integrity verified"

# ============================================================================
# 체인 요약 보기
# ============================================================================
def show_chain_summary(chain_file):
    """개별 체인 요약 정보"""
    try:
        with open(chain_file, 'r', encoding='utf-8') as f:
            chain = json.load(f)
        
        if not chain:
            return None
        
        # 파일명에서 이름 추출
        filename = os.path.basename(chain_file)
        name = filename.replace('pham_chain_', '').replace('.json', '')
        
        # 최신 블록
        latest_block = chain[-1]
        data = latest_block['data']
        
        # 기여도 (score + label)
        score = data.get('score', 0.0)
        label = data.get('label', 'UNKNOWN')
        contribution = f"{label} ({score:.4f})" if score else label
        
        # 요약 정보
        return {
            'name': name,
            'file': filename,
            'blocks': len(chain),
            'contribution': contribution,
            'score': score,
            'label': label,
            'author': data.get('author', 'Unknown'),
            'title': data.get('title', name),
            'timestamp': format_timestamp(latest_block.get('timestamp', '')),
            'hash': format_hash(data.get('hash', 'N/A'), 12),
            'cid': format_cid(data.get('cid', 'N/A'), 15),
        }
    except Exception as e:
        return None

def show_all_chains_summary():
    """모든 체인 요약 테이블"""
    chain_files = sorted(glob.glob('pham_chain_*.json'))
    
    if not chain_files:
        print(f"{Colors.WARNING}⚠️  No blockchain chain files found.{Colors.ENDC}")
        return
    
    print("\n" + "="*100)
    print(f"{Colors.BOLD}{Colors.HEADER}📊 BLOCKCHAIN REGISTRY SUMMARY{Colors.ENDC}")
    print("="*100)
    
    summaries = []
    for chain_file in chain_files:
        summary = show_chain_summary(chain_file)
        if summary:
            summaries.append(summary)
    
    if not summaries:
        print(f"{Colors.WARNING}No valid chains found.{Colors.ENDC}")
        return
    
    print(f"\n{Colors.BOLD}Total Chains: {len(summaries)}{Colors.ENDC}")
    print("\n" + "-"*100)
    print(f"{'#':<4} {'File':<30} {'Blocks':<8} {'Grade':<12} {'Score':<10} {'Author':<15}")
    print("-"*100)
    
    for i, s in enumerate(summaries, 1):
        grade_color = get_grade_color(s['label'])
        print(f"{i:<4} {s['name']:<30} {s['blocks']:<8} {grade_color}{s['label']:<12}{Colors.ENDC} {s['score']:<10.4f} {s['author']:<15}")
    
    print("-"*100)
    
    # 통계
    a_high = sum(1 for s in summaries if 'A_HIGH' in s['contribution'])
    avg_blocks = sum(s['blocks'] for s in summaries) / len(summaries) if summaries else 0
    
    print(f"\n{Colors.BOLD}Statistics:{Colors.ENDC}")
    print(f"  • A_HIGH grade: {Colors.OKGREEN}{a_high}/{len(summaries)}{Colors.ENDC} ({100*a_high//len(summaries)}%)")
    print(f"  • Average blocks per chain: {avg_blocks:.1f}")
    print(f"  • Total blocks: {sum(s['blocks'] for s in summaries)}")
    
    print("\n" + "="*100)
    print(f"{Colors.OKCYAN}💡 Use: python3 view_chains.py <filename> for detailed view{Colors.ENDC}")
    print("="*100 + "\n")

# ============================================================================
# 체인 상세 보기
# ============================================================================
def show_chain_detail(chain_file):
    """특정 체인 상세 정보"""
    try:
        with open(chain_file, 'r', encoding='utf-8') as f:
            chain = json.load(f)
    except FileNotFoundError:
        print(f"{Colors.FAIL}❌ File not found: {chain_file}{Colors.ENDC}")
        return
    except json.JSONDecodeError:
        print(f"{Colors.FAIL}❌ Invalid JSON format: {chain_file}{Colors.ENDC}")
        return
    
    if not chain:
        print(f"{Colors.WARNING}⚠️  Empty chain{Colors.ENDC}")
        return
    
    # 파일명
    filename = os.path.basename(chain_file)
    
    print("\n" + "="*100)
    print(f"{Colors.BOLD}{Colors.HEADER}🔗 BLOCKCHAIN CHAIN DETAIL{Colors.ENDC}")
    print("="*100)
    print(f"\n{Colors.BOLD}File:{Colors.ENDC} {filename}")
    print(f"{Colors.BOLD}Total Blocks:{Colors.ENDC} {len(chain)}")
    
    # 체인 무결성 검증
    is_valid, message = verify_chain(chain)
    if is_valid:
        print(f"{Colors.BOLD}Integrity:{Colors.ENDC} {Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    else:
        print(f"{Colors.BOLD}Integrity:{Colors.ENDC} {Colors.FAIL}✗ {message}{Colors.ENDC}")
    
    print("\n" + "-"*100)
    
    # 각 블록 표시
    for i, block in enumerate(chain):
        data = block['data']
        
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}━━━ BLOCK #{block['index']} ━━━{Colors.ENDC}")
        print(f"{Colors.BOLD}Timestamp:{Colors.ENDC} {format_timestamp(block['timestamp'])}")
        
        # 데이터 섹션
        print(f"\n{Colors.BOLD}📄 Data:{Colors.ENDC}")
        print(f"  • Title:        {data.get('title', 'N/A')}")
        print(f"  • Author:       {data.get('author', 'N/A')}")
        print(f"  • Description:  {data.get('description', 'N/A')}")
        
        # 기여도 (색상 적용)
        score = data.get('score', 0.0)
        label = data.get('label', 'UNKNOWN')
        grade_color = get_grade_color(label)
        print(f"  • Grade:        {grade_color}{label}{Colors.ENDC}")
        print(f"  • Score:        {score:.6f}")
        
        # 신호 섹션
        if 'signals' in data:
            signals = data['signals']
            print(f"\n{Colors.BOLD}📊 Signals:{Colors.ENDC}")
            print(f"  • Byte Signal:  {signals.get('byte_signal', 0.0):.4f}")
            print(f"  • Text Signal:  {signals.get('text_signal', 0.0):.4f}")
            print(f"  • AST Signal:   {signals.get('ast_signal', 0.0):.4f}")
            print(f"  • Exec Signal:  {signals.get('exec_signal', 0.0):.4f}")
        
        # 해시 섹션
        print(f"\n{Colors.BOLD}🔐 Hashes:{Colors.ENDC}")
        print(f"  • File SHA-256: {data.get('hash', 'N/A')[:64]}")
        if len(data.get('hash', '')) > 64:
            print(f"                  {data.get('hash', '')[64:]}")
        print(f"  • IPFS CID:     {data.get('cid', 'N/A')[:64]}")
        if len(data.get('cid', '')) > 64:
            print(f"                  {data.get('cid', '')[64:]}")
        
        # 블록 해시
        print(f"\n{Colors.BOLD}⛓️  Block Chain:{Colors.ENDC}")
        
        # Previous hash (Genesis 블록은 없을 수 있음)
        if 'previous_hash' in block:
            prev_hash = block['previous_hash']
            print(f"  • Previous:     {prev_hash[:64]}")
            if len(prev_hash) > 64:
                print(f"                  {prev_hash[64:]}")
        else:
            print(f"  • Previous:     (Genesis Block)")
        
        # Current hash
        curr_hash = str(block.get('hash', 'N/A'))
        print(f"  • Current:      {curr_hash[:64]}")
        if len(curr_hash) > 64:
            print(f"                  {curr_hash[64:]}")
        
        # 체인 연결 검증
        if i > 0 and 'previous_hash' in block:
            if block['previous_hash'] == chain[i-1]['hash']:
                print(f"  • Chain Link:   {Colors.OKGREEN}✓ Valid{Colors.ENDC}")
            else:
                print(f"  • Chain Link:   {Colors.FAIL}✗ Broken{Colors.ENDC}")
        elif i == 0:
            print(f"  • Chain Link:   {Colors.OKCYAN}Genesis{Colors.ENDC}")
        
        if i < len(chain) - 1:
            print(f"\n{Colors.OKCYAN}{'─'*100}{Colors.ENDC}")
    
    print("\n" + "="*100)
    print(f"{Colors.OKGREEN}✅ Chain display complete{Colors.ENDC}")
    print("="*100 + "\n")

# ============================================================================
# 메인
# ============================================================================
def main():
    """메인 함수"""
    # 색상 체크 (파이프 출력 시 비활성화)
    if not sys.stdout.isatty():
        Colors.disable()
    
    # 인자 파싱
    if len(sys.argv) == 1:
        # 인자 없음: 요약 보기
        show_all_chains_summary()
    
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        
        if arg in ['-h', '--help']:
            print(__doc__)
            return
        
        elif arg == '--all':
            # 모든 체인 상세 보기
            chain_files = sorted(glob.glob('pham_chain_*.json'))
            for i, chain_file in enumerate(chain_files, 1):
                show_chain_detail(chain_file)
                if i < len(chain_files):
                    print("\n" + "█"*100 + "\n")
        
        else:
            # 특정 체인 보기
            chain_file = arg
            if not os.path.exists(chain_file):
                # 파일명만 주어진 경우
                chain_file = f"pham_chain_{arg}.json" if not arg.endswith('.json') else arg
            
            if os.path.exists(chain_file):
                show_chain_detail(chain_file)
            else:
                print(f"{Colors.FAIL}❌ File not found: {chain_file}{Colors.ENDC}")
                print(f"\n{Colors.OKCYAN}Available chains:{Colors.ENDC}")
                for f in sorted(glob.glob('pham_chain_*.json')):
                    print(f"  • {os.path.basename(f)}")
    
    else:
        print(f"{Colors.FAIL}Usage: python3 view_chains.py [chain_file.json | --all]{Colors.ENDC}")
        print(f"       python3 view_chains.py -h  for help")

if __name__ == "__main__":
    main()

