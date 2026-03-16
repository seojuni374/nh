import { thresholds, benefitProfiles, merchantPools } from "../data/constants";

// ─── UTILS ────────────────────────────────────────────────────────────────────
export function clamp(v, mn, mx) { return Math.min(mx, Math.max(mn, v)); }
export function currency(v) { return `₩ ${Math.round(v).toLocaleString()}`; }
export function signedCurrency(v) {
  const abs = Math.abs(Math.round(v));
  return `${v >= 0 ? "+" : "-"}₩ ${abs.toLocaleString()}`;
}
export function pct(v) { return `${v.toFixed(1)}%`; }

// ─── TIER ─────────────────────────────────────────────────────────────────────
export function getTier(spend) {
  return [...thresholds].reverse().find(t => spend >= t.min) || thresholds[0];
}
export function getNextTier(spend) {
  return thresholds.find(t => t.min > spend) || null;
}
export function getProgress(spend) {
  const current = getTier(spend);
  const next = getNextTier(spend);
  return { current, next, projected: spend, gapToNext: next ? Math.max(0, next.min - spend) : 0 };
}
export function getTierIndex(spend) {
  const tier = getTier(spend);
  return thresholds.findIndex(t => t.key === tier.key);
}

// ─── BENEFIT ──────────────────────────────────────────────────────────────────
export function benefitForTx({ amount, category, profileKey, monthlySpend }) {
  const profile = benefitProfiles.find(p => p.key === profileKey) || benefitProfiles[0];
  const tier = getTier(monthlySpend + amount);
  const rate = (profile.categoryRates[category] || profile.baseRate) * tier.multiplier;
  return Math.min(Math.floor(amount * rate), profile.monthlyCap);
}

// ─── GEO ──────────────────────────────────────────────────────────────────────
export function pseudo(a, b, i) {
  const x = Math.abs(Math.sin(a * 103 + i * 17) * Math.cos(b * 97 - i * 13));
  return x - Math.floor(x);
}
export function dist(c, m) {
  const R = 6371000, dLat = ((m.lat - c.lat) * Math.PI) / 180, dLng = ((m.lng - c.lng) * Math.PI) / 180;
  const lat1 = (c.lat * Math.PI) / 180, lat2 = (m.lat * Math.PI) / 180;
  const x = Math.sin(dLat / 2) ** 2 + Math.sin(dLng / 2) ** 2 * Math.cos(lat1) * Math.cos(lat2);
  return R * 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x));
}
export function buildMerchants(center) {
  const cats = Object.keys(merchantPools);
  return Array.from({ length: 12 }, (_, i) => {
    const cat = cats[Math.floor(pseudo(center.lat, center.lng, i) * cats.length)];
    const names = merchantPools[cat];
    const name = names[Math.floor(pseudo(center.lat, center.lng, i + 1) * names.length)];
    return {
      id: `${cat}-${i}`, name: `${name} ${i + 1}`, category: cat,
      lat: center.lat + (pseudo(center.lat, center.lng, i + 3) - 0.5) * 0.004,
      lng: center.lng + (pseudo(center.lat, center.lng, i + 2) - 0.5) * 0.004,
      quickPay: pseudo(center.lat, center.lng, i + 4) > 0.35,
      crowdIndex: Math.round(pseudo(center.lat, center.lng, i + 5) * 100),
      avgCheckoutMinutes: 1 + Math.round(pseudo(center.lat, center.lng, i + 6) * 7),
    };
  });
}

