/**
 * 颜色框图例：按新鲜度划分，与 DetectionBoxOverlay 一致
 */
export default function FreshnessLegend() {
  return (
    <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600 dark:text-slate-400">
      <span className="font-medium text-slate-500 dark:text-slate-500">
        Color by freshness:
      </span>
      <span className="flex items-center gap-1.5">
        <span className="size-3 rounded-sm bg-primary" aria-hidden />
        Green Fresh
      </span>
      <span className="flex items-center gap-1.5">
        <span className="size-3 rounded-sm bg-orange-500" aria-hidden />
        Orange Expiring soon
      </span>
      <span className="flex items-center gap-1.5">
        <span className="size-3 rounded-sm bg-red-500" aria-hidden />
        Red Use soon
      </span>
      <span className="flex items-center gap-1.5">
        <span className="size-3 rounded-sm bg-slate-800 dark:bg-slate-700" aria-hidden />
        Black Not recommended to eat
      </span>
    </div>
  );
}
