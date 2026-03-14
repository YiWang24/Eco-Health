import Link from "next/link";

const variants = {
  primary:
    "bg-primary text-white font-bold shadow-lg shadow-primary/20 hover:opacity-90 transition-all",
  primaryLarge:
    "bg-primary text-white text-lg font-bold shadow-xl shadow-primary/30 hover:scale-[1.02] transition-all",
  outline:
    "border-2 border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-100 font-bold hover:bg-slate-50 dark:hover:bg-slate-800 transition-all",
  secondary:
    "bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-bold hover:bg-slate-200 transition-colors",
  ghost: "bg-white/10 text-white border border-white/20 hover:bg-white/20 backdrop-blur",
};

const sizes = {
  sm: "h-10 px-4 text-sm rounded-lg min-w-[84px]",
  md: "h-14 px-6 rounded-xl min-w-[160px]",
  lg: "h-14 px-8 rounded-xl text-lg min-w-[200px]",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  href,
  ...props
}) {
  const base = "inline-flex cursor-pointer items-center justify-center";
  const combined = `${base} ${variants[variant] || variants.primary} ${sizes[size] || sizes.md} ${className}`;

  if (href) {
    return (
      <Link href={href} className={combined} {...props}>
        {children}
      </Link>
    );
  }
  return (
    <button type="button" className={combined} {...props}>
      {children}
    </button>
  );
}
