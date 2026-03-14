export default function CameraFrame({ children, imageUrl, alt = "" }) {
  return (
    <div className="relative w-full aspect-[4/5] rounded-3xl overflow-hidden bg-slate-200 dark:bg-slate-800 shadow-2xl border-4 border-white dark:border-slate-700">
      {imageUrl && (
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: `url("${imageUrl}")` }}
          aria-hidden
        />
      )}
      {children}
    </div>
  );
}