// ─── RANK PROFILES ────────────────────────────────────────────────────────────
export function rankProfiles({ merchant, amount, monthlySpend, personaKey, escapeModeKey, center, personas, escapeModes }) {
  const persona = personas[personaKey] || personas.pvt;
  const mode = escapeModes[escapeModeKey] || escapeModes.outing90;
  const distance = dist(center, merchant);
  const walkFit = distance <= mode.maxWalkMeters ? 1.08 : distance <= mode.maxWalkMeters * 1.7 ? 1 : 0.92;
  return benefitProfiles.map(profile => {
    const benefit = benefitForTx({ amount, category: merchant.category, profileKey: profile.key, monthlySpend });
    const tierNow = getTier(monthlySpend), tierAfter = getTier(monthlySpend + amount);
    const thresholdLift = tierAfter.min > tierNow.min ? 1.18 : 1;
    const personaWeight = persona.weights[merchant.category] || 1;
    const quickWeight = merchant.quickPay && profile.quickPay ? mode.quickPayWeight * persona.quickBias : 1;
    const recoverySeed = Math.min(1, benefit / Math.max(1, amount)) * 100;
    const recoveryPriority = (1 + recoverySeed / 100) * mode.recoveryWeight * profile.recoveryBias;
    // 시간 가중치: 외출 시간이 짧을수록 빠른 결제 중요도 증가
    const timeWeight = mode.key === "outing90" ? 1.15 : mode.key === "weekdayEvening" ? 1.08 : 1.0;
    const score = benefit * personaWeight * walkFit * quickWeight * thresholdLift * recoveryPriority * timeWeight;
    const confScore = clamp(
      50 + (merchant.category ? 10 : 0) + 15 + (merchant.quickPay ? 10 : 0) +
      (distance <= 500 ? 10 : 0) + (profile.quickPay ? 5 : 0) +
      (tierAfter.min > tierNow.min ? 8 : 0), 40, 99
    );
    const reasons = [
      `${merchant.category} 카테고리에 ${Math.round((profile.categoryRates[merchant.category] || profile.baseRate) * 100)}% 기준 혜택이 적용됩니다.`,
      distance <= mode.maxWalkMeters ? `${mode.label} 기준 도보 ${Math.round(distance)}m로 접근 가능합니다.` : `거리 ${Math.round(distance)}m — 이동 시간 여유 확인 필요.`,
      tierAfter.min > tierNow.min ? `이번 결제로 ${tierAfter.label} 구간이 열립니다!` : `현재 ${tierAfter.label} 유지 중입니다.`,
      profile.quickPay ? "빠른 결제 프로필로 외출 중 체류 시간을 줄이는 데 적합합니다." : "빠른 결제 미지원 프로필입니다.",
    ];
    return {
      profile, benefit, score, distance,
      recoveryRate: clamp((benefit / Math.max(amount, 1)) * 100, 0, 100),
      tierAfter, confScore, reasons,
    };
  }).sort((a, b) => b.score - a.score);
}

// ─── REPORT ENGINE ────────────────────────────────────────────────────────────
export function evalTx(tx, monthlySpend) {
  const currentBenefit = benefitForTx({ amount: tx.amount, category: tx.category, profileKey: tx.profileKey, monthlySpend });
  const options = benefitProfiles.map(profile => ({
    profile,
    benefit: benefitForTx({ amount: tx.amount, category: tx.category, profileKey: profile.key, monthlySpend }),
  })).sort((a, b) => b.benefit - a.benefit);
  const best = options[0];
  const extra = Math.max(0, (best?.benefit || 0) - currentBenefit);
  return { ...tx, currentBenefit, options, best, extra, recoveryRate: clamp((extra / Math.max(tx.amount, 1)) * 100, 0, 100) };
}

