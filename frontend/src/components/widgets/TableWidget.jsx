function TableWidget({ title, columns, rows }) {
  if (!rows?.length) return null;

  const cols = columns || Object.keys(rows[0]);

  return (
    <div style={styles.wrapper}>
      {title && <h4 style={styles.title}>{title}</h4>}
      <div style={styles.scroll}>
        <table style={styles.table}>
          <thead>
            <tr>
              {cols.map((col) => (
                <th key={col} style={styles.th}>
                  {col.replace(/_/g, " ")}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>
                {cols.map((col) => (
                  <td key={col} style={styles.td}>
                    {formatCell(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function formatCell(val) {
  if (val === null || val === undefined) return "—";
  if (typeof val === "object") return JSON.stringify(val);
  return String(val);
}

const styles = {
  wrapper: {
    background: "var(--bg-primary)",
    border: "1px solid var(--border)",
    borderRadius: "12px",
    padding: "20px",
    marginTop: "12px",
  },
  title: {
    margin: "0 0 8px",
    fontSize: "13px",
    fontWeight: 600,
    color: "var(--text-secondary)",
  },
  scroll: { overflowX: "auto" },
  table: {
    borderCollapse: "collapse",
    width: "100%",
    fontSize: "13px",
  },
  th: {
    padding: "10px 14px",
    background: "var(--bg-elevated)",
    borderBottom: "1px solid var(--border)",
    textAlign: "left",
    fontWeight: 600,
    color: "var(--text-muted)",
    textTransform: "capitalize",
    whiteSpace: "nowrap",
  },
  td: {
    padding: "9px 14px",
    borderBottom: "1px solid var(--border)",
    color: "var(--text-primary)",
    whiteSpace: "nowrap",
  },
};

export default TableWidget;
