# 🔎 FindIt

**Find it. Return it. Reuse it.**
학교 분실물 찾기와 돌려주기를 게임처럼 만든 앱 (Python + Streamlit + SQLite)

---

## 1. 실행 방법

### 가장 쉬운 방법 (Windows, 더블클릭)

1. **Python 설치 (처음 한 번만)**: https://www.python.org/downloads/ 에서 설치
   - 설치 첫 화면에서 **"Add python.exe to PATH" 체크** 필수
2. **`FindIt_실행.bat` 더블클릭**
   - 처음엔 1~3분 설치가 진행됨 (다음부터는 바로 실행)
   - 브라우저가 열리면서 앱이 뜸
   - 검은 창은 앱 쓰는 동안 열어두기. 창을 닫으면 앱 종료
3. 데이터를 처음 상태로 되돌리고 싶으면 **`데모데이터_초기화.bat`** 더블클릭

### 직접 명령어로 하는 방법 (Mission 0 연습용)

처음 한 번만:

```bash
# findit 폴더 안에서
python -m venv .venv                 # Mac은 python3

# 가상환경 켜기
.venv\Scripts\Activate.ps1           # Windows
source .venv/bin/activate            # Mac

pip install -r requirements.txt
```

매번 실행할 때:

```bash
# 가상환경 켜기 (위와 같음)
python seed.py          # 데모 데이터 만들기 (기존 데이터는 지워짐)
streamlit run app.py    # 브라우저에서 앱이 열림
```

규칙이 잘 돌아가는지 테스트:

```bash
python test_story.py    # 규칙 50개를 이야기로 자동 확인
```

---

## 2. 파일 구조

