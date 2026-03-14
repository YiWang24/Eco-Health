import Icon from "@/components/ui/Icon";

/**
 * 空状态占位：无数据时显示一句文案 + 可选引导操作
 * @param {string} icon - Material icon 名称
 * @param {string} title - 主文案
 * @param {string} [description] - 副文案
 * @param {React.ReactNode} [action] - 可选按钮或链接
 */
export default function EmptyState({
  icon = "inbox",
  title = "No data yet",
  description,
  action,
}) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 rounded-2xl border-2 border-dashed border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/30 text-center">
      <Icon
        name={icon}
        className="text-4xl text-slate-300 dark:text-slate-600 mb-3"
      />
      <p className="text-slate-700 dark:text-slate-300 font-medium">{title}</p>
      {description && (
        <p className="text-sm text-slate-500 dark:text-slate-500 mt-1 max-w-sm">
          {description}
        </p>
      )}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
