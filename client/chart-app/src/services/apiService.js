import axios from "axios";
import  paths from "../constants/path";

export async function fetchData(query) {
  const serverPath = process.env.REACT_APP_API_URL;
  console.log(serverPath,'server')
  try {
    console.log(query,'query')
    const response = await axios.get(`${serverPath}/${paths.query}`, { query });
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return { labels: [], values: [] };
  }
}
