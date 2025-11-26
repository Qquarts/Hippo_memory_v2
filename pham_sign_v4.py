#!/usr/bin/env python3
# =============================================================================
# pham_sign_v4.py (주석 상세판)
# =============================================================================
# 📜 PHAM Sign v4 — 완전한 기여도 Ledger + Blockchain Reward 시스템
#
# 🎯 핵심 혁신 (v3 대비):
#   1. ✅ raw_bytes/raw_text 저장 → IPFS 없어도 정확한 diff 가능
#   2. ✅ 정석 블록체인 해시 구조 (index|prev|timestamp|data_hash)
#   3. ✅ 데이터 구조 평탄화 (contribution 객체 제거)
#   4. ✅ 블록체인 보상 시스템 (--pay 옵션)
#
# ⚙️ 사용 방법:
#   python3 pham_sign_v4.py <파일> --author <이름> --desc "<설명>" [--exec "<명령>"] [--pay]
#
# 💡 예시:
#   python3 pham_sign_v4.py my_code.py \
#       --author "GNJz" \
#       --desc "기능 추가" \
#       --exec "python3 {file}" \
#       --pay
#
# 📂 결과물:
#   - 블록체인 로그: pham_chain_<filename>.json
#   - 각 블록에 raw_bytes/raw_text 포함 (완전한 기록)
#
# =============================================================================

# 📦 Qquarts Co Present 
# 🖋️ 지은이: GNJz

import argparse
import hashlib
import json
import time
import subprocess
import shlex
import difflib
import ast
import tempfile
import os
import shutil
import sys
from pathlib import Path

# =============================================================================
# 🔗 Blockchain 라이브러리 (Optional)
# =============================================================================
# Web3와 dotenv가 설치되어 있으면 블록체인 보상 기능 활성화
# 설치: pip install web3 python-dotenv
try:
    from web3 import Web3
    from dotenv import load_dotenv
    BLOCKCHAIN_AVAILABLE = True
except:
    BLOCKCHAIN_AVAILABLE = False

# =============================================================================
# 📁 체인 파일 이름 결정
# =============================================================================
# 서명 대상 파일명 기준으로 체인 파일 분리 생성
# 예: my_code.py → pham_chain_my_code.json

if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
    target_name = Path(sys.argv[1]).stem
    CHAIN_FILE = f"pham_chain_{target_name}.json"
else:
    CHAIN_FILE = "pham_chain_default.json"

# =============================================================================
# ⚙️ Configuration (기여도 계산 설정)
# =============================================================================
# 📊 가중치 설정 (총합 = 1.0)
W_BYTE = 0.25   # 바이트 변경 비율 가중치
W_TEXT = 0.35   # 텍스트 유사도 가중치
W_AST  = 0.30   # AST 구조 변경 가중치
W_EXEC = 0.10   # 실행 결과 변화 가중치

# 🚫 스팸 필터 임계값
MIN_BYTE_CHANGE = 0.002   # 0.2% 미만 바이트 변경 → 의심
THRESHOLD_LOW   = 0.12    # 12% 미만 점수 → SPAM

# ✅ 실행 허용 바이너리 (화이트리스트)
# 보안을 위해 허용된 실행 파일만 실행 가능
ALLOWED_EXEC_BINS = ("python3", "pytest", "node", "bash")

# 🎨 ANSI 색상 코드
GREEN = '\033[92m'   # 성공 메시지
YELLOW = '\033[93m'  # 경고 메시지
RED = '\033[91m'     # 오류 메시지
CYAN = '\033[96m'    # 정보 메시지
ENDC = '\033[0m'     # 색상 초기화

# =============================================================================
# 🔐 Hash Functions (SHA256)
# =============================================================================
def sha256_bytes(b: bytes):
    """
    바이트 데이터의 SHA256 해시를 계산합니다.
    
    Args:
        b: 해시를 계산할 바이트 데이터
    
    Returns:
        64자리 16진수 해시 문자열
    """
    return hashlib.sha256(b).hexdigest()


def sha256_text(s: str):
    """
    텍스트의 SHA256 해시를 계산합니다.
    
    Args:
        s: 해시를 계산할 문자열
    
    Returns:
        64자리 16진수 해시 문자열
    """
    return hashlib.sha256(s.encode()).hexdigest()


