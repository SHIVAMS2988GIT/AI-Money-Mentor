import { useState } from "react";
import { PieChart, Pie, Cell } from "recharts";

export default function Portfolio() {

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const fetchData = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/portfolio", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    setResult(data);
  };

  const COLORS = ["#4CAF50", "#2196F3"];

  const allocationData = result ? [
    { name: "Equity", value: result.allocation.equity_percent },
    { name: "Debt", value: result.allocation.debt_percent }
  ] : [];

  return (
    <div>
      <h1>Portfolio</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={fetchData}>Analyze</button>

      {result && (
        <>
          <PieChart width={300} height={300}>
            <Pie data={allocationData} dataKey="value">
              {allocationData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>
          </PieChart>

          <p>XIRR: {result.xirr}%</p>
        </>
      )}
    </div>
  );
}