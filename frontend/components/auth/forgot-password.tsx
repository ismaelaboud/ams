"use client";

import Link from "next/link";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { MoveLeft } from "lucide-react";

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
  email: z.string().email({
    message: "Please enter a valid email",
  }),
});

export default function ForgotPassword() {
  const { loading, forgotPassword } = useAuth();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
    },
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    const { email } = data;
    forgotPassword(email);
  };

  return (
    <section className="flex items-center justify-center h-screen">
      <div className="flex flex-col gap-6 border rounded-lg p-10 max-w-md w-full">
        <div className="flex flex-col gap-y-1 mb-2">
          <Link
            href="/login"
            className="text-muted-foreground mb-2 hover:text-primary text-base flex gap-x-2 items-center"
          >
            <MoveLeft />
            <span>Back to login</span>
          </Link>

          <h3 className="text-4xl font-bold text-foreground leading-none">
            Forgot password?
          </h3>
          <p className="text-muted-foreground text-sm">
            Enter your email to get a reset link
          </p>
        </div>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email address</FormLabel>
                  <FormControl>
                    <Input
                      type="email"
                      placeholder="Email address"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button
              disabled={loading}
              aria-disabled={loading}
              type="submit"
              className="w-full"
            >
              {loading ? "Please wait..." : "Send reset link"}
            </Button>
          </form>
        </Form>
      </div>
    </section>
  );
}
