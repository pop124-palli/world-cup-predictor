import { useState } from "react";

const TEAMS = [
  "Brazil","France","Argentina","England","Spain","Germany","Portugal",
  "Netherlands","Belgium","Italy","Croatia","Uruguay","Mexico",
  "United States","Morocco","Senegal","Japan","South Korea","Australia",
  "Ecuador","Colombia","Poland","Switzerland","Denmark","Austria",
  "Turkey","Serbia","Ukraine","Iran","Saudi Arabia","Canada","Qatar",
];

export default function Squad() {
  const [team, setTeam] = useState("Brazil");
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`/api/teams/${encodeURIComponent(team)}/squad`);
      if (!r.ok) throw new Error("Squad data not found.");
      const d = await r.json();
      if (d.length === 0) throw new Error("No players found for this team. Check fifa_players.csv.");
      setPlayers(d);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const maxPSS = players.length ? Math.max(...players.map((p) => p.PSS)) : 1;

  return (
    <div className="space-y-10">
      <div className="space-y-2">
        <p className="text-xs tracking-widest uppercase text-gray-400">Squad Explorer</p>
        <h1 className="font-serif text-4xl font-bold">Squad strength</h1>
      </div>

      <div className="flex gap-3 items-end">
        <div className="space-y-1">
          <label className="text-xs text-gray-500 uppercase tracking-wide">Nation</label>
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

      {players.length > 0 && (
        <div className="space-y-1">
          <div className="grid grid-cols-3 text-xs text-gray-400 uppercase tracking-wide pb-2 border-b border-gray-100">
            <span>Player</span>
            <span>Club</span>
            <span>PSS</span>
          </div>
          {players.map((p, i) => (
            <div
              key={i}
              className="grid grid-cols-3 items-center py-2.5 border-b border-gray-50 hover:bg-gray-50 transition-colors"
            >
              <span className="text-sm font-medium">{p.short_name}</span>
              <span className="text-xs text-gray-500">{p.club_name}</span>
              <div className="flex items-center gap-2">
                <div className="h-1 bg-gray-100 rounded-full flex-1 max-w-20">
                  <div
                    className="h-full bg-black rounded-full"
                    style={{ width: `${(p.PSS / maxPSS) * 100}%` }}
                  />
                </div>
                <span className="text-xs font-mono text-gray-600">
                  {p.PSS?.toFixed ? p.PSS.toFixed(1) : p.PSS}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}