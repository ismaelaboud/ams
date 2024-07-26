"use client";

import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/contexts/auth";

const formSchema = z.object({
  usernameOrEmail: z.string().min(2, {
    message: "Please enter a valid email address or username.",
  }),
  password: z.string().min(8, {
    message: "Password must be at least 8 characters.",
  }),
});

export default function LoginForm() {
  const { loading, loginUser } = useAuth();

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      usernameOrEmail: "",
      password: "",
    },
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    const { usernameOrEmail, password } = data;
    loginUser(usernameOrEmail, password);
  };

  return (
    <section className="flex items-center justify-center h-screen">
      <div className="flex flex-col gap-6 border rounded-lg p-10 max-w-md w-full">
        <div>
          <h2 className="text-3xl font-bold">Login</h2>
          <p className="text-muted-foreground">
            Enter your credentials to login
          </p>
        </div>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="usernameOrEmail"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email/Username</FormLabel>
                  <FormControl>
                    <Input
                      type="text"
                      placeholder="Email or Username"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="********" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="flex justify-end mt-0">
              <Link
                href="/forgot"
                className="text-primary hover:text-primary/90"
              >
                Forgot Password?
              </Link>
            </div>
            <Button
              disabled={loading}
              aria-disabled={loading}
              type="submit"
              className="w-full"
            >
              {loading ? "Please wait..." : "Login"}
            </Button>
            <p className="text-muted-foreground text-sm mt-2">
              Don&apos;t have an account?{" "}
              <Link href="/register" className="text-primary">
                Register
              </Link>
            </p>
          </form>
        </Form>
      </div>
    </section>
  );
}
