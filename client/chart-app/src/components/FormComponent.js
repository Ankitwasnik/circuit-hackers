import React from "react";
import "../styles/FormComponent.css";

const chartOptions = ["Bar", "Line", "Pie", "Doughnut"];

function FormComponent({ chartType, setChartType, query, setQuery, handleSubmit }) {
  return (
    <form onSubmit={handleSubmit} className="form-container">
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter query here"
        rows={4}
        cols={50}
        className="text-area"
      />
      <br />
      <select value={chartType} onChange={(e) => setChartType(e.target.value)} className="dropdown">
        <option value="">Select Chart Type</option>
        {chartOptions.map((type) => (
          <option key={type} value={type.toLowerCase()}>{type}</option>
        ))}
      </select>
      <br />
      <button type="submit" className="submit-btn">Submit</button>
    </form>
  );
}

export default FormComponent;