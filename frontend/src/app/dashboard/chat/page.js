"use client";

import { useEffect, useMemo, useState } from "react";
import Icon from "@/components/ui/Icon";
import { getLatestChatMessages, sendChatMessage } from "@/lib/api";

function formatAssistantMessage(recommendation) {
  if (!recommendation) {
    return "Message received. Share more constraints and I can generate a full meal plan.";
  }
  const nutrition = recommendation.meal_plan?.nutrition_summary || {};
  return [
    `Recommendation: ${recommendation.decision?.recipe_title || "Suggested meal"}`,
    recommendation.decision?.rationale || "Generated based on your latest profile and pantry data.",
    `Nutrition: ${nutrition.calories || 0} kcal • ${nutrition.protein_g || 0}g protein`,
  ].join("\n");
}

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    async function load() {
      setLoadingHistory(true);
      try {
        const events = await getLatestChatMessages(30);
        if (!active) return;
        const rows = [...events].reverse().flatMap((event) => [
          {
            id: `u-${event.event_id}`,
            role: "user",
            text: event.message,
            createdAt: event.created_at,
          },
        ]);
        setMessages(rows);
      } catch (err) {
        if (!active) return;
        setError(err.message || "Failed to load chat history");
      } finally {
        if (active) setLoadingHistory(false);
      }
    }
    load();
    return () => {
      active = false;
    };
  }, []);

  const quickPrompts = useMemo(
    () => [
      "Make it vegetarian and under 500 calories",
      "I only have 15 minutes, suggest a quick meal",
      "Reduce grocery cost for the next meal plan",
    ],
    []
  );

  async function handleSend(messageText) {
    const trimmed = messageText.trim();
    if (!trimmed || sending) return;

    setError("");
    setSending(true);
    const userMsg = {
      id: `local-u-${Date.now()}`,
      role: "user",
      text: trimmed,
      createdAt: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const result = await sendChatMessage(trimmed, { autoReplan: true });
      const assistantMsg = {
        id: `a-${result.event_id}`,
        role: "assistant",
        text: formatAssistantMessage(result.recommendation),
        createdAt: new Date().toISOString(),
        recommendation: result.recommendation || null,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setError(err.message || "Failed to send message");
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="flex flex-1 flex-col h-full min-h-0 -m-6">
      <header className="flex items-center justify-between px-6 py-4 border-b border-primary/10 flex-shrink-0">
        <div>
          <h1 className="text-base font-bold">Personal Nutrition AI</h1>
          <p className="text-xs text-slate-500 flex items-center gap-1">
            <span className="size-2 bg-primary rounded-full animate-pulse" />
            Online & ready to replan
          </p>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
        {loadingHistory && (
          <p className="text-sm text-slate-500">Loading chat history...</p>
        )}

        {messages.length === 0 && !loadingHistory && (
          <div className="flex flex-col items-center justify-center py-10 text-center space-y-3 opacity-70">
            <Icon name="eco" className="text-5xl text-primary/50" />
            <p className="text-sm">Ask for a meal plan and I will replan using your latest context.</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[88%] rounded-2xl px-4 py-3 text-sm whitespace-pre-line ${
                message.role === "user"
                  ? "bg-primary text-white rounded-tr-none"
                  : "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-tl-none border border-slate-200 dark:border-slate-700"
              }`}
            >
              {message.text}
              {message.recommendation?.recommendation_id && (
                <a
                  href={`/dashboard/recipes/${message.recommendation.recommendation_id}`}
                  className="mt-2 block text-xs font-semibold text-primary underline"
                >
                  View recipe detail
                </a>
              )}
            </div>
          </div>
        ))}
      </div>

      <footer className="p-4 border-t border-primary/10 bg-white dark:bg-background-dark flex-shrink-0 space-y-3">
        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
            {error}
          </div>
        )}

        <div className="flex flex-wrap gap-2">
          {quickPrompts.map((prompt) => (
            <button
              key={prompt}
              type="button"
              onClick={() => handleSend(prompt)}
              className="text-xs px-3 py-1.5 rounded-full border border-primary/30 bg-primary/5 text-primary hover:bg-primary/10"
            >
              {prompt}
            </button>
          ))}
        </div>

        <div className="max-w-4xl mx-auto relative flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleSend(input);
              }
            }}
            placeholder="Type your message here..."
            className="w-full bg-slate-100 dark:bg-slate-800 border-none rounded-xl py-3.5 pl-4 pr-12 text-sm focus:ring-2 focus:ring-primary/50 transition-all outline-none"
            aria-label="Chat message"
          />
          <button
            type="button"
            onClick={() => handleSend(input)}
            disabled={sending}
            className="absolute right-2 top-1/2 -translate-y-1/2 size-9 bg-primary text-white rounded-lg flex items-center justify-center hover:bg-primary/90 disabled:opacity-50"
            aria-label="Send message"
          >
            <Icon name={sending ? "hourglass_top" : "send"} />
          </button>
        </div>
      </footer>
    </div>
  );
}
