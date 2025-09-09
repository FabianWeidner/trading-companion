import { useEffect, useState } from "react";

export default function App() {
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/health")
      .then((r) =>
        r.ok ? r.json() : Promise.reject(new Error("Request failed"))
      )
      .then((d) => setStatus(d.status))
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex items-center justify-center p-6">
      <div className="max-w-md w-full space-y-4">
        <h1 className="text-8xlfont-semibold">Trading Companion</h1>
        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h2 className="text-lg font-medium mb-2">Backend Health</h2>
          {!status && !error && <p>Checking…</p>}
          {error && <p className="text-red-600">Error: {error}</p>}
          {status && (
            <p className="text-emerald-600 font-medium">Status: {status}</p>
          )}
        </div>
        <p className="text-xs text-slate-500">
          Vite + React + TS + Tailwind v4
        </p>
      </div>
    </div>
  );
}
