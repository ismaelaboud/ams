"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Separator } from "../ui/separator";
import { Button } from "../ui/button";

const formSchema = z.object({
  firstName: z.string().min(3, {
    message: "Firstname must be atleast 3 characters",
  }),
  lastName: z.string().min(3, {
    message: "Lastname must be atleast 3 characters",
  }),
  email: z.string().email({
    message: "Please a valid email",
  }),
  username: z.string().min(3, {
    message: "Username must be at least 3 characters.",
  }),
});

type ProfileFormValues = z.infer<typeof formSchema>;

export default function ProfileDetails() {
  const defaultValues: Partial<ProfileFormValues> = {};

  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues,
  });

  const onSubmit = async (data: ProfileFormValues) => {
    console.log(data);
  };

  return (
    <>
      <section className="mt-6">
        <div className="mb-4">
          <h2 className="text-xl font-bold tracking-tight">Profile details</h2>
          <p className="text-sm text-muted-foreground tracking-tight">
            Checkout your profile details
          </p>
        </div>
        <>
          <div>
            <span className="font-medium mr-2">Name:</span>
            <span className="text-sm text-muted-foreground">Jacob Kyalo</span>
          </div>
          <div>
            <span className="font-medium mr-2">Username:</span>
            <span className="text-sm text-muted-foreground">jack</span>
          </div>
          <div>
            <span className="font-medium mr-2">Email:</span>
            <span className="text-sm text-muted-foreground">
              jacob.k@gmail.com
            </span>
          </div>
          <div className="mb-4">
            <span className="font-medium mr-2">Account created on:</span>
            <span className="text-sm text-muted-foreground">
              25th July 2024
            </span>
          </div>
        </>
        <Separator />
        <div className="my-6">
          <h2 className="text-xl font-bold tracking-tight">Update profile</h2>
          <p className="text-sm text-muted-foreground tracking-tight">
            Update your profile details here
          </p>
        </div>
      </section>
      <section>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-8 px-1 w-full"
          >
            <div className="grid sm:grid-cols-2 gap-8">
              <FormField
                control={form.control}
                name="firstName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Firstname</FormLabel>
                    <FormControl>
                      <Input
                        type="text"
                        placeholder="Firstname"
                        {...field}
                        className="w-full"
                        defaultValue="firstname"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="lastName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Lastname</FormLabel>
                    <FormControl>
                      <Input
                        type="text"
                        placeholder="Lastname"
                        {...field}
                        className="w-full"
                        defaultValue="lastname"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="grid sm:grid-cols-2 gap-8">
              <FormField
                control={form.control}
                name="username"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Username</FormLabel>
                    <FormControl>
                      <Input
                        type="text"
                        placeholder="username"
                        {...field}
                        className="w-full"
                        defaultValue="username"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input
                        type="email"
                        placeholder="email"
                        {...field}
                        className="w-full"
                        defaultValue="user@gmail.com"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <Button>Update</Button>
          </form>
        </Form>
      </section>
    </>
  );
}
