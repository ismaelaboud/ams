"use client";

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
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/contexts/auth";

const formSchema = z.object({
  new_password: z.string().min(8, {
    message: "New password must be at least 8 characters.",
  }),
  confirm_new_password: z.string().min(8, {
    message: "Confirm password must be at least 8 characters.",
  }),
});

export default function ResetPassword() {
  const { loading, resetPassword } = useAuth();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      new_password: "",
      confirm_new_password: "",
    },
  });

  const searchParams = useSearchParams();
  const uidb64 = searchParams?.get("uidb64") as string;
  const token = searchParams?.get("token") as string;

  function onSubmit(data: z.infer<typeof formSchema>) {
    const { new_password, confirm_new_password } = data;
    resetPassword(uidb64, token, new_password, confirm_new_password);
  }

  return (
    <section className="flex items-center justify-center h-screen">
      <div className="flex flex-col gap-6 border rounded-lg p-10 max-w-md w-full">
        <div>
          <h3 className="font-bold text-4xl text-foreground leading-none">
            Reset Password
          </h3>
          <p className="text-muted-foreground text-sm">
            Enter your new password to reset
          </p>
        </div>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
              control={form.control}
              name="new_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>New Password</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="New Password"
                      {...field}
                      type="password"
                      className="w-full"
                    />
                  </FormControl>

                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="confirm_new_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm Password</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Confirm Password"
                      {...field}
                      type="password"
                      className="w-full"
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
              {loading ? "Please wait..." : "Reset Password"}
            </Button>
          </form>
        </Form>
      </div>
    </section>
  );
}
