import { Lightbulb } from "lucide-react";

function InsightsPanel({ insights }) {
  if (!insights?.length) return null;

  return (
    <div style={styles.panel}>
      <div style={styles.header}>
        <Lightbulb size={14} color="#FFB020" />
        <span style={styles.headerText}>Key Insights</span>
      </div>
      <ul style={styles.list}>
        {insights.map((insight, i) => (
          <li key={i} style={styles.item}>{insight}</li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  panel: {
    background: "rgba(255,176,32,0.06)",
    border: "1px solid rgba(255,176,32,0.2)",
    borderRadius: "10px",
    padding: "12px 16px",
    marginTop: "12px",
  },
  header: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
    marginBottom: "8px",
  },
  headerText: {
    fontSize: "12px",
    fontWeight: 600,
    color: "#FFB020",
    fontFamily: "var(--font-mono)",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  },
  list: {
    margin: 0,
    paddingLeft: "18px",
  },
  item: {
    fontSize: "13px",
    color: "var(--text-secondary)",
    lineHeight: 1.6,
    marginBottom: "4px",
  },
};

export default InsightsPanel;
