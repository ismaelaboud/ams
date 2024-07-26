import { toast } from "@/components/ui/use-toast";
import { apiUrl } from "./axios";

export const fetchAllAssets = async () => {
  const accessToken = localStorage.getItem("access");
  try {
    const { data } = await apiUrl.get("/assets/", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    return data;
  } catch (error: any) {
    console.log(error);
  }
};