# =============================================================================
# 🛡️ Safe Execution (안전한 명령 실행)
# =============================================================================
def safe_run(cmd_list, timeout=10, cwd=None):
    """
    지정된 커맨드를 안전하게 실행합니다.
    
    Args:
        cmd_list: 실행할 명령어 리스트 (예: ["python3", "test.py"])
        timeout: 실행 제한 시간 (초)
        cwd: 실행 디렉터리 (None이면 현재 디렉터리)
    
    Returns:
        (return_code, stdout, stderr) 튜플
        - return_code: 0 = 성공, 그 외 = 실패
        - stdout: 표준 출력
        - stderr: 표준 에러
    
    ⚠️ 주의:
        shell=False로 설정하여 쉘 인젝션 공격을 방지합니다.
    """
    try:
        p = subprocess.run(
            cmd_list,
            capture_output=True,    # stdout/stderr 캡처
            text=True,              # 텍스트 모드
            timeout=timeout,        # 타임아웃 설정
            cwd=cwd,               # 실행 디렉터리
            shell=False            # 쉘 인젝션 방지
        )
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", str(e)


# =============================================================================
# 💾 JSON I/O (체인 파일 읽기/쓰기)
# =============================================================================
def load_json(path):
    """
    JSON 체인 파일을 로드합니다.
    
    Args:
        path: JSON 파일 경로
    
    Returns:
        블록 리스트 (파일이 없거나 손상되면 빈 리스트)
    """
    if Path(path).exists():
        try:
            return json.loads(Path(path).read_text("utf-8"))
        except:
            # JSON 파싱 실패 시 빈 체인으로 시작
            return []
    return []


def save_json(path, obj):
    """
    JSON 체인 파일을 저장합니다.
    
    Args:
        path: JSON 파일 경로
        obj: 저장할 블록 리스트
    """
    Path(path).write_text(
        json.dumps(obj, indent=2, ensure_ascii=False),
        "utf-8"
    )


# =============================================================================
# 📐 Diff Functions (변경 비율 계산)
# =============================================================================
def compute_byte_ratio(old_bytes, new_bytes):
    """
    이전 바이트 대비 변경된 바이트 비율을 계산합니다.
    
    계산 방식:
        1. 같은 위치의 서로 다른 바이트 개수 세기
        2. 파일 크기 차이 추가
        3. 이전 파일 크기로 나누기
    
    Args:
        old_bytes: 이전 파일의 바이트 데이터
        new_bytes: 새 파일의 바이트 데이터
    
    Returns:
        0.0 ~ 1.0 범위의 변경 비율
        - 0.0 = 변경 없음
        - 1.0 = 완전히 다름
    
    특수 케이스:
        - 이전 파일이 없으면 (첫 서명) → 1.0 반환
    """
    if not old_bytes:
        return 1.0  # 첫 서명 시 100% 변경으로 간주
    
    # 바이트별로 비교하여 변경된 개수 세기
    changed = sum(1 for (a, b) in zip(old_bytes, new_bytes) if a != b)
    
    # 파일 크기 차이 추가
    changed += abs(len(new_bytes) - len(old_bytes))
    
    # 비율 계산 (0.0 ~ 1.0 범위)
    return changed / max(len(old_bytes), 1)


def text_similarity(a, b):
    """
    텍스트 유사도를 계산합니다.
    
    difflib.SequenceMatcher를 사용하여 문자열 유사도 측정
    
    Args:
        a: 이전 텍스트
        b: 새 텍스트
    
    Returns:
        0.0 ~ 1.0 범위의 유사도
        - 0.0 = 완전히 다름
        - 1.0 = 동일
    """
    if not a:
        return 0.0  # 이전 텍스트 없으면 유사도 0
    return difflib.SequenceMatcher(None, a, b).ratio()


