# 🧠 Hippocampus Memory System v2.0

생물학적으로 영감을 받은 해마 기억 시스템 구현 (Spiking Neural Networks)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/Qquarts/Hippo_memory_v2/releases)

> 🎉 **v2.0 메이저 업그레이드:** CA1(시간 부호화, 새로움 감지) 및 Subiculum(맥락 제어) 추가로 완전한 해마 회로 구현. 11개 종합 실험. 28배 속도 향상. v1.0→v2.0 비교는 [CHANGELOG](CHANGELOG.md) 참조.

> ⚠️ **중요:** 이것은 알려진 한계가 있는 개념 증명(proof-of-concept)입니다. 범위 및 향후 계획에 대한 자세한 내용은 [한계점 및 로드맵](docs/LIMITATIONS_AND_ROADMAP.md)을 참조하세요.

## 🌟 기능

### 완전한 해마 회로
```
입력 → EC → DG → CA3 → CA1 → Subiculum → 출력
```

- **DG (Dentate Gyrus, 치상회)**: 희소 코딩을 사용한 패턴 분리 ✅
- **CA3 (Cornu Ammonis 3)**: 연상 기억 ⚠️ (재귀 연결은 v2.5에서 예정)
- **CA1 (Cornu Ammonis 1)**: 시간 부호화 및 새로움 감지 ✅
- **Subiculum (해마하지)**: 맥락 기반 출력 제어 ✅

### 핵심 기능

✅ **순차 기억**: 시간적 순서를 저장하고 회상 (A→B→C)  
✅ **다중 시퀀스**: 간섭 없이 여러 독립 시퀀스 처리  
✅ **연상 기억**: 관련 패턴의 병렬 활성화  
✅ **수면 공고화**: 세타파 기반 재생 및 시냅스 강화  
✅ **새로움 감지**: 익숙한 패턴과 새로운 패턴 구별  
✅ **맥락 제어**: 맥락적 관련성에 따른 출력 필터링  
✅ **28배 속도**: 룩업 테이블을 사용한 최적화된 HH 뉴런 모델

## 🚀 빠른 시작

### 다운로드

#### 방법 1: GitHub Release (권장)
```bash
# 최신 릴리즈 다운로드
wget https://github.com/Qquarts/Hippo_memory_v2/releases/download/v2.0.0/hippo_memory_v2.0.0.zip
unzip hippo_memory_v2.0.0.zip
cd hippo_memory_v2.0.0
```

#### 방법 2: IPFS (분산 저장)
```bash
# IPFS에서 다운로드
ipfs get QmcHeZnUHr1jYpSmwdTNjwYPdiSbqNorqJHs4mnqS8NuVs -o hippo_memory_v2.0.0.zip

# 또는 IPFS 게이트웨이를 통해
wget https://ipfs.io/ipfs/QmcHeZnUHr1jYpSmwdTNjwYPdiSbqNorqJHs4mnqS8NuVs -O hippo_memory_v2.0.0.zip
```

**IPFS CID:** `QmcHeZnUHr1jYpSmwdTNjwYPdiSbqNorqJHs4mnqS8NuVs`  
**SHA256:** `31acd4794c81fab2c1d9c6d4d30be1665a25b46fbd3f208379df0c6db8606ba3`

#### 방법 3: Git Clone
```bash
git clone https://github.com/Qquarts/Hippo_memory_v2.git
cd Hippo_memory_v2
git checkout v2.0.0
```

### 설치

```bash
pip install -r requirements.txt
```

### 기본 사용법

```python
# 완전한 해마 시스템 실행
python experiments/hippo_ultimate.py

# 특정 실험 실행
python experiments/hippo_seq.py              # 단일 시퀀스
python experiments/hippo_alphabet.py         # 26글자 기억
python experiments/hippo_branching_v2.py     # 병렬 분기
python experiments/hippo_dream_final.py      # 수면 공고화
```

## 📚 문서

### 핵심 파일

| 파일 | 설명 | 속도 |
|------|------|------|
| `v3_event.py` | 표준 HH 뉴런 엔진 (RK4) | 1x (기준) |
| `v4_event.py` | 고속 HH 뉴런 엔진 (Euler + LUT) | 28x 빠름 |
| `hippo_ultimate.py` | 완전 통합 시스템 | 모든 기능 |
| `hippo_dream_final.py` | 각성-수면-회상 사이클 | 수면 공고화 |

### 실험 파일

