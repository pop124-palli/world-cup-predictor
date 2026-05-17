import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Home() {
  const [top, setTop] = useState([]);

  useEffect(() => {
    fetch("/api/teams/top?n=10")
      .then((r) => r.json())
      .then(setTop)
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-16">
      <section className="space-y-4 pt-8">
        <p className="text-xs tracking-widest uppercase text-gray-400 font-sans">
          FIFA World Cup 2026
        </p>
        <h1 className="font-serif text-5xl font-bold leading-tight">
          Who will lift
          <br />
          the trophy?
        </h1>
        <p className="text-gray-500 max-w-md text-sm leading-relaxed">
          Data-driven predictions powered by 50,000+ international matches,
          ELO ratings, and machine learning.
        </p>
        <div className="flex gap-4 pt-2">
          <Link
            to="/predict"
            className="bg-black text-white text-sm px-5 py-2.5 hover:bg-gray-800 transition-colors"
          >
            Predict a match →
          </Link>
          <Link
            to="/simulate"
            className="border border-black text-sm px-5 py-2.5 hover:bg-gray-50 transition-colors"
          >
            Simulate tournament
          </Link>
        </div>
      </section>

      {top.length > 0 && (
        <section className="space-y-4">
          <h2 className="font-serif text-xl font-bold">Top 10 by ELO</h2>
          <div className="divide-y divide-gray-100">
            {top.map((t) => (
              <div key={t.team} className="flex justify-between items-center py-3">
                <div className="flex items-center gap-4">
                  <span className="text-xs text-gray-400 w-4">{t.rank}</span>
                  <span className="text-sm font-medium">{t.team}</span>
                </div>
                <span className="text-xs text-gray-500 font-mono">{t.elo}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}