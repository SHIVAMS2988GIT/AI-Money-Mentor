import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Fire from "./pages/Fire";
import Tax from "./pages/Tax";
import Portfolio from "./pages/Portfolio";
import Login from "./pages/Login";

export default function App() {

  const isLoggedIn = localStorage.getItem("user");

  return (
    <Router>
      {isLoggedIn ? (
        <div style={{ display: "flex" }}>
          <Sidebar />

          <div style={{ flex: 1, padding: 20 }}>
            <Routes>
              <Route path="/" element={<Fire />} />
              <Route path="/tax" element={<Tax />} />
              <Route path="/portfolio" element={<Portfolio />} />
            </Routes>
          </div>
        </div>
      ) : (
        <Login />
      )}
    </Router>
  );
}