import React, { useState } from "react";
import FormComponent from "../components/FormComponent";
import ChartComponent from "../components/ChartComponent";
import "../styles/HomePage.css";

// function HomePage() {
//   const [chartType, setChartType] = useState("");
//   const [query, setQuery] = useState("");
//   const [chartData, setChartData] = useState(null);
//   const [showChart, setShowChart] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setChartData({
//       labels: ["Jan", "Feb", "Mar", "Apr", "May"],
//       datasets: [
//         {
//           label: "Sample Data",
//           data: [10, 20, 30, 40, 50],
//           backgroundColor: "rgba(75,192,192,0.6)",
//         },
//       ],
//     });
//     setShowChart(true);
//   };

//   return (
//     <div className="page-wrapper">
//       <div className={`card-container ${showChart ? "moved" : ""}`}>
//         <div className="form-card">
//           <FormComponent
//             chartType={chartType}
//             setChartType={setChartType}
//             query={query}
//             setQuery={setQuery}
//             handleSubmit={handleSubmit}
//           />
//         </div>
//         <div className={`chart-card ${showChart ? "show" : ""}`}>
//           {chartType && chartData && <ChartComponent chartType={chartType} data={chartData} />}
//         </div>
//       </div>
//     </div>
//   );
// }

function HomePage() {
    const [chartType, setChartType] = useState(""); // Holds dropdown selection
    const [selectedChartType, setSelectedChartType] = useState(""); // Holds chart type on submit
    const [query, setQuery] = useState("");
    const [chartData, setChartData] = useState(null);
    const [showChart, setShowChart] = useState(false);
  
    const handleSubmit = async (e) => {
      e.preventDefault();
  
      setChartData(
        {
            "labels": ["2016", "2017", "2018", "2019", "2020", "2021", "2022"],
            "datasets":[
                {
                    "label": "Total Runs",
                    "data": [17692,17907,19098,18574,18508,17716,23052]
                },
                {
                    "label": "Average Strike Rate",
                    "data": [115.03411764705882,112.15482517482518,114.95152173913043,109.6175,107.36473684210526,105.0556375838926,120.40623456790124]
                },
                {
                    "label": "Total Fours",
                    "data": [1632,1608,1652,1653,1582,1548,2017]
                },
                {
                    "label": "Total Sixes",
                    "data": [638,705,872,784,734,687,1062]
                },
                {
                    "label": "Total Hundreds",
                    "data": [7,5,5,6,5,4,8]
                },
                
            ]
        }
        
        );
  
      setSelectedChartType(chartType); // Store selected chart type only on submit
      setShowChart(true);
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
            {selectedChartType && chartData && <ChartComponent chartType={selectedChartType} data={chartData} />}
          </div>
        </div>
      </div>
    );
  }
  

export default HomePage;
