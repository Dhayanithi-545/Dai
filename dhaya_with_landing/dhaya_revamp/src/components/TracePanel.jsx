import { useEffect, useRef, useState } from "react";
import {
  Activity,
  CheckCircle2,
  XCircle,
  Loader2,
  Circle,
} from "lucide-react";

// Animated SVG connector between steps
function Connector({ visible }) {
  return (
    <div style={styles.connectorWrapper}>
      <svg width="2" height="60" viewBox="0 0 2 60" style={{ display: "block" }}>
        <line
          x1="1"
          y1="0"
          x2="1"
          y2="60"
          stroke="#00D4FF"
          strokeWidth="1.5"
          strokeDasharray="60"
          strokeDashoffset={visible ? "0" : "60"}
          style={{
            transition: visible ? "stroke-dashoffset 0.4s ease" : "none",
          }}
        />
      </svg>
      {visible && (
        <svg
          width="10"
          height="6"
          viewBox="0 0 10 6"
          style={{ display: "block", margin: "0 auto" }}
        >
          <path
            d="M0 0 L5 6 L10 0"
            fill="none"
            stroke="#00D4FF"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      )}
    </div>
  );
}

const STATE_META = {
  pending: {
    color: "var(--text-muted)",
    borderColor: "var(--border)",
    icon: <Circle size={13} />,
  },
  running: {
    color: "var(--accent)",
    borderColor: "var(--accent)",
    icon: (
      <Loader2
        size={13}
        style={{ animation: "spin 1s linear infinite" }}
      />
    ),
  },
  completed: {
    color: "var(--success)",
    borderColor: "var(--success)",
    icon: (
      <CheckCircle2
        size={13}
        style={{ animation: "scaleIn 0.35s cubic-bezier(0.34,1.56,0.64,1) both" }}
      />
    ),
  },
  error: {
    color: "var(--error)",
    borderColor: "var(--error)",
    icon: <XCircle size={13} />,
  },
};

function TraceStepCard({ item, index, visible, isLast }) {
  const state = item.status || "completed";
  const meta = STATE_META[state] || STATE_META.completed;

  return (
    <div
      style={{
        ...styles.stepCard,
        borderLeftColor: meta.borderColor,
        opacity: visible ? 1 : 0,
        transform: visible ? "translateX(0)" : "translateX(24px)",
        transition: visible
          ? `opacity 0.32s ease ${index * 0.08}s, transform 0.32s ease ${index * 0.08}s`
          : "none",
      }}
    >
      <div style={styles.stepTop}>
        <span style={{ ...styles.stepIcon, color: meta.color }}>
          {meta.icon}
        </span>
        <span style={styles.stepName}>{item.step || `Step ${index + 1}`}</span>
        {item.duration && (
          <span style={styles.durationBadge}>{item.duration}</span>
        )}
      </div>

      {item.details && (
        <p style={styles.stepDetails}>{item.details}</p>
      )}

      {item.tool && (
        <span style={styles.toolBadge}>{item.tool}</span>
      )}

      {item.timestamp && (
        <span style={styles.stepTimestamp}>{item.timestamp}</span>
      )}
    </div>
  );
}

