import { useState } from "react";
import ProbBar from "../components/ProbBar";

const TEAMS = [
  "Brazil","France","Argentina","England","Spain","Germany","Portugal",
  "Netherlands","Belgium","Italy","Croatia","Uruguay","Mexico",
  "United States","Morocco","Senegal","Japan","South Korea","Australia",
  "Ecuador","Colombia","Poland","Switzerland","Denmark","Austria",
  "Turkey","Serbia","Ukraine","Iran","Saudi Arabia","Canada","Qatar",
];

export default function Predictor() {
  const [home, setHome] = useState("Brazil");
  const [away, setAway] = useState("France");
  const [neutral, setNeutral] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function predict() {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const r = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ home, away, is_neutral: neutral }),
      });
      const data = await r.json();
      if (!r.ok) throw new Error(data.detail || "Prediction failed");
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-12 max-w-lg">
      <div className="space-y-2">
        <p className="text-xs tracking-widest uppercase text-gray-400">Match Predictor</p>
        <h1 className="font-serif text-4xl font-bold">Pick two teams</h1>
      </div>

      <div className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-xs text-gray-500 uppercase tracking-wide">Home</label>
            <select
              value={home}
              onChange={(e) => setHome(e.target.value)}
              className="w-full border border-gray-200 px-3 py-2 text-sm bg-white focus:outline-none focus:border-black"
            >
              {TEAMS.map((t) => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-gray-500 uppercase tracking-wide">Away</label>
            <select
              value={away}
              onChange={(e) => setAway(e.target.value)}
              className="w-full border border-gray-200 px-3 py-2 text-sm bg-white focus:outline-none focus:border-black"
            >
              {TEAMS.map((t) => <option key={t}>{t}</option>)}
            </select>
          </div>
        </div>

        <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={neutral}
            onChange={(e) => setNeutral(e.target.checked)}
            className="accent-black"
          />
          Neutral venue
        </label>

        <button
          onClick={predict}
          disabled={loading || home === away}
          className="bg-black text-white text-sm px-6 py-2.5 hover:bg-gray-800 transition-colors disabled:opacity-40"
        >
          {loading ? "Predicting…" : "Predict →"}
        </button>
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}

      {result && (
        <div className="space-y-5 border-t border-gray-100 pt-8">
          <div className="flex justify-between text-xs text-gray-400 uppercase tracking-widest">
            <span>{result.home}</span>
            <span>vs</span>
            <span>{result.away}</span>
          </div>
          <div className="space-y-4">
            <ProbBar label={`${result.home} win`} value={result.home_win} />
            <ProbBar label="Draw" value={result.draw} />
            <ProbBar label={`${result.away} win`} value={result.away_win} flip />
          </div>
        </div>
      )}
    </div>
  );
}