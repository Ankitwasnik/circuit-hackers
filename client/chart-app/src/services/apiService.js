import axios from "axios";

export async function fetchData(query) {
  try {
    const response = await axios.post("https://api.example.com/data", { query });
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return { labels: [], values: [] };
  }
}