def count_ast_nodes(text):
    """
    Python 코드의 AST 노드 개수를 계산합니다.
    
    AST (Abstract Syntax Tree) = 추상 구문 트리
    코드 구조를 트리 형태로 표현한 것
    
    예시:
        def hello():     → FunctionDef 노드
            print("hi")  → Call, Name, Constant 노드
        
        총 노드 수 ≈ 코드 복잡도
    
    Args:
        text: Python 소스 코드
    
    Returns:
        AST 노드 개수 (파싱 실패 시 0)
    """
    try:
        t = ast.parse(text)
        return sum(1 for _ in ast.walk(t))
    except:
        return 0  # 파싱 실패 (구문 오류 등)


def ast_edit(old_text, new_text):
    """
    AST 구조 변경 비율을 계산합니다.
    
    계산 방식:
        1. 이전 코드와 새 코드의 AST 노드 수 계산
        2. 노드 수 차이를 최댓값으로 나누기
    
    Args:
        old_text: 이전 코드
        new_text: 새 코드
    
    Returns:
        0.0 ~ 1.0 범위의 변경 비율
        - 0.0 = 구조 변경 없음
        - 1.0 = 완전히 다른 구조
    
    예시:
        이전: def hello(): pass (노드 5개)
        새로: def hello(): print("hi") (노드 8개)
        → |8-5| / max(5,8) = 3/8 = 0.375
    """
    try:
        o = count_ast_nodes(old_text)
        n = count_ast_nodes(new_text)
        
        if max(o, n) > 0:
            return abs(o - n) / max(o, n)
        else:
            return 1.0  # 둘 다 빈 코드
    except:
        return 0.5  # 계산 실패 시 중간 값


# =============================================================================
# 🚀 Exec Scoring (실행 결과 비교)
# =============================================================================
def exec_and_score(template, file_path, old_output):
    """
    코드를 실행하고 이전 출력과 비교하여 점수를 계산합니다.
    
    실행 결과 체인 (Exec Output Chaining):
        1. 코드 실행 → 출력 저장
        2. 다음 버전 실행 → 이전 출력과 비교
        3. 차이가 크면 → 높은 기여도 점수
    
    Args:
        template: 실행 명령어 템플릿 (예: "python3 {file}")
        file_path: 실행할 파일 경로
        old_output: 이전 실행 결과 출력
    
    Returns:
        (exec_signal, new_output, exec_status) 튜플
        - exec_signal: 0.0 ~ 1.0 범위의 출력 변화 점수
        - new_output: 새로운 실행 결과
        - exec_status: 실행 상태 (no-exec, blocked, failed, init, ok)
    
    ⚠️ 주의:
        - bash -c 사용 (보안 이슈 존재)
        - v4.1(하드닝)에서는 직접 실행으로 개선됨
    """
    # 1. 명령어 템플릿 검증
    if not template or "{file}" not in template:
        return 0.0, "", "no-exec"
    
    # 2. 화이트리스트 검증
    parts = shlex.split(template)
    if not any(parts[0].endswith(a) for a in ALLOWED_EXEC_BINS):
        return 0.0, "", "blocked"  # 허용되지 않은 바이너리
    
    # 3. 실행 명령어 구성
    cmd = template.format(file=shlex.quote(str(file_path)))
    rc, out, err = safe_run(
        ["bash", "-c", cmd],
        timeout=10,
        cwd=str(file_path.parent)
    )
    new_out = out or ""
    
    # 4. 실행 실패 처리
    if rc != 0:
        return 0.0, new_out, "failed"
    
    # 5. 첫 실행 (이전 출력 없음)
    if not old_output:
        return 0.2, new_out, "init"  # 첫 실행은 0.2 점수 부여
    
    # 6. 이전 출력과 비교
    sim = difflib.SequenceMatcher(None, old_output, new_out).ratio()
    
    # 유사도가 낮을수록 (변화가 클수록) 점수가 높음
    return 1.0 - sim, new_out, "ok"


