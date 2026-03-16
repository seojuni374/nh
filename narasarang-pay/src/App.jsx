import { useState, useMemo, useCallback } from 'react'
import './App.css'
import { personas, escapeModes, benefitProfiles, initialTransactions, catColors } from './data/constants'
import { T, s } from './data/theme'
import {
  currency, pct, getProgress, buildReport, getPaydayInfo,
  getDdaySavings, getSpendingPattern, getOptimalStrategy,
} from './engine/core'

const personaList = Object.values(personas)
const escapeModeList = Object.values(escapeModes)

function App() {
  const [personaKey, setPersonaKey] = useState('pvt')
  const [escapeModeKey, setEscapeModeKey] = useState('outing90')
  const [monthlySpend, setMonthlySpend] = useState(86350)

  const persona = personas[personaKey]
  const escapeMode = escapeModes[escapeModeKey]

  const report = useMemo(
    () => buildReport({ transactions: initialTransactions, monthlySpend }),
    [monthlySpend],
  )
  const progress = useMemo(() => getProgress(monthlySpend), [monthlySpend])
  const payday = useMemo(() => getPaydayInfo(monthlySpend), [monthlySpend])
  const dday = useMemo(() => getDdaySavings(persona, monthlySpend), [persona, monthlySpend])
  const pattern = useMemo(() => getSpendingPattern(initialTransactions), [])
  const strategies = useMemo(
    () => getOptimalStrategy(persona, monthlySpend),
    [persona, monthlySpend],
  )

  const handleSpendChange = useCallback((e) => {
    setMonthlySpend(Number(e.target.value))
  }, [])

  const tierPct = progress.next
    ? ((monthlySpend - progress.current.min) / (progress.next.min - progress.current.min)) * 100
    : 100

  return (
    <div style={{ maxWidth: 520, margin: '0 auto', padding: '24px 16px', fontFamily: '"Pretendard", system-ui, sans-serif' }}>
      {/* 헤더 */}
      <header style={{ textAlign: 'center', marginBottom: 28 }}>
        <h1 style={{ ...s.title, fontSize: 22 }}>나라사랑 Pay</h1>
        <p style={{ color: T.muted, fontSize: 13, marginTop: 4 }}>AI 혜택 최적화 · {escapeMode.label}</p>
      </header>

      {/* 퍼소나 선택 */}
      <div style={{ ...s.panel, marginBottom: 14 }}>
        <p style={s.label}>계급 선택</p>
        <div style={{ display: 'flex', gap: 6, marginTop: 8, flexWrap: 'wrap' }}>
          {personaList.map(p => (
            <button
              key={p.key}
              onClick={() => setPersonaKey(p.key)}
              style={{
                padding: '6px 14px', borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: 'pointer',
                border: p.key === personaKey ? `1.5px solid ${T.brand}` : `1px solid ${T.stroke}`,
                background: p.key === personaKey ? T.brandSoft : T.surfaceAlt,
                color: p.key === personaKey ? T.brand : T.muted,
              }}
            >
              {p.label}
            </button>
          ))}
        </div>
        <p style={{ color: T.muted, fontSize: 12, marginTop: 8 }}>{persona.desc} · 월급 {currency(persona.salary)}</p>
      </div>

      {/* 외출 모드 */}
      <div style={{ ...s.panel, marginBottom: 14 }}>
        <p style={s.label}>외출 모드</p>
        <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>
          {escapeModeList.map(m => (
            <button
              key={m.key}
              onClick={() => setEscapeModeKey(m.key)}
              style={{
                flex: 1, padding: '8px 0', borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: 'pointer',
                border: m.key === escapeModeKey ? `1.5px solid ${T.brand}` : `1px solid ${T.stroke}`,
                background: m.key === escapeModeKey ? T.brandSoft : T.surfaceAlt,
                color: m.key === escapeModeKey ? T.brand : T.muted,
              }}
            >
              {m.icon} {m.label}
            </button>
          ))}
        </div>
      </div>

      {/* 실적 구간 */}
      <div style={{ ...s.panel, marginBottom: 14 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
          <p style={s.label}>이번 달 실적</p>
          <span style={{ ...s.mono, fontSize: 18, fontWeight: 800, color: T.brand }}>{currency(monthlySpend)}</span>
        </div>
        <input
          type="range" min={0} max={300000} step={1000}
          value={monthlySpend} onChange={handleSpendChange}
          style={{ width: '100%', marginTop: 12 }}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6 }}>
          <span style={{ fontSize: 12, color: T.muted }}>{progress.current.icon} {progress.current.label} ×{progress.current.multiplier}</span>
          {progress.next && (
            <span style={{ fontSize: 12, color: T.warning }}>
              다음 {progress.next.label}까지 {currency(progress.gapToNext)}
            </span>
          )}
        </div>
        <div style={{ height: 6, borderRadius: 3, background: T.strokeBright, marginTop: 8, overflow: 'hidden' }}>
          <div style={{ height: '100%', borderRadius: 3, background: T.brand, width: `${Math.min(100, tierPct)}%`, transition: 'width 0.3s' }} />
        </div>
      </div>

      {/* 정산일 정보 */}
      <div style={{ ...s.panel, marginBottom: 14 }}>
        <p style={s.label}>정산일까지</p>
        <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
          <div>
            <span style={{ ...s.mono, fontSize: 22, fontWeight: 800, color: T.text }}>{payday.remainDays}</span>
            <span style={{ fontSize: 12, color: T.muted, marginLeft: 4 }}>일 남음</span>
          </div>
          {payday.nextTier && payday.achievable && (
            <div style={{ fontSize: 12, color: T.success, alignSelf: 'center' }}>
              하루 {currency(payday.dailyNeeded)}씩 사용하면 다음 구간 달성 가능
            </div>
          )}
        </div>
        {dday && (
          <div style={{ marginTop: 10, padding: '8px 12px', borderRadius: 8, background: T.infoSoft, fontSize: 12, color: T.info }}>
            전역까지 {dday.monthsLeft}개월 · 예상 누적 절약 {currency(dday.totalEstSavings)} · 회수 가능 {currency(dday.recoverableSavings)}
          </div>
        )}
      </div>

      {/* 카드 비교 */}
      <div style={{ ...s.panel, marginBottom: 14 }}>
        <p style={s.label}>카드별 혜택 요약</p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 10 }}>
          {benefitProfiles.map(card => {
            const optimal = report.rows.reduce((sum, r) => {
              const opt = r.options.find(o => o.profile.key === card.key)
              return sum + (opt ? opt.benefit : 0)
            }, 0)
            return (
              <div key={card.key} style={{ ...s.card, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ fontSize: 14, fontWeight: 700, color: card.accent }}>{card.short}</span>
                  <span style={{ fontSize: 11, color: T.muted, marginLeft: 6 }}>{card.subtitle}</span>
                  <div style={{ fontSize: 11, color: T.muted, marginTop: 2 }}>
                    {card.highlights.slice(0, 2).join(' · ')}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ ...s.mono, fontSize: 15, fontWeight: 700, color: T.text }}>{currency(optimal)}</div>
                  <div style={{ fontSize: 11, color: T.muted }}>최적 혜택</div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* 소비 패턴 */}
      <div style={{ ...s.panel, marginBottom: 14 }}>
        <p style={s.label}>카테고리별 소비 패턴</p>
        <div style={{ marginTop: 10 }}>
          {pattern.map(p => (
            <div key={p.category} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
              <span style={{ fontSize: 12, fontWeight: 600, color: catColors[p.category] || T.muted, width: 80 }}>{p.category}</span>
              <div style={{ flex: 1, height: 6, borderRadius: 3, background: T.strokeBright, overflow: 'hidden' }}>
                <div style={{ height: '100%', borderRadius: 3, background: catColors[p.category] || T.brand, width: `${p.ratio * 100}%` }} />
              </div>
              <span style={{ ...s.mono, fontSize: 11, color: T.muted, width: 40, textAlign: 'right' }}>{pct(p.ratio * 100)}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 최적 전략 */}
      {strategies.length > 0 && (
        <div style={{ ...s.panel, marginBottom: 14 }}>
          <p style={s.label}>AI 추천 전략</p>
          <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
            {strategies.map((st, i) => (
              <div key={i} style={{
                padding: '10px 12px', borderRadius: 8,
                background: st.priority === 'high' ? T.brandSoft : T.surfaceAlt,
                border: `1px solid ${st.priority === 'high' ? T.brandDim : T.stroke}`,
              }}>
                <div style={{ fontSize: 13, fontWeight: 700, color: st.priority === 'high' ? T.brand : T.text }}>{st.action}</div>
                <div style={{ fontSize: 11, color: T.muted, marginTop: 2 }}>{st.detail}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 최근 거래 */}
      <div style={{ ...s.panel, marginBottom: 14 }}>
        <p style={s.label}>최근 거래 분석</p>
        <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 6 }}>
          {report.rows.slice(0, 5).map(row => (
            <div key={row.id} style={{ ...s.card, display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 12px' }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: T.text }}>{row.merchant}</div>
                <div style={{ fontSize: 11, color: T.muted }}>{row.category} · {row.date}</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ ...s.mono, fontSize: 13, color: T.text }}>{currency(row.amount)}</div>
                {row.extra > 0 && (
                  <div style={{ fontSize: 11, color: T.warning }}>+{currency(row.extra)} 회수 가능</div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 요약 */}
      <div style={{
        ...s.panel, marginBottom: 24, textAlign: 'center',
        background: T.brandSoft, border: `1px solid ${T.brandDim}`,
      }}>
        <p style={{ fontSize: 12, color: T.muted }}>총 {report.rows.length}건 분석 결과</p>
        <div style={{ ...s.mono, fontSize: 20, fontWeight: 800, color: T.brand, marginTop: 4 }}>
          {currency(report.potentialExtra)}
        </div>
        <p style={{ fontSize: 12, color: T.muted, marginTop: 2 }}>추가 회수 가능 혜택</p>
        <p style={{ fontSize: 11, color: T.mutedBright, marginTop: 8 }}>
          회수율 {pct(report.recoveryRatio)} · 현재 절약 {currency(report.totalSaved)} / 최적 {currency(report.optimalBenefit)}
        </p>
      </div>

      {/* 팁 */}
      <div style={{ ...s.panel, marginBottom: 24 }}>
        <p style={s.label}>{persona.label} 맞춤 팁</p>
        <ul style={{ marginTop: 8, paddingLeft: 16 }}>
          {persona.tips.map((tip, i) => (
            <li key={i} style={{ fontSize: 12, color: T.mutedBright, marginBottom: 4 }}>{tip}</li>
          ))}
        </ul>
      </div>

      <footer style={{ textAlign: 'center', padding: '16px 0', fontSize: 11, color: T.muted }}>
        나라사랑 Pay &copy; 2026 · 군 장병 카드 혜택 AI 최적화
      </footer>
    </div>
  )
}

export default App
