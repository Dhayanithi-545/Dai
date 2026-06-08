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

function TemperatureChartWidget({ title, data }) {
  if (!data?.length) return null;

  const tickInterval = Math.max(Math.floor(data.length / 6), 1);

  const temps = data.flatMap((d) => [d.motor_temp, d.battery_temp]);
  const dataMin = Math.min(...temps);
  const dataMax = Math.max(...temps);
  const padding = Math.max((dataMax - dataMin) * 0.1, 2);
  const yMin = Math.floor(dataMin - padding);
  const yMax = Math.ceil(dataMax + padding);

  return (
    <div style={styles.wrapper}>
      {title && <h4 style={styles.title}>{title}</h4>}
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 12, right: 16, left: 4, bottom: 4 }}>
          <CartesianGrid stroke="rgba(255,255,255,0.06)" strokeDasharray="3 3" />
          <XAxis
            dataKey="time"
            tick={{ fill: "var(--text-muted)", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.1)" }}
            tickLine={false}
            interval={tickInterval}
          />
          <YAxis
            domain={[yMin, yMax]}
            tick={{ fill: "var(--text-muted)", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            width={40}
            tickFormatter={(v) => `${v}°`}
            label={{
              value: "°C",
              angle: -90,
              position: "insideLeft",
              fill: "var(--text-muted)",
              fontSize: 11,
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: "12px", paddingTop: "10px" }}
            iconType="circle"
            iconSize={8}
          />
          <Line
            type="monotone"
            dataKey="motor_temp"
            name="Motor"
            stroke="#FF8C42"
            strokeWidth={2.5}
            dot={false}
            activeDot={{ r: 5 }}
          />
          <Line
            type="monotone"
            dataKey="battery_temp"
            name="Battery"
            stroke="#7B61FF"
            strokeWidth={2.5}
            dot={false}
            activeDot={{ r: 5 }}
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
        <p key={entry.dataKey} style={{ color: entry.color, margin: "2px 0", fontSize: "13px" }}>
          {entry.name}: {entry.value}°C
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
    margin: "0 0 12px",
    fontSize: "14px",
    fontWeight: 600,
    color: "var(--text-secondary)",
  },
  tooltip: {
    background: "var(--bg-elevated)",
    border: "1px solid var(--border)",
    borderRadius: "8px",
    padding: "10px 14px",
    fontSize: "13px",
  },
  tooltipTime: {
    margin: "0 0 6px",
    fontWeight: 600,
    color: "var(--text-primary)",
    fontSize: "12px",
  },
};

export default TemperatureChartWidget;
