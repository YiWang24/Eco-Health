/**
 * 前端负责：在画面/视频上根据识别结果绘制颜色框并显示信息。
 * 颜色按「新鲜度」划分：绿=新鲜，橙=即将过期，红=需尽快使用，黑=不建议再食用（由后端 status 决定）。
 *
 * @param {Array<{ id: string, label: string, confidence: number, box: { left, top, width, height }, status?: 'fresh'|'expiring_soon'|'critical'|'do_not_eat' }>} detections
 *   - status: fresh=绿，expiring_soon=橙，critical=红，do_not_eat=黑
 */
export default function DetectionBoxOverlay({ detections = [] }) {
  const getBorderColor = (status) => {
    switch (status) {
      case "do_not_eat":
        return "border-slate-800 dark:border-slate-600 bg-slate-800/30 dark:bg-slate-700/30 shadow-[0_0_12px_rgba(30,41,59,0.5)]";
      case "critical":
        return "border-red-500 bg-red-500/20 shadow-[0_0_12px_rgba(239,68,68,0.5)]";
      case "expiring_soon":
        return "border-orange-400 bg-orange-400/20 shadow-[0_0_12px_rgba(251,146,60,0.5)]";
      default:
        return "border-primary bg-primary/20 shadow-[0_0_12px_rgba(76,174,79,0.4)]";
    }
  };

  const getLabelBg = (status) => {
    switch (status) {
      case "do_not_eat":
        return "bg-slate-800 dark:bg-slate-700";
      case "critical":
        return "bg-red-600";
      case "expiring_soon":
        return "bg-orange-500";
      default:
        return "bg-primary";
    }
  };

  return (
    <div className="absolute inset-0 pointer-events-none">
      {detections.map(({ id, label, confidence, box, status = "fresh" }) => (
        <div
          key={id}
          className={`absolute border-2 rounded ${getBorderColor(status)} backdrop-blur-[1px] transition-all`}
          style={{
            left: `${box.left}%`,
            top: `${box.top}%`,
            width: `${box.width}%`,
            height: `${box.height}%`,
          }}
        >
          <div
            className={`absolute -top-8 left-0 text-white px-2 py-1 rounded-t-lg text-[10px] font-bold uppercase tracking-wider whitespace-nowrap ${getLabelBg(status)}`}
          >
            {label} {confidence != null && `${Math.round(confidence)}%`}
          </div>
        </div>
      ))}
    </div>
  );
}
