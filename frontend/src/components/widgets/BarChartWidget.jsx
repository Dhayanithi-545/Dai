import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import {
  CHART_COLORS,
  getBarColor,
  formatChartValue,
  chartWrapperStyle,
  chartTitleStyle,
  tooltipBoxStyle,
  tooltipLabelStyle,
  tooltipRowStyle,
  tooltipMutedStyle,
  tooltipValueStyle,
} from "./chartTheme";

function BarChartWidget({ title, data, xKey = "name", yKey = "value" }) {
  const chartData = useMemo(
    () =>
      data.map((d, i) => ({
        name: d[xKey],
        value: Number(d[yKey]) || 0,
        index: i,
        color: CHART_COLORS[i % CHART_COLORS.length],
      })),
    [data, xKey, yKey]
  );

  if (!chartData.length) return null;

  const max = Math.max(...chartData.map((d) => d.value), 1);
  const total = chartData.reduce((s, d) => s + d.value, 0);

  return (
    <div style={chartWrapperStyle}>
      {title && <h4 style={chartTitleStyle}>{title}</h4>}
      <ResponsiveContainer width="100%" height={320}>
        <BarChart
          data={chartData}
          margin={{ top: 12, right: 12, left: 4, bottom: 8 }}
          barCategoryGap="18%"
        >
          <CartesianGrid
            stroke="rgba(255,255,255,0.06)"
            strokeDasharray="3 3"
            vertical={false}
          />
          <XAxis
            dataKey="name"
            tick={{ fill: "var(--text-muted)", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.1)" }}
            tickLine={false}
            interval={0}
            angle={chartData.length > 5 ? -25 : 0}
            textAnchor={chartData.length > 5 ? "end" : "middle"}
            height={chartData.length > 5 ? 56 : 32}
          />
          <YAxis
            tick={{ fill: "var(--text-muted)", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            width={48}
            tickFormatter={(v) => formatChartValue(v)}
          />
          <Tooltip
            cursor={{ fill: "rgba(0,212,255,0.06)", radius: 6 }}
            content={<BarTooltip max={max} total={total} />}
          />
          <Bar
            dataKey="value"
            radius={[8, 8, 0, 0]}
            maxBarSize={64}
            animationDuration={600}
          >
            {chartData.map((entry) => (
              <Cell
                key={entry.name}
                fill={entry.color}
                stroke={entry.color}
                strokeWidth={0}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function BarTooltip({ active, payload, max, total }) {
  if (!active || !payload?.length) return null;

  const item = payload[0].payload;
  const color = item.color || getBarColor(item.index, item.value, max);
  const shareOfMax = max > 0 ? ((item.value / max) * 100).toFixed(1) : 0;
  const shareOfTotal = total > 0 ? ((item.value / total) * 100).toFixed(1) : 0;

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
        {item.name}
      </p>
      <div style={tooltipRowStyle}>
        <span style={tooltipMutedStyle}>Value</span>
        <span style={{ ...tooltipValueStyle, color }}>{formatChartValue(item.value)}</span>
      </div>
      <div style={tooltipRowStyle}>
        <span style={tooltipMutedStyle}>Share of total</span>
        <span style={tooltipValueStyle}>{shareOfTotal}%</span>
      </div>
      <div style={tooltipRowStyle}>
        <span style={tooltipMutedStyle}>vs highest</span>
        <span style={tooltipValueStyle}>{shareOfMax}%</span>
      </div>
    </div>
  );
}

export default BarChartWidget;
