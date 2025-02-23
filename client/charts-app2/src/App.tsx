import { useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  ArcElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar, Line, Pie, Doughnut } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  ArcElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

const SERVER_URL = import.meta.env.VITE_SERVER_URL;
const QUERY_ENDPOINT = "/query";

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top" as const,
    },
    title: {
      display: true,
      text: "Chart",
    },
  },
};

const predefinedColors = [
  "rgb(255, 99, 132)",
  "rgb(255, 159, 64)",
  "rgb(255, 205, 86)",
  "rgb(75, 192, 192)",
  "rgb(54, 162, 235)",
  "rgb(153, 102, 255)",
  "rgb(201, 203, 207)",
];

const CHART_COLORS = {
  red: "rgb(255, 99, 132)",
  orange: "rgb(255, 159, 64)",
  yellow: "rgb(255, 205, 86)",
  green: "rgb(75, 192, 192)",
  blue: "rgb(54, 162, 235)",
  purple: "rgb(153, 102, 255)",
  grey: "rgb(201, 203, 207)",
};

const assignColors = (
  datasets: { label: string; data: number[] }[],
  chartType: string
) => {
  if (chartType === "pie" || chartType === "doughnut") {
    console.log("i am a pie or a doughnut");
    return datasets.map((dataset) => ({
      ...dataset,
      backgroundColor: Object.values(CHART_COLORS),
    }));
  } else {
    console.log("i am a bar or line");
    return datasets.map((dataset, index) => ({
      ...dataset,
      backgroundColor: predefinedColors[index % predefinedColors.length],
      borderColor: predefinedColors[index % predefinedColors.length].replace(
        "0.5",
        "1"
      ),
      borderWidth: 1,
    }));
  }
};

type Widget = {
  id: number;
  labels: string[];
  datasets: { label: string; data: number[] }[];
  input: string;
  loading: boolean;
  chartType: "bar" | "line" | "pie" | "doughnut";
  error: boolean;
};

