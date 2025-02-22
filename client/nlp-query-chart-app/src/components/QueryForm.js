import React, { useState } from "react";
import axios from "axios";
import ChartComponent from "./ChartComponent";

export default function QueryForm() {
  const [query, setQuery] = useState("");
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post("https://your-api-url.com/query", { query });
      setChartData(response.data.chartData);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-lg bg-white p-6 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-4 text-center">Query</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          className="border w-full p-2 rounded-lg mb-2"
          rows="4"
          placeholder="Enter your query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        ></textarea>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-lg w-full">
          {loading ? "Loading..." : "Submit"}
        </button>
      </form>
      {chartData && <ChartComponent data={chartData} />}
    </div>
  );
}