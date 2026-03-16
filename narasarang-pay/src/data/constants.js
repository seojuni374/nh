// ─── 실적 구간 ────────────────────────────────────────────────────────────────
export const thresholds = [
  { key: "starter", label: "기본 구간", min: 0, multiplier: 1, icon: "🌱" },
  { key: "steady", label: "실속 구간", min: 50000, multiplier: 1.08, icon: "📈" },
  { key: "focus", label: "집중 구간", min: 120000, multiplier: 1.16, icon: "🔥" },
  { key: "plus", label: "확장 구간", min: 200000, multiplier: 1.24, icon: "💎" },
];

// ─── 계급별 퍼소나 ─────────────────────────────────────────────────────────────
export const personas = {
  pvt: {
    key: "pvt", label: "이등병", avgSpend: 55000,
    salary: 200000, rankLabel: "이등병",
    desc: "입대 초반, PX·편의점 위주 소비",
    salaryNote: "적금 제외 가용 20만 원",
    dday: 540,
    weights: { PX: 1.4, CONVENIENCE: 1.25, GAME: 1.05, DELIVERY: 1.0, TRANSIT: 0.95, CAFE: 0.85, DIGITAL: 0.95, HEALTH: 0.9 },
    quickBias: 1.3,
    tips: ["PX 할인 집중 활용", "편의점 소액 결제도 카드로", "적금 자동이체 설정 필수"],
  },
  pfc: {
    key: "pfc", label: "일병", avgSpend: 90000,
    salary: 350000, rankLabel: "일병",
    desc: "적응 완료, PX·게임·간식 소비 증가",
    salaryNote: "적금 제외 가용 35만 원",
    dday: 420,
    weights: { PX: 1.3, CONVENIENCE: 1.2, GAME: 1.15, DELIVERY: 1.08, TRANSIT: 1.0, CAFE: 0.95, DIGITAL: 1.0, HEALTH: 0.95 },
    quickBias: 1.2,
    tips: ["게임 결제 시 카드 혜택 확인", "정기 구독은 실적 구간 고려", "영수증 습관 들이기"],
  },
  cpl: {
    key: "cpl", label: "상병", avgSpend: 150000,
    salary: 650000, rankLabel: "상병",
    desc: "복무 중반, 여가·교통·배달 지출 증가",
    salaryNote: "적금 제외 가용 65만 원",
    dday: 270,
    weights: { PX: 1.2, CONVENIENCE: 1.1, TRANSIT: 1.18, GAME: 1.15, DELIVERY: 1.12, CAFE: 1.05, DIGITAL: 1.08, HEALTH: 1.0 },
    quickBias: 1.15,
    tips: ["교통비 실적 구간 활용", "배달 앱 연동 카드 확인", "사후정산 중간 점검"],
  },
  sgt: {
    key: "sgt", label: "병장", avgSpend: 200000,
    salary: 950000, rankLabel: "병장",
    desc: "전역 준비, 디지털·배달·교통 소비 집중",
    salaryNote: "적금 제외 가용 95만 원",
    dday: 90,
    weights: { PX: 1.05, CONVENIENCE: 1.05, TRANSIT: 1.12, GAME: 1.18, DELIVERY: 1.2, CAFE: 1.1, DIGITAL: 1.22, HEALTH: 1.0 },
    quickBias: 1.1,
    tips: ["전역 전 미신청 건 일괄 정리", "디지털 구독 혜택 극대화", "전역 후 카드 전환 준비"],
  },
  nco: {
    key: "nco", label: "부사관·장교", avgSpend: 420000,
    salary: 2800000, rankLabel: "간부",
    desc: "장기 복무, 교통·의료·디지털 전반",
    salaryNote: "간부 급여 기준",
    dday: null,
    weights: { TRANSIT: 1.15, HEALTH: 1.12, DIGITAL: 1.1, CAFE: 1.08, DELIVERY: 1.05, PX: 1.0, CONVENIENCE: 1.0, MART: 1.05 },
    quickBias: 0.95,
    tips: ["의료비 할인 적극 활용", "교통 정기권 실적 반영", "연간 혜택 한도 관리"],
  },
};

// ─── 외출 모드 ─────────────────────────────────────────────────────────────────
export const escapeModes = {
  outing90: {
    key: "outing90", label: "외출 3.5시간", description: "도보 10분 내, 빠른 결제, 회수율 우선",
    maxWalkMeters: 800, quickPayWeight: 1.22, recoveryWeight: 1.12, icon: "⏱️",
  },
  overnight: {
    key: "overnight", label: "외박", description: "이동 범위 넓게, 누적 혜택·실적 구간 우선",
    maxWalkMeters: 1400, quickPayWeight: 0.96, recoveryWeight: 1.16, icon: "🌙",
  },
  weekdayEvening: {
    key: "weekdayEvening", label: "평일 저녁", description: "교통·간편 결제·시간 절약 중심",
    maxWalkMeters: 700, quickPayWeight: 1.12, recoveryWeight: 1.08, icon: "🌆",
  },
};

