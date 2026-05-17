import { NavLink } from "react-router-dom";

const links = [
  { to: "/",         label: "Home" },
  { to: "/predict",  label: "Predictor" },
  { to: "/elo",      label: "ELO" },
  { to: "/squad",    label: "Squad" },
  { to: "/simulate", label: "Simulate" },
];

export default function Navbar() {
  return (
    <header className="border-b border-gray-200 bg-white sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-6 flex items-center justify-between h-14">
        <span className="font-serif font-bold text-lg tracking-tight">
          WC26 Predictor
        </span>
        <nav className="flex gap-6">
          {links.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              className={({ isActive }) =>
                `text-sm transition-colors ${
                  isActive
                    ? "text-black font-semibold"
                    : "text-gray-500 hover:text-black"
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}