function TracePanel({ trace }) {
  const [visibleCount, setVisibleCount] = useState(0);
  const prevTraceRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    // If trace changed (new response arrived), reset and re-animate
    if (trace.length > 0 && trace !== prevTraceRef.current) {
      setVisibleCount(0);
      prevTraceRef.current = trace;

      // Clear any existing timer
      if (timerRef.current) clearInterval(timerRef.current);

      let count = 0;
      timerRef.current = setInterval(() => {
        count += 1;
        setVisibleCount(count);
        if (count >= trace.length) {
          clearInterval(timerRef.current);
        }
      }, 400);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [trace]);

  return (
    <aside style={styles.panel}>
      {/* Header */}
      <div style={styles.panelHeader}>
        <div style={styles.headerLeft}>
          <Activity size={15} color="#00D4FF" />
          <span style={styles.headerTitle}>MCP Trace</span>
        </div>
        <div style={styles.liveBadge}>
          <span style={styles.liveDot} />
          <span style={styles.liveText}>Live</span>
        </div>
      </div>

      {/* Trace list */}
      <div style={styles.traceList}>
        {trace.length === 0 ? (
          <div style={styles.emptyTrace}>
            <p style={styles.emptyTraceText}>Awaiting trace data...</p>
          </div>
        ) : (
          trace.map((item, index) => {
            const visible = index < visibleCount;
            const isLast = index === trace.length - 1;
            return (
              <div key={index} style={styles.stepWithConnector}>
                <TraceStepCard
                  item={item}
                  index={index}
                  visible={visible}
                  isLast={isLast}
                />
                {!isLast && <Connector visible={visible} />}
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
}

const styles = {
  panel: {
    width: "25%",
    height: "100vh",
    background: "var(--bg-secondary)",
    borderLeft: "1px solid var(--border)",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
  },
  panelHeader: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 18px",
    height: "58px",
    borderBottom: "1px solid var(--border)",
    flexShrink: 0,
  },
  headerLeft: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },
  headerTitle: {
    fontFamily: "var(--font-display)",
    fontWeight: 600,
    fontSize: "13px",
    color: "var(--text-primary)",
    letterSpacing: "0.04em",
  },
  liveBadge: {
    display: "flex",
    alignItems: "center",
    gap: "5px",
    background: "rgba(34,197,94,0.08)",
    border: "1px solid rgba(34,197,94,0.25)",
    borderRadius: "20px",
    padding: "2px 9px",
  },
  liveDot: {
    width: "6px",
    height: "6px",
    borderRadius: "50%",
    background: "var(--success)",
    animation: "livePulse 1.8s infinite",
  },
  liveText: {
    fontSize: "10px",
    color: "var(--success)",
    fontFamily: "var(--font-mono)",
    fontWeight: 500,
  },
  traceList: {
    flex: 1,
    overflowY: "auto",
    padding: "18px 14px 24px",
  },
  stepWithConnector: {
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
  },
  stepCard: {
    background: "var(--bg-elevated)",
    borderLeft: "3px solid",
    borderRadius: "10px",
    padding: "11px 13px",
    display: "flex",
    flexDirection: "column",
    gap: "5px",
  },
  stepTop: {
    display: "flex",
    alignItems: "center",
    gap: "7px",
  },
  stepIcon: {
    flexShrink: 0,
    display: "flex",
    alignItems: "center",
  },
  stepName: {
    fontFamily: "var(--font-display)",
    fontSize: "12px",
    fontWeight: 600,
    color: "var(--text-primary)",
    flex: 1,
    lineHeight: 1.3,
  },
  durationBadge: {
    fontFamily: "var(--font-mono)",
    fontSize: "10px",
    color: "var(--text-muted)",
    background: "var(--bg-primary)",
    border: "1px solid var(--border)",
    borderRadius: "4px",
    padding: "1px 5px",
    flexShrink: 0,
  },
  stepDetails: {
    fontSize: "12px",
    color: "var(--text-secondary)",
    lineHeight: 1.55,
    paddingLeft: "20px",
  },
  toolBadge: {
    fontFamily: "var(--font-mono)",
    fontSize: "10.5px",
    color: "var(--accent)",
    background: "var(--accent-muted)",
    borderRadius: "4px",
    padding: "2px 7px",
    display: "inline-block",
    alignSelf: "flex-start",
    marginTop: "2px",
  },
  stepTimestamp: {
    fontFamily: "var(--font-mono)",
    fontSize: "10px",
    color: "var(--text-muted)",
    paddingLeft: "20px",
    marginTop: "2px",
  },
  connectorWrapper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "2px 0",
  },
  emptyTrace: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "120px",
  },
  emptyTraceText: {
    fontSize: "12px",
    color: "var(--text-muted)",
    fontFamily: "var(--font-mono)",
  },
};

export default TracePanel;