// ─── 카드 프로필 ──────────────────────────────────────────────────────────────
export const benefitProfiles = [
  {
    key: "IBK",
    name: "IBK기업은행 나라사랑카드", short: "IBK",
    subtitle: "PX·편의점 특화", accent: "#4F8EF7",
    baseRate: 0.005, monthlyCap: 15000, quickPay: true, recoveryBias: 1.1,
    categoryRates: { PX: 0.10, CONVENIENCE: 0.05, TRANSIT: 0.05, HEALTH: 0.03, CAFE: 0.03, MART: 0.03 },
    highlights: ["PX 10% 할인", "편의점 5% 할인", "교통 5% 할인", "의료·약국 3%"],
    note: "복지매장·편의점 이용이 많은 병사에게 최적",
  },
  {
    key: "NH",
    name: "NH농협 나라사랑카드", short: "NH농협",
    subtitle: "교통·여가 특화", accent: "#22C55E",
    baseRate: 0.005, monthlyCap: 12000, quickPay: true, recoveryBias: 1.0,
    categoryRates: { PX: 0.08, TRANSIT: 0.10, GAME: 0.08, DELIVERY: 0.06, MART: 0.05, CONVENIENCE: 0.03 },
    highlights: ["교통 10% 할인", "PX 8% 할인", "게임·여가 8%", "배달 6%"],
    note: "외출 시 대중교통과 여가 지출이 많은 병사에게 최적",
  },
  {
    key: "HANA",
    name: "하나은행 나라사랑카드", short: "하나",
    subtitle: "디지털·배달 특화", accent: "#38BDF8",
    baseRate: 0.005, monthlyCap: 13000, quickPay: false, recoveryBias: 1.05,
    categoryRates: { PX: 0.07, DIGITAL: 0.12, DELIVERY: 0.08, CAFE: 0.06, GAME: 0.06, CONVENIENCE: 0.03 },
    highlights: ["디지털·통신 12% 할인", "배달·음식 8%", "카페 6%", "PX 7%"],
    note: "디지털 콘텐츠·배달 앱 지출이 많은 병사에게 최적",
  },
];

// ─── 가맹점 풀 ─────────────────────────────────────────────────────────────────
export const merchantPools = {
  PX: ["복지매장", "마트형 PX", "기지 생활관 PX"],
  CONVENIENCE: ["편의점", "24시 스토어", "생활마트"],
  TRANSIT: ["지하철역", "버스 환승센터", "기차역 매점"],
  GAME: ["PC방", "게임 스토어", "콘솔 매장"],
  DELIVERY: ["배달 스테이션", "테이크아웃 허브", "푸드 픽업존"],
  CAFE: ["카페", "테이크아웃 커피", "디저트 카페"],
  DIGITAL: ["전자매장", "통신 대리점", "디지털 숍"],
  HEALTH: ["약국", "헬스용품점", "클리닉 편의점"],
};

// ─── 카테고리 색상 ────────────────────────────────────────────────────────────
export const catColors = {
  PX: "#4ADE80", CONVENIENCE: "#60A5FA", TRANSIT: "#FBBF24",
  GAME: "#A78BFA", DELIVERY: "#F87171", CAFE: "#FB923C",
  DIGITAL: "#34D399", HEALTH: "#F472B6", MART: "#38BDF8",
};

// ─── 초기 거래 데이터 ──────────────────────────────────────────────────────────
export const initialTransactions = [
  { id: "t1", merchant: "복지매장 A", amount: 18200, category: "PX", profileKey: "IBK", hasReceipt: true, date: "2026-03-12" },
  { id: "t2", merchant: "버스 환승센터", amount: 1450, category: "TRANSIT", profileKey: "NH", hasReceipt: false, date: "2026-03-11" },
  { id: "t3", merchant: "게임 스토어", amount: 32000, category: "GAME", profileKey: "IBK", hasReceipt: true, date: "2026-03-10" },
  { id: "t4", merchant: "배달 스테이션", amount: 21900, category: "DELIVERY", profileKey: "HANA", hasReceipt: true, date: "2026-03-09" },
  { id: "t5", merchant: "생활마트 B", amount: 12800, category: "CONVENIENCE", profileKey: "NH", hasReceipt: false, date: "2026-03-08" },
  { id: "t6", merchant: "카페 1", amount: 5500, category: "CAFE", profileKey: "HANA", hasReceipt: true, date: "2026-03-07" },
  { id: "t7", merchant: "통신 대리점", amount: 45000, category: "DIGITAL", profileKey: "HANA", hasReceipt: true, date: "2026-03-05" },
  { id: "t8", merchant: "약국 2", amount: 8900, category: "HEALTH", profileKey: "IBK", hasReceipt: true, date: "2026-03-04" },
];
