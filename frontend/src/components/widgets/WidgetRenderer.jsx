import KpiWidget from "./KpiWidget";
import BarChartWidget from "./BarChartWidget";
import LineChartWidget from "./LineChartWidget";
import PieChartWidget from "./PieChartWidget";
import TableWidget from "./TableWidget";
import TelematicsChartWidget from "./TelematicsChartWidget";
import TemperatureChartWidget from "./TemperatureChartWidget";

function WidgetRenderer({ widgets }) {
  if (!widgets?.length) return null;

  const kpis = widgets.filter((w) => w.type === "kpi");
  const charts = widgets.filter((w) => w.type !== "kpi");

  return (
    <div style={styles.container}>
      {kpis.length > 0 && (
        <div style={styles.kpiRow}>
          {kpis.map((w, i) => (
            <KpiWidget key={i} title={w.title} value={w.value} />
          ))}
        </div>
      )}
      {charts.map((w, i) => (
        <Widget key={i} widget={w} />
      ))}
    </div>
  );
}

function Widget({ widget }) {
  switch (widget.type) {
    case "bar_chart":
      return (
        <BarChartWidget
          title={widget.title}
          data={widget.data}
          xKey={widget.xKey}
          yKey={widget.yKey}
        />
      );
    case "line_chart":
      return (
        <LineChartWidget
          title={widget.title}
          data={widget.data}
          xKey={widget.xKey}
          yKey={widget.yKey}
        />
      );
    case "pie_chart":
      return <PieChartWidget title={widget.title} data={widget.data} />;
    case "table":
      return (
        <TableWidget
          title={widget.title}
          columns={widget.columns}
          rows={widget.rows}
        />
      );
    case "telematics_chart":
      return (
        <TelematicsChartWidget
          title={widget.title}
          data={widget.data}
        />
      );
    case "temperature_chart":
      return (
        <TemperatureChartWidget
          title={widget.title}
          data={widget.data}
        />
      );
    default:
      return null;
  }
}

const styles = {
  container: {
    marginTop: "4px",
    maxWidth: "100%",
  },
  kpiRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
    marginTop: "12px",
  },
};

export default WidgetRenderer;
