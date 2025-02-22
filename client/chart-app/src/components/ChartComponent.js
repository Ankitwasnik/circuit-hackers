import React from "react";
import { Bar, Line, Pie, Doughnut } from "react-chartjs-2";
import "chart.js/auto";
import "../styles/ChartComponent.css";

function ChartComponent({ chartType, data }) {
  const renderChart = () => {
    switch (chartType) {
      case "bar":
        return <Bar data={data} />;
      case "line":
        return <Line data={data} />;
      case "pie":
        return <Pie data={data} />;
      case "doughnut":
        return <Doughnut data={data} />;
      default:
        return null;
    }
  };

  return <div className="chart-container">{renderChart()}</div>;
}

export default ChartComponent;