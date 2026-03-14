import Icon from "@/components/ui/Icon";

export const metadata = {
  title: "Chat - Agentic Dietitian",
};

export default function ChatPage() {
  return (
    <div className="flex flex-1 flex-col h-full min-h-0 -m-6">
      <header className="flex items-center justify-between px-6 py-4 border-b border-primary/10 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div>
            <h1 className="text-base font-bold">Personal Nutrition AI</h1>
            <p className="text-xs text-slate-500 flex items-center gap-1">
              <span className="size-2 bg-primary rounded-full animate-pulse" />
              Online & Ready to assist
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button
            type="button"
            className="p-2 hover:bg-primary/10 rounded-full transition-colors"
            aria-label="Calendar"
          >
            <Icon name="calendar_month" className="text-slate-600 dark:text-slate-400" />
          </button>
          <div
            className="size-10 rounded-full bg-slate-200 border-2 border-primary/20 bg-cover bg-center"
            style={{
              backgroundImage:
                "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCASRfUbUeXnE2RDAwctYK5P47DLUuedRXlwOY5Xt9Vg1xOHGcZ_nfzdHEfkeVdDZ6zvVJ06RiT81PuBEXksBkp8ra0gzOzM1oAiMDwEJsZ1S1oVsre6eCYy_79J59syI3cCPJv-2axt4327L8NBECoDbV7ibEE2z9xeEKamQQmXgOgVGF4Mh1OlVIR_Ny-jXQphohwQMMVXvpwT-WtIuH5QKXje_6RNW4BmSyTdR_hY_JV3hc9y5MfuhB-5_MIndlTJFA8jXnsZnnK')",
            }}
            aria-hidden
          />
        </div>
      </header>
      <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
        <div className="flex flex-col items-center justify-center py-10 text-center space-y-4 opacity-50">
          <Icon name="eco" className="text-6xl text-primary/30" />
          <p className="text-sm">Today is a great day to eat healthy. How can I help?</p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <div className="flex items-end gap-3 max-w-[80%] md:max-w-[60%]">
            <div className="flex flex-col gap-1 items-end">
              <span className="text-[11px] font-medium text-slate-400 mr-1">
                You • 18:02
              </span>
              <div className="bg-primary text-white px-5 py-3 rounded-2xl rounded-tr-none shadow-sm">
                <p className="text-sm md:text-base">What should I cook tonight?</p>
              </div>
            </div>
            <div
              className="size-8 rounded-full bg-slate-200 shrink-0 bg-cover bg-center"
              style={{
                backgroundImage:
                  "url('https://lh3.googleusercontent.com/aida-public/AB6AXuC-R2aVQZuMaEddKV6EZHx1d4LoamnNsAZp4G7GvU-F8bHqEmJL4UkRPdSHEQVo7_7azev964hudF8nO3nAmYKmkzsIvzqTBp0osCsQR4GsXSyzusyDMXQTFBAHv27nQ_HX_B0gmTeuswOgF5PrQwci3Ir-Hbc5G8P_ht-St_wKJY3kdYHk3ofVQmwAZ2g2r1zIpvD6bxj7vMOp2gnLLiFav0Oke414_C8EokLUftP-DdRU-m2LPv08hkjJTfEDlHZu3xLykC-07G56')",
              }}
              aria-hidden
            />
          </div>
        </div>
        <div className="flex flex-col items-start gap-2">
          <div className="flex items-start gap-3 max-w-[85%] md:max-w-[70%]">
            <div className="size-8 rounded-full bg-primary flex items-center justify-center shrink-0">
              <Icon name="smart_toy" className="text-white text-sm" />
            </div>
            <div className="flex flex-col gap-1 items-start">
              <span className="text-[11px] font-medium text-slate-400 ml-1">
                Agentic Dietitian • 18:02
              </span>
              <div className="bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-100 px-5 py-3 rounded-2xl rounded-tl-none shadow-sm border border-slate-200 dark:border-slate-700">
                <p className="text-sm md:text-base leading-relaxed">
                  Based on your fridge contents and nutrition profile, a{" "}
                  <strong className="text-primary font-semibold">
                    mushroom spinach omelette
                  </strong>{" "}
                  fits your goals perfectly. It&apos;s high in protein, low in
                  carbs, and uses the spinach you bought yesterday!
                </p>
                <div className="mt-4 p-3 bg-white dark:bg-slate-900 rounded-lg border border-primary/20 flex gap-4 items-center">
                  <div
                    className="size-16 rounded bg-cover bg-center"
                    style={{
                      backgroundImage:
                        "url('https://lh3.googleusercontent.com/aida-public/AB6AXuD7dU90_-1ojqbyJ8TR8vAPBKoKwMAVMOS48jgZWs0c2NHjjMxWdDCpkQ2c-qevQXUsIw3nI8Tw3VskcevvkHw0zPgqDRykC2QNsp-AxENfTy2mbFs8UXQRGUj5RzIeO-A5f5BPQwN_SKqzK3mG2jtXbRYN9mql_diVwM4zAbmmXSX-ytuXX81XVv0VoxrWZA6lKyS0hNgvNzzaS6AoN-XKLc0bP7e_E8wt3VnF83jWF4iUlPMYX5eBcy3pnPCJi7I8T8KyBQjgcUkv')",
                    }}
                    aria-hidden
                  />
                  <div>
                    <h4 className="text-sm font-bold">
                      Mushroom Spinach Omelette
                    </h4>
                    <div className="flex gap-3 mt-1">
                      <span className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full uppercase font-bold">
                        High Protein
                      </span>
                      <span className="text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-500 px-2 py-0.5 rounded-full uppercase font-bold">
                        15 mins
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex flex-wrap gap-2 pt-2">
                <button
                  type="button"
                  className="flex items-center gap-2 px-4 py-2 rounded-full border border-primary/30 bg-primary/5 hover:bg-primary/10 text-primary text-sm font-medium transition-all"
                >
                  <Icon name="filter_list" className="text-sm" />
                  Make it vegetarian
                </button>
                <button
                  type="button"
                  className="flex items-center gap-2 px-4 py-2 rounded-full border border-primary/30 bg-primary/5 hover:bg-primary/10 text-primary text-sm font-medium transition-all"
                >
                  <Icon name="timer" className="text-sm" />
                  15 min only
                </button>
                <button
                  type="button"
                  className="flex items-center gap-2 px-4 py-2 rounded-full border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 hover:bg-slate-100 text-slate-600 dark:text-slate-400 text-sm font-medium transition-all"
                >
                  <Icon name="menu_book" className="text-sm" />
                  Full recipe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <footer className="p-4 md:p-6 border-t border-primary/10 bg-white dark:bg-background-dark flex-shrink-0">
        <div className="max-w-4xl mx-auto relative flex items-center gap-2">
          <button
            type="button"
            className="p-2 text-slate-400 hover:text-primary transition-colors"
            aria-label="Add attachment"
          >
            <Icon name="add_circle" />
          </button>
          <div className="relative flex-1">
            <input
              type="text"
              placeholder="Type your message here..."
              className="w-full bg-slate-100 dark:bg-slate-800 border-none rounded-xl py-4 pl-4 pr-12 text-sm focus:ring-2 focus:ring-primary/50 transition-all outline-none"
              aria-label="Chat message"
            />
            <button
              type="button"
              className="absolute right-2 top-1/2 -translate-y-1/2 size-10 bg-primary text-white rounded-lg flex items-center justify-center hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20"
              aria-label="Send message"
            >
              <Icon name="send" />
            </button>
          </div>
          <button
            type="button"
            className="p-2 text-slate-400 hover:text-primary transition-colors"
            aria-label="Voice input"
          >
            <Icon name="mic" />
          </button>
        </div>
        <p className="text-center text-[10px] text-slate-400 mt-3 uppercase tracking-widest font-semibold">
          AI can make mistakes. Verify important nutritional info.
        </p>
      </footer>
    </div>
  );
}
