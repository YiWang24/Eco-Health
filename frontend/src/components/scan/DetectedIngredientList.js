import Icon from "@/components/ui/Icon";

/**
 * 右侧「检测到的食材」列表，前端根据后端数据渲染。
 * 每条：图标、名称、状态文案（过期/仅剩/新鲜等），用颜色区分状态。
 *
 * @param {Array<{ id: string, name: string, icon: string, status: 'fresh'|'expiring_soon'|'critical', statusText: string }>} items
 * @param {number} newCount - “X New Found” 徽章数字，可选
 */
export default function DetectedIngredientList({ items = [], newCount }) {
  const getStatusColor = (status) => {
    switch (status) {
      case "critical":
        return "text-red-600 dark:text-red-400";
      case "expiring_soon":
        return "text-orange-600 dark:text-orange-400";
      case "do_not_eat":
        return "text-slate-500 dark:text-slate-500";
      default:
        return "text-slate-600 dark:text-slate-400";
    }
  };

  const getIconColor = (status) => {
    switch (status) {
      case "critical":
        return "text-red-500";
      case "expiring_soon":
        return "text-orange-500";
      case "do_not_eat":
        return "text-slate-500 dark:text-slate-500";
      default:
        return "text-primary";
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold">Detected Ingredients</h3>
        {newCount != null && newCount > 0 && (
          <span className="bg-primary/20 text-primary text-xs font-bold px-2 py-1 rounded-full">
            {newCount} New Found
          </span>
        )}
      </div>
      <ul className="space-y-2">
        {items.map(({ id, name, icon, status, statusText }) => (
          <li
            key={id}
            className="flex items-center gap-3 p-3 rounded-xl bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700"
          >
            <span className={getIconColor(status)}>
              <Icon name={icon || "eco"} className="text-2xl" />
            </span>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-slate-900 dark:text-slate-100 truncate">
                {name}
              </p>
              <p className={`text-xs font-medium ${getStatusColor(status)}`}>
                {status && status !== "fresh" ? "▲ " : ""}
                {statusText}
              </p>
            </div>
            <button
              type="button"
              className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
              aria-label="More options"
            >
              <Icon name="more_vert" className="text-lg" />
            </button>
          </li>
        ))}
      </ul>
      <button
        type="button"
        className="w-full py-3 rounded-xl border-2 border-dashed border-slate-200 dark:border-slate-600 text-slate-500 dark:text-slate-400 text-sm font-medium hover:border-primary hover:text-primary transition-colors"
      >
        + Add Ingredient Manually
      </button>
    </div>
  );
}