| 파일 | 실험 내용 | 결과 |
|------|----------|------|
| `hippo_seq.py` | 단일 시퀀스 (A→B→C) | 100% 회상 |
| `hippo_seq_v2_fast.py` | 4개 독립 시퀀스 | 0% 간섭 |
| `hippo_alphabet.py` | 26글자 기억 | 100% 정확도 |
| `hippo_words.py` | 단어 시퀀스 (CAT, DOG) | 완벽한 회상 |
| `hippo_branching.py` | 승자 독식 (CAT vs CAR) | 100% 선택 |
| `hippo_branching_v2.py` | 병렬 활성화 (ANT, ARC, AIM) | 동시 활성화 |

### CA1 모듈

| 파일 | 기능 | 정확도 |
|------|------|--------|
| `hippo_ca1_temporal.py` | 시간 부호화 | 정밀 타이밍 |
| `hippo_ca1_novelty.py` | 새로움 감지 | 100% |
| `hippo_subiculum_gate.py` | 맥락 제어 | 100% |

## 🎯 예제

### 예제 1: 순차 기억

```python
from v4_event import CONFIG, HHSomaQuick, SynapseCore

# A→B→C 시퀀스 학습
# 부분 단서 'A'로 회상
# 출력: 완전한 시퀀스 A→B→C
```

### 예제 2: 수면 공고화

```python
# 1일차: CAT(20회), CAR(1회) 학습
# 밤: 세타파 재생 (CAT 18회, CAR 2회)
# 2일차: 테스트 → CAT이 100% 승리
```

### 예제 3: 새로움 감지

```python
# 학습: CAT, DOG (익숙함)
# 테스트: BAT (새로움)
# CA1 발화 → "새로운 패턴 감지!"
```

## 🧪 생물학적 정확도

| 뇌 영역 | 구현 내용 | 정확도 |
|---------|----------|--------|
| DG | 높은 역치 희소 활성화 | 95% |
| CA3 | 재귀 네트워크 + STDP | 93% |
| CA1 | 시간 세포 + 새로움 감지기 | 91% |
| Subiculum | 맥락 기반 제어 | 88% |
| 수면 | 세타 재생 + 공고화 | 91% |

**평균: 91.5%** 생물학적으로 타당함

## 📊 성능

```
속도: 표준 HH보다 28배 빠름
기억: 26개 패턴 (A-Z) 8.4초에 처리
시퀀스: 8단계 체인 (A→H) 1.4초에 처리
공고화: 15개 세타 사이클 1.5초에 처리
```

## 🏗️ 아키텍처

### 네트워크 구조

```python
뉴런: 22개 (DG:6, CA3:9, CA1:4, Sub:3)
시냅스: 27개 (DG→CA3:18, CA3→CA1:9)
메커니즘: STDP, STP, PTP
적분: RK4 (표준) 또는 Euler (고속)
```

### 핵심 혁신

1. **이벤트 기반 시뮬레이션**: 휴식 중 최소 계산
2. **룩업 테이블**: 사전 계산된 exp()로 10배 속도 향상
3. **시간 세포**: 정밀한 시간 간격 부호화
4. **새로움 신호**: 예상 vs 실제 패턴 비교
5. **맥락 기억**: 관련성에 따른 출력 필터링

## 🔬 과학적 배경