export function buildReport({ transactions, monthlySpend }) {
  const rows = transactions.map(tx => evalTx(tx, monthlySpend));
  const totalSpend = rows.reduce((s, r) => s + r.amount, 0);
  const totalSaved = rows.reduce((s, r) => s + r.currentBenefit, 0);
  const potentialExtra = rows.reduce((s, r) => s + r.extra, 0);
  const optimalBenefit = rows.reduce((s, r) => s + (r.best?.benefit || r.currentBenefit), 0);
  const recoveryRatio = optimalBenefit === 0 ? 0 : (totalSaved / optimalBenefit) * 100;
  // 카테고리별 집계
  const byCategory = {};
  rows.forEach(r => {
    if (!byCategory[r.category]) byCategory[r.category] = { spend: 0, benefit: 0, count: 0 };
    byCategory[r.category].spend += r.amount;
    byCategory[r.category].benefit += r.currentBenefit;
    byCategory[r.category].count++;
  });
  return {
    rows: [...rows].sort((a, b) => b.recoveryRate - a.recoveryRate || b.extra - a.extra),
    totalSpend, totalSaved, potentialExtra, optimalBenefit, recoveryRatio, byCategory,
  };
}

// ─── PAYDAY & D-DAY ──────────────────────────────────────────────────────────
export function getPaydayInfo(monthlySpend) {
  const now = new Date();
  const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  const remainDays = lastDay - now.getDate();
  const nextTier = getNextTier(monthlySpend);
  const gapToNext = nextTier ? Math.max(0, nextTier.min - monthlySpend) : 0;
  const dailyNeeded = remainDays > 0 && nextTier ? Math.ceil(gapToNext / remainDays) : 0;
  return { remainDays, lastDay, gapToNext, dailyNeeded, nextTier, achievable: remainDays > 0 && dailyNeeded <= 15000 };
}

export function getDdaySavings(persona, monthlySpend) {
  if (persona.dday == null) return null;
  const monthsLeft = Math.max(1, Math.round(persona.dday / 30));
  const currentTier = getTier(monthlySpend);
  const avgBenefitPerMonth = Math.round(persona.avgSpend * (currentTier.multiplier * 0.06));
  const totalEstSavings = avgBenefitPerMonth * monthsLeft;
  const missedRate = 0.37;
  const recoverableSavings = Math.round(totalEstSavings * missedRate);
  return { monthsLeft, avgBenefitPerMonth, totalEstSavings, recoverableSavings };
}

// ─── ANALYTICS (공모전 차별화) ────────────────────────────────────────────────
export function getSpendingPattern(transactions) {
  const cats = {};
  transactions.forEach(tx => {
    cats[tx.category] = (cats[tx.category] || 0) + tx.amount;
  });
  const total = Object.values(cats).reduce((a, b) => a + b, 0) || 1;
  return Object.entries(cats).map(([cat, amount]) => ({
    category: cat, amount, ratio: amount / total,
  })).sort((a, b) => b.amount - a.amount);
}

export function getWeeklyTrend(transactions) {
  const weeks = [0, 0, 0, 0];
  transactions.forEach(tx => {
    if (tx.date) {
      const d = new Date(tx.date);
      const week = Math.min(3, Math.floor(d.getDate() / 8));
      weeks[week] += tx.amount;
    }
  });
  return weeks.map((v, i) => ({ week: `${i + 1}주차`, amount: v }));
}

export function getOptimalStrategy(persona, monthlySpend) {
  const tier = getTier(monthlySpend);
  const next = getNextTier(monthlySpend);
  const strategies = [];
  if (next && next.min - monthlySpend < persona.avgSpend * 0.5) {
    strategies.push({ priority: "high", action: `${next.label} 돌파 집중`, detail: `${currency(next.min - monthlySpend)} 추가 사용 시 배율 ×${next.multiplier} 적용` });
  }
  const topCats = Object.entries(persona.weights).sort(([, a], [, b]) => b - a).slice(0, 3);
  topCats.forEach(([cat, w]) => {
    strategies.push({ priority: w > 1.15 ? "high" : "medium", action: `${cat} 카테고리 집중`, detail: `가중치 ×${w} — 이 카테고리에서 가장 높은 혜택` });
  });
  return strategies;
}

// ─── LOG ──────────────────────────────────────────────────────────────────────
export function mkLog(entry) {
  const now = new Date();
  const stamp = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
  return { id: `${stamp}-${Math.random().toString(36).slice(2, 7)}`, stamp, ...entry };
}
