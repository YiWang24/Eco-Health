"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Icon from "@/components/ui/Icon";
import {
  confirmEmailCode,
  getCurrentUser,
  hasAuthSession,
  loginWithEmail,
  registerWithEmail,
  resendEmailCode,
} from "@/lib/api";
import { ROUTES } from "@/lib/constants";

const MODE_REGISTER = "register";
const MODE_VERIFY = "verify";
const MODE_LOGIN = "login";

function resolveMode(mode) {
  if (mode === MODE_REGISTER || mode === MODE_VERIFY || mode === MODE_LOGIN) {
    return mode;
  }
  return MODE_LOGIN;
}

export default function AuthPage() {
  const router = useRouter();
  const [mode, setMode] = useState(MODE_LOGIN);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [booting, setBooting] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const nextMode = resolveMode(params.get("mode"));
    setMode(nextMode);
  }, []);

  useEffect(() => {
    let active = true;
    async function boot() {
      if (!hasAuthSession()) {
        if (active) setBooting(false);
        return;
      }
      try {
        await getCurrentUser();
        if (!active) return;
        router.replace(ROUTES.dashboard);
      } catch {
        if (!active) return;
        setBooting(false);
      }
    }
    boot();
    return () => {
      active = false;
    };
  }, [router]);

  const title = useMemo(() => {
    if (mode === MODE_REGISTER) return "Create account";
    if (mode === MODE_VERIFY) return "Verify email";
    return "Sign in";
  }, [mode]);

  function switchMode(nextMode) {
    setMode(nextMode);
    setError("");
    setNotice("");
    router.replace(`${ROUTES.auth}?mode=${nextMode}`, { scroll: false });
  }

  async function handleRegister(event) {
    event.preventDefault();
    if (loading) return;
    setLoading(true);
    setError("");
    setNotice("");
    try {
      await registerWithEmail({ email, password });
      setNotice("Verification code sent to your email.");
      switchMode(MODE_VERIFY);
    } catch (err) {
      setError(err.message || "Failed to register account");
    } finally {
      setLoading(false);
    }
  }

  async function handleVerify(event) {
    event.preventDefault();
    if (loading) return;
    setLoading(true);
    setError("");
    setNotice("");
    try {
      await confirmEmailCode({ email, code });
      setNotice("Email verified. Please sign in.");
      switchMode(MODE_LOGIN);
    } catch (err) {
      setError(err.message || "Failed to verify email");
    } finally {
      setLoading(false);
    }
  }

  async function handleResendCode() {
    if (!email || loading) return;
    setLoading(true);
    setError("");
    setNotice("");
    try {
      await resendEmailCode({ email });
      setNotice("Verification code resent.");
    } catch (err) {
      setError(err.message || "Failed to resend code");
    } finally {
      setLoading(false);
    }
  }

  async function handleLogin(event) {
    event.preventDefault();
    if (loading) return;
    setLoading(true);
    setError("");
    setNotice("");
    try {
      await loginWithEmail({ email, password });
      await getCurrentUser();
      router.replace(ROUTES.onboarding);
    } catch (err) {
      setError(err.message || "Failed to sign in");
    } finally {
      setLoading(false);
    }
  }

  if (booting) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background-light px-4">
        <div className="text-sm text-slate-500">Checking session...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background-light flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-[460px] rounded-3xl border border-slate-200 bg-white shadow-sm p-6 md:p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="h-11 w-11 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
            <Icon name="lock" className="text-2xl" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-widest text-slate-500">AWS Cognito</p>
            <h1 className="text-2xl font-black tracking-tight">{title}</h1>
          </div>
        </div>

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        )}
        {notice && (
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm text-emerald-700">
            {notice}
          </div>
        )}

        <form
          onSubmit={
            mode === MODE_REGISTER
              ? handleRegister
              : mode === MODE_VERIFY
                ? handleVerify
                : handleLogin
          }
          className="space-y-4"
        >
          <label className="block space-y-1.5">
            <span className="text-sm font-semibold text-slate-700">Email</span>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm"
              placeholder="you@example.com"
              required
            />
          </label>

          {mode !== MODE_VERIFY && (
            <label className="block space-y-1.5">
              <span className="text-sm font-semibold text-slate-700">Password</span>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="w-full rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm"
                placeholder="At least 8 characters"
                minLength={8}
                required
              />
            </label>
          )}

          {mode === MODE_VERIFY && (
            <label className="block space-y-1.5">
              <span className="text-sm font-semibold text-slate-700">Verification code</span>
              <input
                type="text"
                value={code}
                onChange={(event) => setCode(event.target.value)}
                className="w-full rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm"
                placeholder="6-digit code"
                required
              />
            </label>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-primary text-white font-bold py-3 disabled:opacity-60"
          >
            {loading
              ? "Processing..."
              : mode === MODE_REGISTER
                ? "Create account"
                : mode === MODE_VERIFY
                  ? "Verify email"
                  : "Sign in"}
          </button>
        </form>

        {mode === MODE_VERIFY && (
          <button
            type="button"
            onClick={handleResendCode}
            disabled={loading || !email}
            className="w-full rounded-xl border border-slate-200 bg-white font-semibold py-2.5 text-sm disabled:opacity-60"
          >
            Resend code
          </button>
        )}

        <div className="text-sm text-slate-600 flex flex-wrap gap-2">
          {mode !== MODE_LOGIN && (
            <button type="button" className="text-primary font-semibold" onClick={() => switchMode(MODE_LOGIN)}>
              Back to sign in
            </button>
          )}
          {mode === MODE_LOGIN && (
            <>
              <button type="button" className="text-primary font-semibold" onClick={() => switchMode(MODE_REGISTER)}>
                Create account
              </button>
              <button type="button" className="text-primary font-semibold" onClick={() => switchMode(MODE_VERIFY)}>
                Verify email
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
