import { useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from "recharts";

const TEAMS = [
  "Brazil","France","Argentina","England","Spain","Germany","Portugal",
  "Netherlands","Belgium","Italy","Croatia","Uruguay","Mexico",
  "United States","Morocco","Senegal","Japan","South Korea","Australia",
  "Ecuador","Colombia","Poland","Switzerland","Denmark","Austria",
  "Turkey","Serbia","Ukraine","Iran","Saudi Arabia","Canada","Qatar",
];

export default function EloTracker() {
  const [team, setTeam] = useState("Brazil");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`/api/elo/${encodeURIComponent(team)}`);
      if (!r.ok) throw new Error("ELO history not found. Run pipeline.py first.");
      const d = await r.json();
      setData(d);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const current = data.length ? Math.round(data[data.length - 1].elo) : null;
  const peak = data.length ? Math.round(Math.max(...data.map((d) => d.elo))) : null;

  return (
    <div className="space-y-10">
      <div className="space-y-2">
        <p className="text-xs tracking-widest uppercase text-gray-400">ELO Tracker</p>
        <h1 className="font-serif text-4xl font-bold">Rating history</h1>
      </div>

      <div className="flex gap-3 items-end">
        <div className="space-y-1">
          <label className="text-xs text-gray-500 uppercase tracking-wide">Team</label>
          <select
            value={team}
            onChange={(e) => setTeam(e.target.value)}
            className="border border-gray-200 px-3 py-2 text-sm bg-white focus:outline-none focus:border-black"
          >
            {TEAMS.map((t) => <option key={t}>{t}</option>)}
          </select>
        </div>
        <button
          onClick={load}
          disabled={loading}
          className="bg-black text-white text-sm px-5 py-2 hover:bg-gray-800 transition-colors disabled:opacity-40"
        >
          {loading ? "Loading…" : "Load →"}
        </button>
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}

      {data.length > 0 && (
        <div className="space-y-6">
          <div className="flex gap-8">
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide">Current</p>
              <p className="font-serif text-3xl font-bold">{current}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide">Peak</p>
              <p className="font-serif text-3xl font-bold">{peak}</p>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 10, fill: "#9ca3af" }}
                tickFormatter={(v) => v.slice(0, 4)}
                interval={Math.floor(data.length / 6)}
              />
              <YAxis
                tick={{ fontSize: 10, fill: "#9ca3af" }}
                domain={["auto", "auto"]}
                width={40}
              />
              <Tooltip
                contentStyle={{ border: "1px solid #e5e7eb", borderRadius: 0, fontSize: 12 }}
                labelStyle={{ color: "#6b7280" }}
              />
              <Line
                type="monotone"
                dataKey="elo"
                stroke="#000"
                strokeWidth={1.5}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}