function App() {
  const [widgets, setWidgets] = useState<Widget[]>([]);

  const addWidget = (): void => {
    setWidgets([
      ...widgets,
      {
        id: Date.now(),
        labels: [],
        datasets: [],
        input: "",
        loading: false,
        chartType: "bar",
        error: false,
      },
    ]);
  };

  const updateWidget = (id: number, value: string): void => {
    setWidgets(
      widgets.map((widget) =>
        widget.id === id ? { ...widget, input: value } : widget
      )
    );
  };

  const changeChartType = (
    id: number,
    chartType: "bar" | "line" | "pie" | "doughnut"
  ) => {
    setWidgets(
      widgets.map((widget) =>
        widget.id === id
          ? {
              ...widget,
              chartType,
              datasets: assignColors(widget.datasets, chartType),
            }
          : widget
      )
    );
  };

  const generateChart = async (id: number): Promise<void> => {
    setWidgets(
      widgets.map((w) =>
        w.id === id ? { ...w, loading: true, error: false } : w
      )
    );

    const widget = widgets.find((w) => w.id === id);
    if (!widget) return;

    try {
      const response = await fetch(SERVER_URL + QUERY_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: widget.input }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      const result = await response.json();
      if (
        result.status === "SUCCESS" &&
        result.labels?.length &&
        result.datasets?.length
      ) {
        setWidgets(
          widgets.map((w) =>
            w.id === id
              ? {
                  ...w,
                  labels: result.labels,
                  datasets: assignColors(result.datasets, widget.chartType),
                  loading: false,
                  error: false,
                }
              : w
          )
        );
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error("Error fetching chart data:", error);
      setWidgets(
        widgets.map((w) =>
          w.id === id
            ? { ...w, loading: false, labels: [], datasets: [], error: true }
            : w
        )
      );
    }
  };

  return (
    <>
      <div className="w-full h-full p-4">
        <div className="w-full bg-gray-800 text-white text-center py-4 text-xl font-bold">
          Circuit Hackers
        </div>
        <header className="text-center my-6">
          <h1 className="text-3xl font-bold">🏏 Welcome to Dashify</h1>
          <p className="text-gray-600">
            Explore IPL player statistics dynamically using natural language.
          </p>
        </header>
        <section className="bg-gray-100 p-4 rounded shadow-md my-6">
          <h2 className="text-2xl font-bold mb-2">What Data is Available?</h2>
          <div className="text-gray-700">
            <p>
              Each query is based on IPL player stats across multiple years. You
              can ask about:
            </p>
            <ul className="list-disc pl-5">
              <li>
                <strong>Player Performance:</strong> Total runs scored, Highest
                score in an innings, Number of fifties, and hundreds, Batting
                average, Strike rate
              </li>
              <li>
                <strong>Match & Innings Stats:</strong> Matches played, Innings
                played, Not-outs, Balls faced
              </li>
              <li>
                <strong>Boundaries & Hitting Power:</strong> 4s, 6s
              </li>
              <li>
                <strong>Year-wise Performance:</strong> Stats categorized by
                year
              </li>
            </ul>
            <p className="mt-3 font-semibold">
              🏆 Example Queries You Can Try:
            </p>
            <ul className="list-disc pl-5">
              <li>Who hit the most sixes in 2021?</li>
              <li>
                How has the total number of fours and sixes changed over the
                years?
              </li>
              <li>
                Show total runs and average strike rate of Rohit Sharma over the
                years.
              </li>
              <li>
                How many times have players remained not out compared to the
                total innings played each year?
              </li>
            </ul>
          </div>
        </section>
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded"
          onClick={addWidget}
        >
          Add Widget
        </button>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {widgets.map((widget) => (
            <div
              key={widget.id}
              className="p-3 border rounded shadow bg-white border-gray-200"
            >
              <div className="p-2">
                <textarea
                  rows={4}
                  placeholder="Enter a query"
                  value={widget.input}
                  onChange={(e) => updateWidget(widget.id, e.target.value)}
                  className="w-full p-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg"
                />
                <select
                  className="w-full mt-2 p-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg"
                  value={widget.chartType}
                  onChange={(e) =>
                    changeChartType(
                      widget.id,
                      e.target.value as "bar" | "line" | "pie" | "doughnut"
                    )
                  }
                >
                  <option value="bar">Bar Chart</option>
                  <option value="line">Line Chart</option>
                  <option value="pie">Pie Chart</option>
                  <option value="doughnut">Doughnut Chart</option>
                </select>
                <button
                  className="mt-2 px-4 py-2 bg-green-500 text-white rounded"
                  onClick={() => generateChart(widget.id)}
                >
                  {widget.loading ? "Loading..." : "Generate Chart"}
                </button>
                {widget.loading && (
                  <p className="mt-2 text-gray-500">Fetching data...</p>
                )}
                {!widget.loading && widget.error && (
                  <p className="mt-2 text-red-500">
                    Sorry, we cannot process your request right now. Please try
                    again later.
                  </p>
                )}
                {!widget.loading &&
                  !widget.error &&
                  widget.labels.length > 0 &&
                  (widget.chartType === "bar" ? (
                    <Bar
                      options={options}
                      data={{
                        labels: widget.labels,
                        datasets: widget.datasets,
                      }}
                    />
                  ) : widget.chartType === "line" ? (
                    <Line
                      options={options}
                      data={{
                        labels: widget.labels,
                        datasets: widget.datasets,
                      }}
                    />
                  ) : widget.chartType === "pie" ? (
                    <Pie
                      options={options}
                      data={{
                        labels: widget.labels,
                        datasets: widget.datasets,
                      }}
                    />
                  ) : (
                    <Doughnut
                      options={options}
                      data={{
                        labels: widget.labels,
                        datasets: widget.datasets,
                      }}
                    />
                  ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default App;
