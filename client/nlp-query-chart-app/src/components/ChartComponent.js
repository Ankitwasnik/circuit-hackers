import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function ChartComponent({ data }) {
  return (
    <div className="w-full max-w-lg mt-6">
      <Bar
        data={{
          labels: data.map((item) => item.name),
          datasets: [
            {
              label: "Values",
              data: data.map((item) => item.value),
              backgroundColor: "#4F46E5",
            },
          ],
        }}
      />
    </div>
  );
}