# =============================================================================
# 🎯 Contribution Score (기여도 점수 계산)
# =============================================================================
def compute_score(old_bytes, old_text, new_bytes, new_text, exec_cmd, path, prev_output):
    """
    4가지 신호를 조합하여 최종 기여도 점수를 계산합니다.
    
    📊 4-Signal 시스템:
        1. Byte Signal (W=0.25): 바이트 변경 비율
        2. Text Signal (W=0.35): 텍스트 유사도 (1 - similarity)
        3. AST Signal  (W=0.30): AST 구조 변경
        4. Exec Signal (W=0.10): 실행 결과 변화
    
    계산 공식:
        score = (W_BYTE × byte_sig + W_TEXT × text_sig + 
                 W_AST × ast_sig + W_EXEC × exec_sig) / weight_sum
    
    Args:
        old_bytes: 이전 파일 바이트
        old_text: 이전 파일 텍스트
        new_bytes: 새 파일 바이트
        new_text: 새 파일 텍스트
        exec_cmd: 실행 명령어 템플릿
        path: 파일 경로
        prev_output: 이전 실행 결과
    
    Returns:
        {
            "score": float,         # 최종 점수 (0.0 ~ 1.0)
            "signals": {            # 각 신호별 점수
                "byte": float,
                "text": float,
                "ast": float,
                "exec": float
            },
            "new_output": str,      # 새로운 실행 결과
            "exec_stat": str        # 실행 상태
        }
    """
    # 1️⃣ Byte Signal 계산
    byte_sig = min(compute_byte_ratio(old_bytes, new_bytes), 1.0)
    
    # 2️⃣ Text Signal 계산 (1 - 유사도 = 차이)
    text_sig = 1.0 - text_similarity(old_text, new_text)
    
    # 3️⃣ AST Signal 계산
    ast_sig = ast_edit(old_text, new_text)
    
    # 4️⃣ Exec Signal 계산 (옵션)
    exec_sig = 0.0
    new_out = ""
    exec_stat = ""
    
    if exec_cmd:
        exec_sig, new_out, exec_stat = exec_and_score(exec_cmd, path, prev_output)
    
    # 5️⃣ 가중 평균 계산
    total = (W_BYTE * byte_sig + 
             W_TEXT * text_sig + 
             W_AST * ast_sig + 
             W_EXEC * exec_sig)
    
    # 가중치 합 (exec가 없으면 W_EXEC 제외)
    weight = (W_BYTE + W_TEXT + W_AST + (W_EXEC if exec_cmd else 0))
    
    score = total / weight if weight > 0 else 0.0
    score = max(0.0, min(1.0, score))  # 0.0 ~ 1.0 클램프
    
    return {
        "score": score,
        "signals": {
            "byte": byte_sig,
            "text": text_sig,
            "ast": ast_sig,
            "exec": exec_sig
        },
        "new_output": new_out,
        "exec_stat": exec_stat
    }


# =============================================================================
# 🏷️ Classification (기여도 레이블 분류)
# =============================================================================
def classify(score):
    """
    점수를 기반으로 기여도 레이블을 분류합니다.
    
    분류 기준:
        - 0.8 이상: A_HIGH     (⭐ 높은 기여도)
        - 0.5 이상: B_MEDIUM   (✅ 중간 기여도)
        - 0.12 이상: C_LOW     (⚠️ 낮은 기여도)
        - 0.12 미만: SPAM      (🚫 스팸 의심)
    
    Args:
        score: 기여도 점수 (0.0 ~ 1.0)
    
    Returns:
        "A_HIGH", "B_MEDIUM", "C_LOW", "SPAM" 중 하나
    """
    if score >= 0.8:
        return "A_HIGH"
    if score >= 0.5:
        return "B_MEDIUM"
    if score >= THRESHOLD_LOW:  # 0.12
        return "C_LOW"
    return "SPAM"


