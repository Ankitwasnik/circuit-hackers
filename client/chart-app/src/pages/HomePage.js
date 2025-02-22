import React, { useState } from "react";
import FormComponent from "../components/FormComponent";
import ChartComponent from "../components/ChartComponent";
import { fetchData } from "../services/apiService"
import "../styles/HomePage.css";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function HomePage() {
  const [chartType, setChartType] = useState("");
  const [query, setQuery] = useState("");
  const [chartData, setChartData] = useState(null);
  const [showChart, setShowChart] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const fetchChartData = async () => {
    try {
      const data = await fetchData({ query });
      console.log(data, typeof data)
      // Error Handling
      if (!data || (Array.isArray(data) && data.length === 0)) {
        toast.error("No data available for the selected chart type.");
        setErrorMessage("No data available for the selected chart type.");
        setChartData(null);
        return;
      }

      if (typeof data === "string") {
        toast.error("No data available for the selected chart type.");
        setErrorMessage(`Error: ${data}`);
        setChartData(null);
        return;
      }

      setChartData(data);
      setErrorMessage("");
      setShowChart(true);
    } catch (error) {
      setErrorMessage("Failed to load chart data. Please try again.");
      toast.error("Failed to load chart data. Please try again.");
      setChartData(null);
    }
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    // setChartData({
    //   labels: ["Jan", "Feb", "Mar", "Apr", "May"],
    //   datasets: [
    //     {
    //       label: "Sample Data",
    //       data: [10, 20, 30, 40, 50],
    //       backgroundColor: "rgba(75,192,192,0.6)",
    //     },
    //   ],
    // });
    fetchChartData(chartType);
};

  return (
    <div className="page-wrapper">
      <div className={`card-container ${showChart ? "moved" : ""}`}>
        <div className="form-card">
          <FormComponent
            chartType={chartType}
            setChartType={setChartType}
            query={query}
            setQuery={setQuery}
            handleSubmit={handleSubmit}
          />
        </div>
        <div className={`chart-card ${showChart ? "show" : ""}`}>
          {chartType && chartData && <ChartComponent chartType={chartType} data={chartData} />}
        </div>
      </div>
    </div>
  );
}



export default HomePage;
