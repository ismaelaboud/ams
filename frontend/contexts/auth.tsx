"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiUrl } from "@/lib/axios";
import { toast } from "@/components/ui/use-toast";

export type User = [
  {
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
  }
];

export type Auth = {
  user: User;
  registerUser: () => void;
  loginUser: () => void;
};

export const AuthContext = createContext<Auth>({} as Auth);

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [user, setUser] = useState<User | undefined>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();

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
        description: error?.message,
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
      setLoading(false);

      toast({
        title: "Success",
        description: data?.message || "Login successful",
      });
      router.push("/dashboard");
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.message,
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  useEffect(() => {
    if (localStorage.getItem("access")) {
      const getAccountDetails = async () => {
        const accessToken = localStorage.getItem("access");
        const { data } = await apiUrl.get("/user_profiles/", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        setUser(data);
      };

      getAccountDetails();
    }
  }, []);

  const values: any = { loading, user, registerUser, loginUser };
  return (
    <>
      <AuthContext.Provider value={values}>{children}</AuthContext.Provider>
    </>
  );
}

export const useAuth = () => {
  return useContext(AuthContext);
};