# =============================================================================
# 💰 Blockchain Reward (블록체인 보상 시스템)
# =============================================================================
def blockchain_reward(score):
    """
    기여도 점수를 기반으로 PHAM 토큰을 창작자에게 전송합니다.
    
    💡 수익 공유 철학:
        "Code is Free. Success is Shared."
        - 코드는 자유롭게 사용
        - 수익 발생 시 창작자에게 6% 로열티 후원
    
    보상 계산:
        base_amount = score × 1000 PHAM
        royalty = base_amount × 0.06 (6%)
    
    예시:
        score = 0.9 → 1000 × 0.9 × 0.06 = 54 PHAM 전송
    
    Args:
        score: 기여도 점수 (0.0 ~ 1.0)
    
    필요 설정 (.env 파일):
        MY_PRIVATE_KEY: 보내는 지갑 개인키
        INFURA_URL: Ethereum RPC URL
        PHAM_CONTRACT_ADDRESS: PHAM 토큰 컨트랙트 주소
    
    ⚠️ 주의:
        - Web3 라이브러리 필요: pip install web3 python-dotenv
        - Gas 비용 발생
        - 실제 블록체인 트랜잭션
    """
    # 1. Web3 라이브러리 확인
    if not BLOCKCHAIN_AVAILABLE:
        print(f"{YELLOW}⚠ web3 없음 — reward skipped{ENDC}")
        return
    
    # 2. .env 파일에서 설정 로드
    load_dotenv()
    PRIV = os.getenv("MY_PRIVATE_KEY")
    URL = os.getenv("INFURA_URL")
    PHAM = os.getenv("PHAM_CONTRACT_ADDRESS")
    CREATOR = "0x99779F19376c4740d4F555083F6dcB2B47C76bF5"  # 창작자 지갑
    
    # 3. 설정 검증
    if not (PRIV and URL and PHAM):
        print(f"{RED}⚠ .env incomplete{ENDC}")
        return
    
    try:
        # 4. Web3 연결
        w3 = Web3(Web3.HTTPProvider(URL))
        acct = w3.eth.account.from_key(PRIV)
        
        # 5. ERC-20 Transfer ABI (최소)
        abi = '[{"name":"transfer","type":"function","stateMutability":"nonpayable","inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"outputs":[{"name":"","type":"bool"}]}]'
        contract = w3.eth.contract(address=PHAM, abi=abi)
        
        # 6. 보상 계산
        base = int(score * 1000)  # 점수 × 1000 PHAM
        amount = w3.to_wei(base, 'ether')
        royalty = int(amount * 0.06)  # 6% 로열티
        
        # 7. 트랜잭션 생성
        tx = contract.functions.transfer(CREATOR, royalty).build_transaction({
            "from": acct.address,
            "nonce": w3.eth.get_transaction_count(acct.address),
            "gas": 100000,
            "gasPrice": w3.eth.gas_price
        })
        
        # 8. 트랜잭션 서명 및 전송
        signed = w3.eth.account.sign_transaction(tx, PRIV)
        txh = w3.eth.send_raw_transaction(signed.rawTransaction)
        
        print(f"{GREEN}Reward TX sent: {w3.to_hex(txh)}{ENDC}")
    except Exception as e:
        print(f"{RED}Reward error: {e}{ENDC}")


# =============================================================================
# 🌐 IPFS Integration (파일 저장 및 검색)
# =============================================================================
def ipfs_add(path):
    """
    파일을 IPFS에 업로드하고 CID를 반환합니다.
    
    IPFS (InterPlanetary File System):
        - 분산 파일 시스템
        - 콘텐츠 기반 주소 (CID)
        - 영구 저장
    
    Args:
        path: 업로드할 파일 경로
    
    Returns:
        CID 문자열 (업로드 실패 시 "CID-unavailable")
    
    ⚠️ 주의:
        - IPFS 데몬 실행 필요: ipfs daemon
        - 타임아웃 8초
    """
    try:
        rc, out, err = safe_run(["ipfs", "add", "-Q", str(path)], timeout=8)
        if rc == 0 and out.strip():
            return out.strip()
    except:
        pass
    return "CID-unavailable"


def ipfs_cat(cid):
    """
    IPFS에서 CID에 해당하는 내용을 가져옵니다.
    
    Args:
        cid: IPFS CID
    
    Returns:
        파일 내용 (실패 시 None)
    
    ⚠️ v4의 혁신:
        - IPFS 로드 실패해도 raw_bytes/raw_text에서 복구 가능
        - 따라서 IPFS는 백업 용도로만 사용
    """
    try:
        rc, out, err = safe_run(["ipfs", "cat", cid], timeout=10)
        if rc == 0:
            return out
    except:
        pass
    return None


