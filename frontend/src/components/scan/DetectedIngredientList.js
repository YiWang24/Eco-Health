import Icon from "@/components/ui/Icon";

const STATUS_COLORS = {
  critical: { text: "text-red-600", icon: "text-red-500", badge: "bg-red-100 text-red-700" },
  expiring_soon: { text: "text-orange-600", icon: "text-orange-500", badge: "bg-orange-100 text-orange-700" },
  fresh: { text: "text-slate-500", icon: "text-primary", badge: "" },
};

function getColors(status) {
  return STATUS_COLORS[status] || STATUS_COLORS.fresh;
}

export default function DetectedIngredientList({
  items = [],
  newCount,
  deletingIds = new Set(),
  clearingAll = false,
  onDelete,
  onClearAll,
}) {
  const hasItems = items.length > 0;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-bold">Pantry</h3>
          {newCount != null && newCount > 0 && (
            <span className="bg-primary/20 text-primary text-xs font-bold px-2 py-1 rounded-full">
              +{newCount} new
            </span>
          )}
          {hasItems && (
            <span className="text-xs text-slate-400 font-medium">{items.length} items</span>
          )}
        </div>
        {hasItems && onClearAll && (
          <button
            type="button"
            onClick={onClearAll}
            disabled={clearingAll}
            className="flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-red-500 hover:bg-red-50 disabled:opacity-50 transition-colors"
          >
            {clearingAll ? (
              <span className="h-3 w-3 animate-spin rounded-full border-2 border-red-300 border-t-red-500" />
            ) : (
              <Icon name="delete_sweep" className="text-sm" />
            )}
            Clear All
          </button>
        )}
      </div>

      {!hasItems ? (
        <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 py-8 text-center text-sm text-slate-400">
          <Icon name="kitchen" className="text-3xl mb-2 block" />
          No ingredients yet — scan your fridge to populate
        </div>
      ) : (
        <ul className="space-y-2 max-h-[420px] overflow-y-auto pr-0.5">
          {items.map(({ id, name, icon, status, statusText }) => {
            const colors = getColors(status);
            const isDeleting = deletingIds.has(id);

            return (
              <li
                key={id}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white border border-slate-100 transition-opacity ${isDeleting ? "opacity-40 pointer-events-none" : ""}`}
              >
                <span className={colors.icon}>
                  <Icon name={icon || "eco"} className="text-xl" />
                </span>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-slate-900 truncate text-sm">{name}</p>
                  {statusText && (
                    <p className={`text-xs font-medium ${colors.text}`}>
                      {status !== "fresh" && "▲ "}{statusText}
                    </p>
                  )}
                </div>
                {onDelete && (
                  <button
                    type="button"
                    onClick={() => onDelete(id)}
                    disabled={isDeleting}
                    aria-label={`Remove ${name}`}
                    className="shrink-0 p-1.5 rounded-lg text-slate-300 hover:text-red-400 hover:bg-red-50 transition-colors"
                  >
                    {isDeleting ? (
                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-red-400 block" />
                    ) : (
                      <Icon name="close" className="text-base" />
                    )}
                  </button>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
