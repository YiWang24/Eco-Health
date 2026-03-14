/**
 * 加载中指示器，用于按钮或区块 loading 状态
 * 使用：<LoadingSpinner className="size-5" /> 或 <LoadingSpinner />
 */
export default function LoadingSpinner({ className = "size-6" }) {
  return (
    <span
      className={`inline-block animate-spin rounded-full border-2 border-current border-t-transparent ${className}`}
      role="status"
      aria-label="Loading"
    />
  );
}
