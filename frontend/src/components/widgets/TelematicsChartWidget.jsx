import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function TelematicsChartWidget({ title, data }) {
  if (!data?.length) return null;

  const tickInterval = Math.max(Math.floor(data.length / 6), 1);

  return (
    <div style={styles.wrapper}>
      {title && <h4 style={styles.title}>{title}</h4>}
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 4 }}>
          <CartesianGrid stroke="rgba(255,255,255,0.06)" strokeDasharray="3 3" />
          <XAxis
            dataKey="time"
            tick={{ fill: "var(--text-muted)", fontSize: 10 }}
            axisLine={{ stroke: "rgba(255,255,255,0.1)" }}
            tickLine={false}
            interval={tickInterval}
          />
          <YAxis
            yAxisId="left"
            tick={{ fill: "var(--text-muted)", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            width={36}
            label={{
              value: "km/h",
              angle: -90,
              position: "insideLeft",
              fill: "var(--text-muted)",
              fontSize: 10,
            }}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            domain={[0, 100]}
            tick={{ fill: "var(--text-muted)", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            width={36}
            label={{
              value: "%",
              angle: 90,
              position: "insideRight",
              fill: "var(--text-muted)",
              fontSize: 10,
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }}
            iconType="circle"
            iconSize={8}
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="speed"
            name="Speed"
            stroke="#00D4FF"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="battery"
            name="Battery"
            stroke="#4ADE80"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;

  return (
    <div style={styles.tooltip}>
      <p style={styles.tooltipTime}>{label}</p>
      {payload.map((entry) => (
        <p key={entry.dataKey} style={{ color: entry.color, margin: "2px 0", fontSize: "12px" }}>
          {entry.name}: {entry.value}
          {entry.dataKey === "speed" ? " km/h" : entry.dataKey === "battery" ? "%" : ""}
        </p>
      ))}
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
    margin: "0 0 8px",
    fontSize: "13px",
    fontWeight: 600,
    color: "var(--text-secondary)",
  },
  tooltip: {
    background: "var(--bg-elevated)",
    border: "1px solid var(--border)",
    borderRadius: "8px",
    padding: "8px 12px",
    fontSize: "12px",
  },
  tooltipTime: {
    margin: "0 0 4px",
    fontWeight: 600,
    color: "var(--text-primary)",
    fontSize: "11px",
  },
};

export default TelematicsChartWidget;
