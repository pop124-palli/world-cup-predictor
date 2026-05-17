import { useState } from "react";

export default function Simulate() {
  const [runs, setRuns] = useState(1000);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function simulate() {
    setLoading(true);
    setError("");
    setResults([]);
    try {
      const r = await fetch(`/api/simulate?n=${runs}`);
      if (!r.ok) throw new Error("Simulation failed.");
      const d = await r.json();
      setResults(d);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const max = results.length ? results[0].probability : 1;

  return (
    <div className="space-y-10">
      <div className="space-y-2">
        <p className="text-xs tracking-widest uppercase text-gray-400">
          Monte Carlo
        </p>
        <h1 className="font-serif text-4xl font-bold">Tournament simulator</h1>
        <p className="text-sm text-gray-500 max-w-md leading-relaxed">
          Simulates the full 2026 bracket thousands of times using your trained
          model and returns each team's win probability.
        </p>
      </div>

      <div className="flex gap-3 items-end">
        <div className="space-y-1">
          <label className="text-xs text-gray-500 uppercase tracking-wide">
            Simulations
          </label>
          <select
            value={runs}
            onChange={(e) => setRuns(Number(e.target.value))}
            className="border border-gray-200 px-3 py-2 text-sm bg-white focus:outline-none focus:border-black"
          >
            <option value={500}>500</option>
            <option value={1000}>1 000</option>
            <option value={2000}>2 000</option>
            <option value={5000}>5 000</option>
          </select>
        </div>
        <button
          onClick={simulate}
          disabled={loading}
          className="bg-black text-white text-sm px-5 py-2 hover:bg-gray-800 transition-colors disabled:opacity-40"
        >
          {loading ? "Simulating…" : "Run →"}
        </button>
      </div>

      {loading && (
        <div className="space-y-2">
          <div className="h-0.5 bg-gray-100 w-full overflow-hidden">
            <div className="h-full bg-black animate-pulse w-1/2" />
          </div>
          <p className="text-xs text-gray-400">
            Running {runs.toLocaleString()} simulations…
          </p>
        </div>
      )}

      {error && <p className="text-sm text-red-500">{error}</p>}

      {results.length > 0 && (
        <div className="space-y-1">
          <div className="grid grid-cols-3 text-xs text-gray-400 uppercase tracking-wide pb-2 border-b border-gray-100">
            <span>Rank</span>
            <span>Team</span>
            <span>Win probability</span>
          </div>
          {results.map((t, i) => (
            <div
              key={t.team}
              className="grid grid-cols-3 items-center py-2.5 border-b border-gray-50"
            >
              <span className="text-xs text-gray-400">{i + 1}</span>
              <span className="text-sm font-medium">{t.team}</span>
              <div className="flex items-center gap-3">
                <div className="h-1 bg-gray-100 rounded-full flex-1 max-w-28">
                  <div
                    className="h-full bg-black rounded-full transition-all duration-500"
                    style={{ width: `${(t.probability / max) * 100}%` }}
                  />
                </div>
                <span className="text-xs font-mono text-gray-600 w-10">
                  {t.probability}%
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}