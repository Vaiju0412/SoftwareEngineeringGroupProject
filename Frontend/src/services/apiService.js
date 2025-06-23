import axios from "axios";

const apiService = axios.create({
  baseURL: "http://127.0.0.1:5000",
  headers: {
    "Access-Control-Allow-Origin": "*", // Replace with your Vue.js app's URL if needed
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    Authorization:`Bearer`+sessionStorage.getItem("accesstoken"),
  },
});
export default apiService