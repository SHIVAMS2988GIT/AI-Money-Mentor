import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div style={{ width: 220, background: "#020617", color: "white", padding: 20 }}>
      <h2>💰 Mentor</h2>

      <p><Link to="/" style={{ color: "white" }}>🔥 FIRE</Link></p>
      <p><Link to="/tax" style={{ color: "white" }}>💸 Tax</Link></p>
      <p><Link to="/portfolio" style={{ color: "white" }}>📊 Portfolio</Link></p>
    </div>
  );
}