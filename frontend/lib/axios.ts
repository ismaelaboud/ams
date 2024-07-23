import axios from "axios";

export const apiUrl = axios.create({
  baseURL: "http://10.0.3.169:8000/api",
});