# =============================================================================
# 🔗 Blockchain-style Block Hash (정석 블록 해시)
# =============================================================================
def compute_block_hash(index, prev_hash, timestamp, data_dict):
    """
    ✅ v4의 혁신: 정석 블록체인 해시 구조
    
    Bitcoin/Ethereum 스타일 블록 해시:
        1. 데이터를 먼저 해시화 → data_hash
        2. index|prev_hash|timestamp|data_hash 구조
        3. 최종 해시 계산
    
    구조:
        block_hash = SHA256(
            f"{index}|{prev_hash}|{timestamp}|{SHA256(data)}"
        )
    
    장점:
        - 명확한 구분자 (|)
        - 2단계 해시 (데이터 → 블록)
        - 표준 블록체인 구조
    
    Args:
        index: 블록 인덱스
        prev_hash: 이전 블록 해시
        timestamp: 블록 생성 시각
        data_dict: 블록 데이터 (딕셔너리)
    
    Returns:
        64자리 16진수 블록 해시
    """
    # 1. 데이터 해시 계산
    data_hash = sha256_text(json.dumps(data_dict, sort_keys=True))
    
    # 2. 블록 문자열 구성 (구분자 | 사용)
    s = f"{index}|{prev_hash}|{timestamp}|{data_hash}"
    
    # 3. 최종 블록 해시 계산
    return hashlib.sha256(s.encode()).hexdigest()


# =============================================================================
# 🎯 Main (메인 실행 함수)
# =============================================================================
def main():
    """
    메인 실행 흐름:
        1. 인자 파싱
        2. 파일 읽기
        3. 체인 로드 및 이전 블록 검색
        4. 기여도 점수 계산
        5. 블록체인 보상 (--pay 옵션)
        6. IPFS 업로드
        7. 블록 생성 및 저장
        8. 결과 출력
    """
    # 1️⃣ 인자 파싱
    p = argparse.ArgumentParser()
    p.add_argument("file", help="서명할 파일 경로")
    p.add_argument("--author", default="unknown", help="작성자 이름")
    p.add_argument("--desc", default="", help="변경 사항 설명")
    p.add_argument("--exec", default=None, help="실행 명령어 (예: python3 {file})")
    p.add_argument("--pay", action="store_true", help="블록체인 보상 트리거 (score >= 0.5)")
    args = p.parse_args()
    
    # 2️⃣ 파일 존재 확인
    target = Path(args.file)
    if not target.exists():
        print(f"{RED}file not found{ENDC}")
        return
    
    # 3️⃣ 새 파일 읽기
    new_bytes = target.read_bytes()
    try:
        new_text = new_bytes.decode("utf-8")
    except:
        new_text = ""  # 바이너리 파일
    
    new_hash = sha256_bytes(new_bytes)
    
    # 4️⃣ 체인 로드 및 최신 블록 검색
    chain = load_json(CHAIN_FILE)
    latest = None
    
    # 역순으로 검색하여 같은 파일의 최신 블록 찾기
    for b in reversed(chain):
        if b.get("data", {}).get("title") == target.name:
            latest = b
            break
    
    # 5️⃣ 이전 버전 로드 (✅ v4의 혁신: raw_bytes/raw_text 사용)
    old_bytes = b""
    old_text = ""
    prev_out = ""
    
    if latest:
        # 동일 해시 체크 (파일 변경 없음)
        if latest["data"]["hash"] == new_hash:
            print(f"{YELLOW}no change — skip{ENDC}")
            return
        
        # 이전 실행 결과 로드
        prev_out = latest["data"].get("exec_output", "")
        
        # ✅ v4: raw_bytes/raw_text에서 이전 버전 로드
        # → IPFS 없어도 정확한 diff 가능!
        if "raw_bytes" in latest["data"]:
            old_bytes = bytes.fromhex(latest["data"]["raw_bytes"])
        if "raw_text" in latest["data"]:
            old_text = latest["data"]["raw_text"]
    
    # 6️⃣ 임시 디렉터리 생성
    tmpdir = Path(tempfile.mkdtemp(prefix="pham_", dir="/tmp"))
    
    try:
        # 7️⃣ 기여도 점수 계산
        res = compute_score(
            old_bytes, old_text,
            new_bytes, new_text,
            args.exec, target, prev_out
        )
        score = res["score"]
        label = classify(score)
        
        # 8️⃣ 블록체인 보상 (--pay 옵션)
        if args.pay and score >= 0.5:
            blockchain_reward(score)
        
        # 9️⃣ IPFS 업로드
        cid = ipfs_add(target)
        
        # 🔟 Genesis 블록 생성 (체인이 비어있으면)
        if not chain:
            chain = [{
                "index": 0,
                "timestamp": time.time(),
                "data": {"name": "GENESIS"},
                "hash": "0"
            }]
        
        # 1️⃣1️⃣ 블록 데이터 구성
        prev_hash = chain[-1]["hash"]
        timestamp = time.time()
        
        # ✅ v4: raw_bytes/raw_text 저장 (핵심 혁신!)
        block_data = {
            "title": target.name,
            "author": args.author,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "hash": new_hash,
            "cid": cid,
            "description": args.desc,
            "score": round(score, 4),
            "label": label,
            "signals": res["signals"],
            "exec_output": res["new_output"],
            "raw_bytes": new_bytes.hex(),  # ✅ 바이트를 hex로 저장
            "raw_text": new_text            # ✅ 텍스트 직접 저장
        }
        
        # 1️⃣2️⃣ 블록 생성
        block = {
            "index": len(chain),
            "timestamp": timestamp,
            "data": block_data,
            "previous_hash": prev_hash
        }
        
        # ✅ v4: 정석 블록체인 해시 계산
        block["hash"] = compute_block_hash(
            block["index"],
            prev_hash,
            timestamp,
            block_data
        )
        
        # 1️⃣3️⃣ 체인에 추가 및 저장
        chain.append(block)
        save_json(CHAIN_FILE, chain)
        
        # 1️⃣4️⃣ 결과 출력
        emoji = {
            "A_HIGH": "⭐",
            "B_MEDIUM": "✅",
            "C_LOW": "⚠️",
            "SPAM": "🚫"
        }[label]
        
        color = (GREEN if label == "A_HIGH" else
                CYAN if label == "B_MEDIUM" else
                YELLOW if label == "C_LOW" else RED)
        
        print(f"{color}{emoji} contribution: {label} ({score:.4f}){ENDC}")
        print(f"→ block {block['index']} added to {CHAIN_FILE}")
    
    finally:
        # 1️⃣5️⃣ 임시 디렉터리 정리
        shutil.rmtree(tmpdir, ignore_errors=True)


