"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiUrl } from "@/lib/axios";
import { toast } from "@/components/ui/use-toast";

export type User = {
  id?: number;
  role: string;
  department: {
    name: string;
  };
  user: {
    email: string;
    username: string;
    firstName: string;
    lastName: string;
    date_joined: string;
    id?: number;
  };
};

export type Auth = {
  user: User;
  loading: boolean;
  registerUser: (
    username: string,
    password: string,
    password2: string,
    email: string,
    firstName: string,
    lastName: string
  ) => void;
  loginUser: (usernameOrEmail: string, password: string) => void;
  logoutUser: () => void;
  forgotPassword: (email: string) => void;
  resetPassword: (
    uidb64: string,
    token: string,
    new_password: string,
    confirm_new_password: string
  ) => void;
  updateProfile: (firstName: string, lastName: string) => void;
  updatePassword: (
    oldPassword: string,
    newPassword: string,
    newPasswordConfirm: string
  ) => void;
};

export const AuthContext = createContext<Auth>({} as Auth);

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [user, setUser] = useState<User | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();

  const getAccountDetails = async () => {
    const accessToken = localStorage.getItem("access");
    const { data } = await apiUrl.get("/profile/", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    setUser(data);
  };

  useEffect(() => {
    if (localStorage.getItem("access")) {
      getAccountDetails();
    }
  }, []);

  const registerUser = async (
    username: string,
    password: string,
    password2: string,
    email: string,
    firstName: string,
    lastName: string
  ) => {
    try {
      setLoading(true);
      const { data } = await apiUrl.post("/auth/register/", {
        username,
        password,
        password2,
        email,
        firstName,
        lastName,
      });
      setLoading(false);

      toast({
        title: "Success",
        description: data?.message || "Account created successfully",
      });
      router.push("/login");
    } catch (error: any) {
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const loginUser = async (usernameOrEmail: string, password: string) => {
    try {
      setLoading(true);
      const { data } = await apiUrl.post("/auth/login/", {
        usernameOrEmail,
        password,
      });
      localStorage.setItem("access", data?.access);
      localStorage.setItem("refresh", data?.refresh);
      const accessToken = localStorage.getItem("access");
      const res = await apiUrl.get("/profile/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      setUser(res?.data);
      setLoading(false);

      toast({
        title: "Success",
        description: res?.data?.message || "Login successful",
      });
      router.push("/dashboard");
    } catch (error: any) {
      console.log(error);
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const logoutUser = async () => {
    const refresh_token = localStorage.getItem("refresh");
    const accessToken = localStorage.getItem("access");

    try {
      setLoading(true);
      const { data } = await apiUrl.post(
        "/auth/logout/",
        {
          refresh_token,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      setUser(undefined);
      setLoading(false);

      toast({
        title: "Success",
        description: data?.message || "Logout successful",
      });
      router.push("/login");
    } catch (error: any) {
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const forgotPassword = async (email: string) => {
    try {
      setLoading(true);
      const { data } = await apiUrl.post("/password_reset/", { email });

      setLoading(false);

      toast({
        title: "Success",
        description: data?.message || "Reset link sent to your email",
      });
    } catch (error: any) {
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const resetPassword = async (
    uidb64: string,
    token: string,
    new_password: string,
    confirm_new_password: string
  ) => {
    try {
      setLoading(false);
      const { data } = await apiUrl.post("/reset-password-confirm/", {
        uidb64,
        token,
        new_password,
        confirm_new_password,
      });
      setLoading(false);

      toast({
        title: "Success",
        description: data?.message || "Password reset successful",
      });

      router.push("/login");
    } catch (error: any) {
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const updateProfile = async (firstName: string, lastName: string) => {
    const accessToken = localStorage.getItem("access");

    try {
      setLoading(true);
      const user = {
        firstName,
        lastName,
      };

      const { data } = await apiUrl.put(
        "/profile/",
        {
          user,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      setLoading(false);
      setUser(data);
      toast({
        title: "Success",
        description: data?.message || "Profile update successful",
      });
    } catch (error: any) {
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const updatePassword = async (
    oldPassword: string,
    newPassword: string,
    newPasswordConfirm: string
  ) => {
    const accessToken = localStorage.getItem("access");

    try {
      setLoading(true);
      const { data } = await apiUrl.post(
        "/auth/change_password/",
        {
          oldPassword,
          newPassword,
          newPasswordConfirm,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      setLoading(false);
      toast({
        title: "Success",
        description: data?.message || "Password update successful",
      });
    } catch (error: any) {
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const values: any = {
    loading,
    user,
    registerUser,
    loginUser,
    logoutUser,
    forgotPassword,
    resetPassword,
    updateProfile,
    updatePassword,
  };
  return (
    <>
      <AuthContext.Provider value={values}>{children}</AuthContext.Provider>
    </>
  );
}

export const useAuth = () => {
  return useContext(AuthContext);
};
