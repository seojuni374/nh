// ─── THEME ────────────────────────────────────────────────────────────────────
export const T = {
  bg: "#0A0F0C",
  surface: "#111A14",
  surfaceAlt: "#182219",
  surfaceBright: "#1E2D22",
  stroke: "#243028",
  strokeBright: "#2E3E33",
  brand: "#4ADE80",
  brandDim: "#22C55E",
  brandSoft: "#0F2016",
  text: "#E8F0EA",
  muted: "#6B8070",
  mutedBright: "#8FA89A",
  warning: "#F59E0B",
  warningSoft: "#1C1505",
  danger: "#F87171",
  dangerSoft: "#200A0A",
  success: "#4ADE80",
  amber: "#FBBF24",
  info: "#38BDF8",
  infoSoft: "#0C1929",
};

export const s = {
  panel: { background: T.surface, border: `1px solid ${T.stroke}`, borderRadius: 16, padding: 20 },
  card: { background: T.surfaceAlt, border: `1px solid ${T.stroke}`, borderRadius: 12, padding: 16 },
  input: { background: T.bg, border: `1px solid ${T.strokeBright}`, color: T.text, borderRadius: 8, padding: "8px 12px", fontSize: 13, width: "100%", outline: "none" },
  label: { fontSize: 11, fontWeight: 700, letterSpacing: "0.1em", color: T.muted, textTransform: "uppercase" },
  title: { fontSize: 18, fontWeight: 800, color: T.text, letterSpacing: "-0.02em" },
  mono: { fontFamily: '"Space Mono", monospace' },
};
