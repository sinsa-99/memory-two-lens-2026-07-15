import re, sys

p = 'index.html'
s = open(p, encoding='utf-8').read()
fails = []

def rep(old, new, label):
    global s
    if old not in s:
        fails.append(label); return
    s = s.replace(old, new)

# ---------- 1) 블로그 소스 보충 ----------
rep('7/14(월) 밤', '7/14(화) 밤', 'R1 요일')
rep('약 50% 비쌈</span>. 상장 때 괴리율 3% → 며칠 만에 50%.',
    '49% 비쌈</span> — 7/14 종가 본주 1,941,000원 vs ADR $193.92. 상장 때 괴리율 3% → 두 거래일 만에 49%.', 'R2 괴리49')
rep('기관 매수세 집중.</li>',
    '''기관 매수세 집중.</li>
      <li>$330의 근거는 수급 전망: <b>2027년 D램 공급 +20% vs 수요 +35%</b> — 공급부족이 2027년까지 이어진다는 계산.</li>
      <li>ADR 시세 경로: 7/10(금) 상장 첫날 종가 $168.01 → 7/13(월) 본주 −15.4% 폭락에 동조한 <b>$152.35(−9.32%)</b> → 7/14(화) <b>$193.92(+27.29%)</b>.</li>''', 'R3 시세경로')
rep('7월 말 이후에도 개인은 계속 소외되는 구조.</li>',
    '''7월 말 이후에도 개인은 계속 소외되는 구조.</li>
      <li><b>④ ADR 공매도도 어렵다</b> — 교과서적 수렴 거래(본주 매수 + ADR 공매도)를 하려 해도, ADR 발행량이 <span class="hl">본주의 2.5%</span>뿐인 데다 락업 물량이 많아 빌릴 유통주식 자체가 부족.</li>
      <li><b>⑤ 환위험</b> — 서울은 원화·뉴욕은 달러 결제인데 개장 시간이 달라, 양쪽에 다리를 걸치는 순간 환율 변동에 노출.</li>''', 'R4 장벽45')
rep('⑤ 같은 회사인데 50% 괴리 — 차익거래를 막는 3대 장벽',
    '⑤ 같은 회사인데 49% 괴리 — 차익거래를 막는 5대 장벽', 'R5 제목')
rep('''기관 순매도의 62%</span>.</li>
    </ul>
  </div>''',
    '''기관 순매도의 62%</span>.</li>
    </ul>
    <div class="stance"><b>전망</b> — 이 다섯 장벽이 유지되는 동안 정교한 차익거래는 어렵고, <b>"다음날 서울 본주가 간밤 미장 ADR을 후행 추종"</b>하는 패턴이 이어질 공산이 크다. 7/15 본주 +5.70% 반등도 전날 밤 ADR +27%를 뒤따른 그 패턴의 연장.</div>
  </div>''', 'R6 전망')
rep('전일 약 50%에서 산술상 약 27% 수준으로 하루 만에 급축소',
    '전일 49%에서 산술상 약 28% 수준으로 하루 만에 급축소', 'R7a')
rep('괴리율이 약 50%에서 산술상 약 27% 수준으로 급축소',
    '괴리율이 49%에서 산술상 약 28% 수준으로 급축소', 'R7b')
rep('하루 만에 ~50% → 약 27% 추정', '하루 만에 49% → 약 28% 추정', 'R7c')
rep('괴리 7/14 ~50% → 7/15 약 27% 추정', '괴리 7/14 49% → 7/15 약 28% 추정', 'R7d')
rep('<a href="#snap">오늘 스냅샷</a>',
    '<a href="#snap">오늘 스냅샷</a>\n  <a href="#macro">매크로 노트</a>', 'R8 nav')

MACRO = """<!-- ============ MACRO ============ -->
<section id="macro">
  <h2><span class="tag n">매크로</span> 매크로 노트 — CPI의 착시와 유가 리스크</h2>
  <div class="chap">
    <div class="thead"><h3>6월 CPI — 6년 만의 최대 하락, 그러나 조사 기간의 함정</h3></div>
    <ul>
      <li>6월 CPI 전월비 <span class="hl">−0.4%</span> — 6년 만에 가장 큰 하락, 예상치(−0.2%) 하회. 근원 CPI는 전월과 같은 수준(예상 +0.2%도 하회).</li>
      <li>주역은 에너지: 6/17 미·이란 휴전으로 <b>휘발유 −9.7%</b> 등 에너지가 급락, 운송서비스·중고차도 하락. "에너지 급락 + 나머지 현상 유지"의 조합.</li>
      <li>워시 연준의장은 경계 유지 — <span class="hl">"오늘 아침 데이터를 보고 '임무 완수, 다 잘 돌아간다'고 말하는 사람이 있을 수 있다. 그건 내 견해가 아니다."</span> 그래도 발표 직후 10년물 등 국채금리는 큰 폭 하락, 증시도 긍정 반응.</li>
      <li><b>함정: 이 수치는 6월 조사분.</b> 7/8 이후 미국의 이란 타격 재개, 7/13 이란 항구 해상봉쇄 재개 발표로 브렌트유가 7/1 70달러 밑 → 7/14 <span class="hl">85달러 돌파 (2주 만에 +20%)</span>. 7월 CPI는 유가발 재반등 리스크를 안고 있다.</li>
    </ul>
  </div>
  <div class="chap">
    <div class="thead"><h3>호르무즈 "보호비" 소동 — 하루 만의 철회가 말해주는 것</h3></div>
    <ul>
      <li>트럼프의 "호르무즈해협 통과 화물에 화물가치의 20% 보호비" 발언이 유가 불안을 키웠으나, <b>발표 하루 만에 철회</b> — "중동 지도부와의 매우 생산적인 대화로, 20% 수수료를 걸프 국가들이 미국에 할 무역·투자 딜로 대체"(트루스소셜).</li>
      <li>애초에 성립이 어려운 요율이었다: VLCC(초대형 유조선) 200만 배럴 × $80 = 화물가치 1.6억 달러의 20% = <span class="hl">3,200만 달러</span>. 이란 통행료는 배럴당 $1 = 200만 달러 — 미국이 <b>16배</b>를 더 받겠다는 계산이라, 화주는 이란에 내고 다니는 쪽을 택하게 된다.</li>
      <li>트럼프는 이번 공습을 'military skirmish(소규모 충돌)'로 규정 — 제한 공습으로 압박해 유리한 협상 국면을 만들려는 의도로 읽힌다. 기본 시나리오는 확전보다 협상 복귀.</li>
    </ul>
    <div class="stance"><b>시사점</b> — 2부 민스키 체크 ②의 감시 변수(유가·10Y 금리)가 이미 움직이기 시작했다. CPI 호재로 낮아진 금리 인상 확률은 <b>유가 +20%가 7월 CPI에 반영되는 8월 중순</b>에 재시험대에 오른다. 반도체 랠리의 매크로 전제(금리 안정)는 아직 확정이 아니다.</div>
  </div>
</section>

<!-- ============ VIDEO A ============ -->"""
rep('<!-- ============ VIDEO A ============ -->', MACRO, 'R9 매크로섹션')

