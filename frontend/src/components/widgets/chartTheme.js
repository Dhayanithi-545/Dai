export const CHART_COLORS = [
  "#00D4FF",
  "#7B61FF",
  "#00E5A0",
  "#FFB020",
  "#FF5C7A",
  "#5C9EFF",
  "#FF8C42",
  "#C084FC",
];

export function getBarColor(index, value, max) {
  if (max <= 0) return CHART_COLORS[index % CHART_COLORS.length];
  const ratio = value / max;
  if (ratio >= 0.85) return "#00E5A0";
  if (ratio >= 0.6) return "#00D4FF";
  if (ratio >= 0.35) return "#FFB020";
  return "#FF5C7A";
}

export function formatChartValue(value) {
  if (value == null) return "—";
  if (typeof value === "number") {
    return value >= 1000 ? value.toLocaleString() : String(value);
  }
  return String(value);
}

export const chartWrapperStyle = {
  background: "var(--bg-primary)",
  border: "1px solid var(--border)",
  borderRadius: "12px",
  padding: "20px",
  marginTop: "12px",
};

export const chartTitleStyle = {
  margin: "0 0 12px",
  fontSize: "14px",
  fontWeight: 600,
  color: "var(--text-secondary)",
};

export const tooltipBoxStyle = {
  background: "var(--bg-elevated)",
  border: "1px solid var(--border)",
  borderRadius: "10px",
  padding: "12px 14px",
  boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
  minWidth: "140px",
};

export const tooltipLabelStyle = {
  margin: "0 0 8px",
  fontSize: "12px",
  fontWeight: 600,
  color: "var(--text-primary)",
  borderBottom: "1px solid var(--border)",
  paddingBottom: "6px",
};

export const tooltipRowStyle = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: "16px",
  fontSize: "12px",
  margin: "4px 0",
};

export const tooltipMutedStyle = {
  color: "var(--text-muted)",
};

export const tooltipValueStyle = {
  color: "var(--text-primary)",
  fontFamily: "var(--font-mono)",
  fontWeight: 600,
};
