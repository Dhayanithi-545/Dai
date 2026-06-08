function KpiWidget({ title, value }) {
  return (
    <div style={styles.card}>
      <span style={styles.label}>{title}</span>
      <span style={styles.value}>{value}</span>
    </div>
  );
}

const styles = {
  card: {
    background: "var(--bg-primary)",
    border: "1px solid var(--border)",
    borderRadius: "10px",
    padding: "18px 20px",
    display: "flex",
    flexDirection: "column",
    gap: "6px",
    minWidth: "140px",
    flex: "1 1 160px",
  },
  label: {
    fontSize: "12px",
    color: "var(--text-muted)",
    fontFamily: "var(--font-mono)",
    textTransform: "uppercase",
    letterSpacing: "0.04em",
  },
  value: {
    fontSize: "26px",
    fontWeight: 700,
    color: "var(--accent)",
    fontFamily: "var(--font-display)",
  },
};

export default KpiWidget;