OLD_ROW = """이른바 '역(逆)김치 프리미엄' <span class="src">(연합뉴스 7/10)</span></td></tr>"""
NEW_ROW = OLD_ROW + """
    <tr><td>ADR-본주 괴리 "약 50%"</td><td class="vok">✅<span class="note"> 정밀</span></td><td>7/14 종가 대조 시 <b>정확히 49%</b> — 본주 1,941,000원 vs ADR $193.92(+27.29%). 경로: 7/10 $168.01 → 7/13 $152.35(−9.32%) → 7/14 $193.92 <span class="src">(종가 시세 대조)</span></td></tr>"""
rep(OLD_ROW, NEW_ROW, 'R10 팩트체크행')

rep('칩플레이션(컴퓨터 세부 +17%) 지속 여부 + 유가·10Y 금리. 민스키 체크 ②의 감시 변수.',
    '칩플레이션(컴퓨터 세부 +17%) 지속 여부 + 유가·10Y 금리. 브렌트가 7/1 70달러 밑 → 7/14 85달러+(2주 +20%)로 이미 반등 — 7월 CPI 재상승 리스크가 민스키 체크 ②의 1순위 감시 변수.', 'R11 캘린더')
rep('차트 18장 + 웹 조사 10건 (v2: 국내 차트 반영)',
    '차트 18장 · 팩트체크 11건 · 매크로 노트', 'R12 배지')

# ---------- 2) 일봉=왼쪽 / 주봉=오른쪽 전면 교체 ----------
def get_block(text, src, start=0):
    pat = re.compile(r'[ \t]*<figure class="fig" onclick="lb\(\'charts/' + re.escape(src) + r'\'\)">.*?</figure>', re.S)
    return pat.search(text, start)

def swap_first(text, srcA, srcB, label, start=0):
    # srcA가 앞, srcB가 뒤에 있는 상태를 뒤집는다
    mA = get_block(text, srcA, start)
    mB = get_block(text, srcB, start)
    if not mA or not mB or mA.start() >= mB.start():
        fails.append(label); return text
    return text[:mA.start()] + mB.group(0) + text[mA.end():mB.start()] + mA.group(0) + text[mB.end():]

# 챕터 내 페어 (첫 등장 기준)
s = swap_first(s, 'samsung_weekly.png', 'soxl_daily.png', 'S1 A③')
s = swap_first(s, 'dell_weekly.png', 'mu_daily.png', 'S2 B①')
s = swap_first(s, 'ter_weekly.png', 'ter_daily.png', 'S3 B⑤')
s = swap_first(s, 'amd_weekly.png', 'amd_daily.png', 'S4 B⑦')

# 갤러리 (두 번째 등장 = 갤러리 시작 이후)
g = s.index('<div class="gal">')
s = swap_first(s, 'mu_weekly.png', 'mu_daily.png', 'G1 MU', g)
s = swap_first(s, 'sndk_weekly.png', 'sndk_daily.png', 'G2 SNDK', g)
s = swap_first(s, 'amd_weekly.png', 'amd_daily.png', 'G3 AMD', g)
s = swap_first(s, 'ter_weekly.png', 'ter_daily.png', 'G4 TER', g)
s = swap_first(s, 'samsung_weekly.png', 'samsung_daily.png', 'G5 삼전', g)
s = swap_first(s, 'hynix_weekly.png', 'hynix_daily.png', 'G6 하이닉스1', g)
s = swap_first(s, 'hynix_weekly.png', 'hynix_daily_wide.png', 'G7 하이닉스2', g)

open(p, 'w', encoding='utf-8').write(s)
if fails:
    print('실패:', fails); sys.exit(1)
print("모든 패치 성공. '약 27%' 잔존:", s.count('약 27%'), "/ '약 50% 비쌈' 잔존:", s.count('약 50% 비쌈'))