| 파일 | 역할 |
|---|---|
| `app.py` | **화면** 9개 (🏠 Home, 🙋 I found something, 😢 I lost something, 🔎 Browse found items, 🗺️ School map, 📬 My messages, 🏅 My Findy level, 🌍 Our school's impact, 물건 상세) |
| `db.py` | **저장 + 규칙**. 테이블 6개, 기능 함수 전부 (save_item, claim_item, pick_up, spot_check, add_alert …) |
| `lang.py` | **화면 글자** 영어 / 스페인어 사전 (`t("key")`로 꺼내 씀) |
| `seed.py` | 데모용 샘플 데이터 20개 + Jaden 시연 이야기 |
| `test_story.py` | 규칙 테스트 (50개 항목 자동 확인) |
| `screenshots/` | 완성 화면 캡처 |

👉 화면(app.py)과 규칙(db.py)을 나눈 이유: 규칙만 따로 테스트할 수 있고, 화면을 바꿔도 규칙은 안 깨짐

---

## 3. 내 설계가 어디에 들어갔나

| 설계 결정 | 코드 위치 |
|---|---|
| Q5 사진은 DB 안에 저장 | `db.py` items 테이블 `photo BLOB` |
| 기본 규칙: 주운 자리에 그대로 두고 등록 | `save_item` (kept_at 없음) + `where_text` |
| 귀중품(폰·지갑·열쇠·이어폰)은 Lost & Found 데스크에 맡김 | `save_item(valuable=True, kept_at=...)`, `RETURN_SPOT_INFO` |
| 질문/답변(QnA) 없음 — 주인이 "It's mine!"만 누르면 됨 | `claim_item` |
| 일반 물건: "It's mine! I picked it up" → 바로 Returned | `claim_item` |
| 귀중품: "It's mine!" → 데스크 안내 메시지 → 데스크에서 받고 "I picked it up" | `claim_item`, `pick_up` |
| Q13 실명, 전화번호 저장 안 함 | 테이블에 해당 칸 없음 |
| 🆕 로그인(닉네임+비밀번호), 회원가입, 로그아웃(항상 보임) · ⚠️ **데모: 모든 계정 비밀번호 1212** | `log_in`, `sign_up`, `DEMO_PASSWORD`, 로그인 화면 |
| 🆕 물건 카드·지도: 발견 장소 + 지금 있는 곳(그 자리 / 데스크 / 주인에게 / 재사용 박스) | `now_text`, `map_position` |
| 🆕 검색: 단어별로 찾고 많이 맞는 물건부터, 날짜 필터(7일/30일) | `search_items`, `match_score` |
| 🆕 내 알림마다 "지금 맞는 물건 N개" | `alert_matches` (😢 I lost something 화면) |
| 🆕 🌍 Our school's impact: 이번 주 반환 수 | `get_stats()["this_week"]` |
| 🆕 비밀번호 찾기(이메일) — 버튼만 있음, 실제 발송은 나중에 | 로그인 화면 "Forgot your password?" |
| Q14 레벨은 XP로 계산 | `calc_level` |
| Q15 배지 테이블 따로 | `user_badges` 테이블, `give_badges` |
| Q16 7일 지나면 다시 Found | `reset_old_claims` (앱 열 때마다 실행) |
| Q17 XP 점수표 | `db.py` 맨 위 `XP_...` 숫자들 |
| Q18 레벨 기준 0/50/150/300 | `LEVELS` |
| Q19 하루 5개, 내가 올린 물건은 Claim 금지 | `save_item`, `claim_item` 안의 검사 |
| Q20 XP는 반환 때 확정 | `calc_xp` (확정 XP / 예약 XP) |
| 귀중품 Claim 시 주인에게 "어느 데스크로 가라" 메시지 | `claim_item`, `messages` 테이블 |
| 귀중품 등록 보너스 XP | `XP_VALUABLE` |
| 🆕 "아직 거기 있어요 / 없어졌어요" 버튼 + 3일 넘으면 "데스크로 옮겨 주세요" | `spot_check`, `last_check`, `move_to_desk`, `MOVE_TO_DESK_DAYS` |
| 🆕 "잃어버렸어요" 알림: 맞는 물건이 올라오면 메시지 | `add_alert`, `_notify_alerts`, `lost_alerts` 테이블 |
| 🆕 사진 주의 안내 (이름·얼굴·학생증 안 보이게) | 🙋 I found something 화면 |
| 🆕 30일 지나면 Reuse(재사용) 박스로 ⚠️ **잠정 규칙, 학교 정책 확인 필요** · 귀중품은 제외 | `move_old_to_reuse`, `REUSE_AFTER_DAYS` |
| 🆕 영어 / 스페인어 전환 | `lang.py`, 사이드바 🌐 |
| 🆕 이번 주 Top Finders (최근 7일, 닉네임만) | `top_finders` (Home, Our school's impact) |
| 🆕 공정 규칙: 같은 사람 물건은 하루 1개만 찾아갈 수 있음 (점수 부풀리기 방지) | `_check_pair_limit` |

💡 숫자를 바꾸고 싶으면 `db.py` 맨 위 **Settings** 부분만 고치면 됨

### 학교 지도 (Round Rock High School)

- Map 화면 = 실제 위성 지도 (Esri 위성사진 / OpenStreetMap 일반 지도, 오른쪽 위에서 전환)
- **B1~B6** (남색 이름표) = 물건이 발견되는 건물·장소
- **R1~R4** (초록 핀) = Lost & Found 데스크: R1 Front Office · R2 Library Desk · R3 Gym Office · R4 Counselor's Office
- ⚠️ 건물·반환 장소 위치는 **추정값**임. 정확히 맞추는 방법:
  1. Map 화면에서 **📐 Map setup** 켜기
  2. 위성 지도에서 실제 건물을 클릭 → 위도/경도 숫자가 뜸
  3. `db.py` 맨 위 `LOCATIONS`, `RETURN_SPOT_INFO`의 숫자를 바꾸고 저장 → 앱 새로고침

---

## 4. 데모 해보기 (닉네임만 바꾸면 다른 사람이 됨)

### 일반 물건 (질문 없음)
1. **Jaden** → 🙋 I found something → 사진·장소·설명 → Submit (물건은 그 자리에 그대로)
2. **Max** → Home에서 물병 발견 → View details → **"It's mine! I picked it up"** → Returned 🎉

### 귀중품 (Lost & Found 데스크)
1. 🙋 I found something에서 **💎 It's a valuable** 켜기 → 맡긴 데스크 선택 → Submit
2. 주인 → View details → **"It's mine!"** → 메시지로 "R2 Library Desk로 가라" 안내
3. 데스크에서 받고 **"I picked it up"** → Returned 🎉 (본인 확인은 데스크 직원이 직접)

### 새 기능
- **로그인 화면**: 닉네임 + 비밀번호(데모는 모두 **1212**), ✨ Sign up 탭(닉네임·학교 이메일·비밀번호), "Forgot your password?"(이메일 발송은 준비 중)
- **로그아웃**: 화면 오른쪽 위 + 사이드바에 항상 보임. 사람을 바꿀 때 Log out → 다음 사람으로 로그인
- **😢 I lost something** 화면: "blue bottle"처럼 적고 🔔 알림 켜기 → 맞는 물건이 올라오면 메시지
- 물건 상세: **👍 Still there / ❌ Not there anymore** · 3일 넘게 남아 있으면 "데스크로 옮겼어요" 버튼
- 사이드바 **🌐 English / Español**: 모든 화면·메시지·오류가 바뀜 (물건 설명과 장소 이름은 그대로)
- Home·Our school's impact: **🏆 This week's Top Finders**
- ⚠️ Reuse 30일 규칙은 학교 Lost & Found 정책 확인 후 `REUSE_AFTER_DAYS` 숫자만 바꾸면 됨

### 시연용 상황극 (처음부터 끝까지 Jaden 한 명, 비밀번호 1212)

- 물건들은 여러 학생(Nana, Max, BookWorm9, LunchHero …)이 올린 상태로 시작
- Jaden: **180 XP = 3단계 Super Finder**, 새 메시지 2개
  - "white earbuds" 알림 매칭 (Nana가 주워서 Library Desk에 맡김)
  - "Max가 Jaden이 올린 물병을 찾아감"

영상 순서 (가이드 PDF v6 참고):
1. **Jaden 로그인** → Home (Findy 3단계, 메시지 2개)
2. **🙋 I found something**: 파란 물병 등록 (`photos/01.jpg`, Tennis Courts) → 💎 스위치만 보여주고 끄기
3. **😢 I lost something**: "gray scarf" 알림 등록 → 예전 "white earbuds" 알림에 맞는 물건 1개
4. **📬 My messages → Open item** → 이어폰 **"It's mine!"** → Library Desk 안내 → **"I picked it up"**
5. **🏅 My Findy level**: Findy 레벨 1~5 (지난 단계 컬러·작게, 현재 단계 크게, 남은 단계 흑백) → **🌍 Our school's impact** → 🏠 Home에서 **Español**

### 시작 슬라이드 (발표용)
- 앱을 열면 `assets/slides/` 안의 슬라이드 4장이 전체 화면으로 먼저 나옴
- 화면 아무 곳이나 클릭 → 다음 장, 마지막 장에서 클릭 → 로그인 화면
- 슬라이드를 바꾸려면 `assets/slides/` 안의 그림(slide-1.jpg …)을 교체 (이름 순서대로 나옴)
- 슬라이드 없이 바로 시작: 주소 끝에 `?slides=off` (예: http://localhost:8501/?slides=off)
- 브라우저 전체 화면은 **F11**

### 왼쪽 메뉴
🏠 Home · 🙋 I found something · 😢 I lost something · 🔎 Browse found items · 🗺️ School map · 📬 My messages · 🏅 My Findy level · 🌍 Our school's impact
(메뉴 이름은 `lang.py`의 `page_...` 줄에서 바꿀 수 있음)

### 레벨과 배지
- **Findy 레벨 5단계**: New Finder 0 · Finder 50 · Super Finder 150 · Finder Hero 300 · FindIt Legend 500 (`LEVELS`)
- 캐릭터 그림: `assets/levels/level1~5.svg` (`make_art.py`로 다시 그릴 수 있음)
- 특별 배지 4개: Water Bottle Hunter, Book Finder, Sports Finder, Return Hero (못 받은 배지는 흑백)
- 로고: `assets/logo.png`, 아이콘 `assets/icon.png`

💡 업데이트 후 처음 실행할 때는 `데모데이터_초기화.bat`을 한 번 실행(Y) — DB 구조가 바뀌어서 꼭 필요함
