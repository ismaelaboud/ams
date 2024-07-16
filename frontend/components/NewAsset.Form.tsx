"use client";

import React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Input } from "@/components/ui/input";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

const formSchema = z.object({
  name: z.string().min(2, {
    message: "Name must be at least 2 characters.",
  }),
});

const NewAssetForm: React.FC = () => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
    },
  });

  const { handleSubmit, control } = form;

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values);
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">New Asset</h2>
      <Form {...form}>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel className={cn("block text-sm font-medium text-gray-700")}>
                  Name
                </FormLabel>
                <Input placeholder="shadcn" {...field} />
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel className={cn("block text-sm font-medium text-gray-700")}>
                  Description
                </FormLabel>
                <Input placeholder="description" {...field} />
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel className={cn("block text-sm font-medium text-gray-700")}>
                  Serial number
                </FormLabel>
                <Input placeholder="serial number" {...field} />
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel className={cn("block text-sm font-medium text-gray-700")}>
                  Category
                </FormLabel>
                <Input placeholder="select category" {...field} />
                <FormMessage />
              </FormItem>
            )}
          />
          <Button
            type="submit"
            className={cn(
              "inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 focus:ring-blue-500"
            )}
          >
            Add
          </Button>
        </form>
      </Form>
    </div>
  );
};

export default NewAssetForm;
