import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Predictor from "./pages/Predictor";
import EloTracker from "./pages/EloTracker";
import Squad from "./pages/Squad";
import Simulate from "./pages/Simulate";

export default function App() {
  return (
    <div className="min-h-screen bg-white text-black">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-12">
        <Routes>
          <Route path="/"         element={<Home />} />
          <Route path="/predict"  element={<Predictor />} />
          <Route path="/elo"      element={<EloTracker />} />
          <Route path="/squad"    element={<Squad />} />
          <Route path="/simulate" element={<Simulate />} />
        </Routes>
      </main>
    </div>
  );
}