export default function ProbBar({ label, value, flip = false }) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between text-xs text-gray-500">
        <span>{label}</span>
        <span className="font-semibold text-black">{value}%</span>
      </div>
      <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${
            flip ? "ml-auto bg-gray-700" : "bg-black"
          }`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}