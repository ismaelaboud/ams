import axios from "axios";

export const apiUrl = axios.create({
  baseURL: "https://ngemuantony.pythonanywhere.com/api",
});
