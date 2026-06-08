import { useState, useMemo } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Sector,
} from "recharts";
import {
  CHART_COLORS,
  formatChartValue,
  chartWrapperStyle,
  chartTitleStyle,
  tooltipBoxStyle,
  tooltipLabelStyle,
  tooltipRowStyle,
  tooltipMutedStyle,
  tooltipValueStyle,
} from "./chartTheme";

function PieChartWidget({ title, data }) {
  const [activeIndex, setActiveIndex] = useState(null);

  const chartData = useMemo(
    () =>
      data.map((d, i) => ({
        name: d.name,
        value: Number(d.value) || 0,
        color: CHART_COLORS[i % CHART_COLORS.length],
      })),
    [data]
  );

  if (!chartData.length) return null;

  const total = chartData.reduce((s, d) => s + d.value, 0) || 1;

  return (
    <div style={chartWrapperStyle}>
      {title && <h4 style={chartTitleStyle}>{title}</h4>}
      <div style={styles.body}>
        <ResponsiveContainer width="100%" height={280} minWidth={220}>
          <PieChart>
            <Pie
              data={chartData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={52}
              outerRadius={activeIndex != null ? 98 : 92}
              paddingAngle={2}
              animationDuration={700}
              activeIndex={activeIndex}
              activeShape={renderActiveShape}
              onMouseEnter={(_, index) => setActiveIndex(index)}
              onMouseLeave={() => setActiveIndex(null)}
            >
              {chartData.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={entry.color}
                  stroke="var(--bg-primary)"
                  strokeWidth={2}
                  style={{ cursor: "pointer", outline: "none" }}
                />
              ))}
            </Pie>
            <Tooltip content={<PieTooltip total={total} />} />
          </PieChart>
        </ResponsiveContainer>

        <div style={styles.legend}>
          {chartData.map((entry, i) => {
            const color = entry.color;
            const pct = ((entry.value / total) * 100).toFixed(1);
            const isActive = activeIndex === i;

            return (
              <div
                key={entry.name}
                style={{
                  ...styles.legendItem,
                  background: isActive ? "rgba(0,212,255,0.08)" : "transparent",
                  borderColor: isActive ? color : "transparent",
                }}
                onMouseEnter={() => setActiveIndex(i)}
                onMouseLeave={() => setActiveIndex(null)}
              >
                <span style={{ ...styles.dot, background: color }} />
                <span style={styles.legendText}>{entry.name}</span>
                <span style={{ ...styles.legendPct, color }}>{pct}%</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function renderActiveShape({
  cx,
  cy,
  innerRadius,
  outerRadius,
  startAngle,
  endAngle,
  fill,
}) {
  return (
    <Sector
      cx={cx}
      cy={cy}
      innerRadius={innerRadius}
      outerRadius={outerRadius + 8}
      startAngle={startAngle}
      endAngle={endAngle}
      fill={fill}
      stroke="var(--bg-primary)"
      strokeWidth={2}
      style={{ filter: "brightness(1.15)" }}
    />
  );
}

function PieTooltip({ active, payload, total }) {
  if (!active || !payload?.length) return null;

  const item = payload[0];
  const name = item.name;
  const value = item.value;
  const color = item.payload?.color || CHART_COLORS[0];
  const pct = total > 0 ? ((value / total) * 100).toFixed(1) : 0;

  return (
    <div style={tooltipBoxStyle}>
      <p style={tooltipLabelStyle}>
        <span
          style={{
            display: "inline-block",
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: color,
            marginRight: 8,
            verticalAlign: "middle",
          }}
        />
        {name}
      </p>
      <div style={tooltipRowStyle}>
        <span style={tooltipMutedStyle}>Value</span>
        <span style={{ ...tooltipValueStyle, color }}>{formatChartValue(value)}</span>
      </div>
      <div style={tooltipRowStyle}>
        <span style={tooltipMutedStyle}>Share</span>
        <span style={tooltipValueStyle}>{pct}%</span>
      </div>
      <div style={tooltipRowStyle}>
        <span style={tooltipMutedStyle}>Total</span>
        <span style={tooltipValueStyle}>{formatChartValue(total)}</span>
      </div>
    </div>
  );
}

const styles = {
  body: {
    display: "flex",
    alignItems: "center",
    gap: "24px",
    flexWrap: "wrap",
  },
  legend: {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
    flex: "1 1 180px",
    minWidth: "160px",
  },
  legendItem: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    fontSize: "13px",
    padding: "8px 10px",
    borderRadius: "8px",
    border: "1px solid transparent",
    cursor: "pointer",
    transition: "background 0.2s, border-color 0.2s",
  },
  dot: {
    width: "10px",
    height: "10px",
    borderRadius: "50%",
    flexShrink: 0,
  },
  legendText: {
    color: "var(--text-secondary)",
    flex: 1,
  },
  legendPct: {
    fontFamily: "var(--font-mono)",
    fontWeight: 600,
    fontSize: "14px",
  },
};

export default PieChartWidget;
