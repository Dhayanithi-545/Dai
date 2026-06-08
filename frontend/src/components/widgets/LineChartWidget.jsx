function LineChartWidget({ title, data, xKey = "name", yKey = "value" }) {
  if (!data?.length) return null;

  const values = data.map((d) => Number(d[yKey]) || 0);
  const dataMin = Math.min(...values);
  const dataMax = Math.max(...values);
  const padding = Math.max((dataMax - dataMin) * 0.1, dataMax * 0.05 || 1);
  const min = dataMin - padding;
  const max = dataMax + padding;
  const range = max - min || 1;

  const w = 720;
  const h = 280;
  const pad = 28;
  const showDots = data.length <= 24;

  const points = data.map((d, i) => {
    const val = Number(d[yKey]) || 0;
    const x = pad + (i / Math.max(data.length - 1, 1)) * (w - pad * 2);
    const y = h - pad - ((val - min) / range) * (h - pad * 2);
    return `${x},${y}`;
  }).join(" ");

  const yTicks = [0, 0.25, 0.5, 0.75, 1].map((t) => ({
    y: pad + t * (h - pad * 2),
    label: (max - t * range).toFixed(dataMax < 10 ? 1 : 0),
  }));

  return (
    <div style={styles.wrapper}>
      {title && <h4 style={styles.title}>{title}</h4>}
      <svg viewBox={`0 0 ${w} ${h}`} style={styles.svg}>
        {yTicks.map((tick) => (
          <g key={tick.y}>
            <line
              x1={pad}
              y1={tick.y}
              x2={w - pad}
              y2={tick.y}
              stroke="rgba(255,255,255,0.06)"
              strokeWidth="1"
            />
            <text
              x={pad - 6}
              y={tick.y + 4}
              textAnchor="end"
              fill="var(--text-muted)"
              fontSize="11"
            >
              {tick.label}
            </text>
          </g>
        ))}
        <polyline
          points={points}
          fill="none"
          stroke="#00D4FF"
          strokeWidth="2.5"
          strokeLinejoin="round"
        />
        {showDots && data.map((d, i) => {
          const val = Number(d[yKey]) || 0;
          const x = pad + (i / Math.max(data.length - 1, 1)) * (w - pad * 2);
          const y = h - pad - ((val - min) / range) * (h - pad * 2);
          return <circle key={i} cx={x} cy={y} r="4" fill="#00D4FF" />;
        })}
      </svg>
      <div style={styles.labels}>
        {data.filter((_, i) => i % Math.ceil(data.length / 6) === 0 || i === data.length - 1).map((d, i) => (
          <span key={i} style={styles.label}>{d[xKey]}</span>
        ))}
      </div>
    </div>
  );
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
    margin: "0 0 12px",
    fontSize: "14px",
    fontWeight: 600,
    color: "var(--text-secondary)",
  },
  svg: {
    width: "100%",
    height: "280px",
    display: "block",
  },
  labels: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "8px",
  },
  label: {
    fontSize: "11px",
    color: "var(--text-muted)",
    fontFamily: "var(--font-mono)",
  },
};

export default LineChartWidget;