# =============================================================================
# 🚀 Entry Point
# =============================================================================
if __name__ == "__main__":
    main()


# =============================================================================
# 📜 PHAM-OPEN LICENSE v2.0 (Profit-Sharing / Trustware)
# (C) 2025 Qquarts Co / GNJz
#
# ⚖️ 1. 사용 원칙 (Usage Principle)
#   - [자유로운 사용]: 이 코드는 누구나 무료로 복제, 수정, 연구, 실행할 수 있습니다.
#   - [학습과 연구]: 학생, 연구자, 개발자는 비용 부담 없이 이 기술을 마음껏 활용하세요.
#
# 💰 2. 수익 분배 (Revenue Sharing)
#   - [성공 보수]: 만약 당신이 이 코드를 사용하여 금전적 수익(Profit)을 창출하거나,
#     상업적 프로젝트에서 성과를 냈다면, 그때 수익의 일부(예: 6%)를 원작자에게 후원합니다.
#   - [신뢰 기반]: 이것은 법적 강제가 아닌, 블록체인에 기록된 '신뢰(Trust)'에 기반한 약속입니다.
#
# 🔗 3. 기여의 기록 (Proof of Contribution)
#   - 이 코드를 사용할 때 `pham_sign_v4.py`를 통해 당신의 기여를 블록체인에 남기세요.
#   - 당신의 성공이 곧 나의 성공이며, 그 기록은 영원히 남습니다.
#
# 🏦 원작자 지갑 (Patron Address):
#   0x99779F19376c4740d4F555083F6dcB2B47C76bF5
#
# "Code is Free. Success is Shared. Ledger is Complete."
# =============================================================================