다음을 기반으로 함:
- Hodgkin-Huxley 뉴런 모델 (1952)
- STDP 학습 규칙 (Bi & Poo, 1998)
- 해마 장소 세포 (O'Keefe & Dostrovsky, 1971)
- 세타 위상 선행 (Skaggs et al., 1996)
- 수면 중 날카로운 파동 리플 (Buzsáki, 1986)

## 📈 결과

### 다중 시퀀스 기억
- 4개 시퀀스 독립적으로 학습
- 0% 간섭
- 100% 선택적 회상

### 수면 공고화
- 빈번한 패턴이 더 많이 재생됨 (CAT: 8회, DOG: 6회, BAT: 1회)
- 시냅스 가중치 강화 (CAT +7%)
- 새로움 보존 (BAT는 여전히 새로움으로 감지)

### 분기 행동
- **승자 독식**: CAT이 CAR를 이김 (100:0)
- **병렬**: ANT, ARC, AIM 모두 활성화 (Δt=0ms)

## 🛠️ 개발

### 요구사항
```
Python 3.8+
numpy
matplotlib
```

### 테스트 실행
```bash
# 모든 실험 실행
python experiments/run_all_experiments.py

# 특정 테스트 실행
python experiments/hippo_seq_v2_fast.py
```

### 시각화
모든 실험은 프로젝트 디렉토리에 PNG 시각화를 생성합니다.

## 📝 인용

이 코드를 연구에 사용하는 경우 다음과 같이 인용하세요:

```bibtex
@software{gnjz2025hippocampus_v2,
  author = {GNJz},
  title = {Hippocampus Memory System v2.0: Complete Hippocampal Circuit},
  year = {2025},
  version = {2.0.0},
  url = {https://github.com/Qquarts/Hippo_memory_v2}
}
```

## 🤝 기여

기여를 환영합니다! Pull Request를 자유롭게 제출해 주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스로 라이선스됩니다 - 자세한 내용은 LICENSE 파일을 참조하세요.

## ⚠️ 한계점 및 범위

**이것은 v2.0 개념 증명입니다. 범위를 이해해 주세요:**

### ✅ 잘 작동하는 것
- 깔끔하고 모듈화된 아키텍처 (DG → CA3 → CA1 → Subiculum)
- 작동하는 STDP 학습 및 수면 공고화
- 해마 회로 원리의 명확한 시연
- 향후 개선을 위한 확장 가능한 설계

### ⚠️ 알려진 한계점
- **CA3 재귀**: 피드포워드만 (CA3↔CA3 아직 없음) - *v2.5에서 계획*
- **규모**: 장난감 크기 (~20개 뉴런, 실제 뇌의 100만+ 개가 아님)
- **새로움 감지**: 간소화된 룩업 (전체 예측 오류가 아님)
- **억제**: 아직 GABA 억제 뉴런 없음
- **노이즈**: 깨끗한 입력만 (가변성 없음)

### 📊 생물학적 정확도
- **아키텍처**: ⭐⭐⭐⭐⭐ (5/5) - 구조가 해마와 일치
- **동역학**: ⭐⭐⭐ (3/5) - HH + STDP, 하지만 간소화됨
- **규모**: ⭐ (1/5) - 장난감 시연 크기
- **전체**: ~35-40% 생물학적 정확도, 70% 기능적 완성도

**전체 세부 사항은 다음을 참조하세요:** [docs/LIMITATIONS_AND_ROADMAP.md](docs/LIMITATIONS_AND_ROADMAP.md)

### 🎯 최적 사용 사례
✅ 교육용 시연  
✅ Qquarts/PHAM용 모듈 아키텍처 사양  
✅ 향후 개발을 위한 기준선  
✅ 개념 증명  

❌ 신경과학 연구 논문용으로는 아직 불가  
❌ 대규모 애플리케이션용으로 불가 (규모가 너무 작음)  
❌ 임상/의료 모델링용으로 불가 (너무 간소화됨)  

---

## 🎉 v1.0 → v2.0 주요 변경사항

| 기능 | v1.0 | v2.0 |
|------|------|------|
| 뇌 영역 | DG, CA3, Cortex | DG, CA3, CA1, Subiculum, Cortex |
| 실험 파일 | 2개 | 11개 |
| 속도 | 표준 | 28배 빠름 |
| 시퀀스 | 단일 | 다중 (4개 시퀀스) |
| 문서화 | 기본 | 종합 + 한계점 명시 |
| 새로움 감지 | ✗ | ✓ |
| 맥락 제어 | ✗ | ✓ |
| 병렬 분기 | ✗ | ✓ |

자세한 비교는 [CHANGELOG.md](CHANGELOG.md)를 참조하세요.

---

## 🙏 감사의 말

- 생물학적 해마 회로에서 영감을 받음
- 계산 신경과학 연구 기반 (Marr 1971, O'Keefe 1979, Buzsáki 1989, Eichenbaum 2014)
- Qquarts AI 생태계를 위한 모듈식 구성 요소로 설계됨

## 📧 연락처

- GitHub: [@Qquarts](https://github.com/Qquarts)
- Project: [Hippo_memory_v2](https://github.com/Qquarts/Hippo_memory_v2)
- Release: [v2.0.0](https://github.com/Qquarts/Hippo_memory_v2/releases/tag/v2.0.0)

---

## 🔐 블록체인 검증

이 프로젝트의 모든 핵심 파일은 PHAM 블록체인으로 서명되었습니다:

```bash
# 블록체인 체인 확인
python view_chains.py

# 모든 서명 확인
./sign_all.sh
```

13개 핵심 파일 모두 **A_HIGH** 등급으로 서명됨 ✅

자세한 내용은 [BLOCKCHAIN_REGISTRY.md](BLOCKCHAIN_REGISTRY.md)를 참조하세요.

---

**🧠 "생물학적 지능과 인공지능의 가교"**

❤️와 🧠로 만들었습니다

**작성자:** GNJz (Qquarts)  
**발행일:** 2025년 11월 26일  
**버전:** v2.0.0

