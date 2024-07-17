"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

const formSchema = z.object({
  name: z.string().min(3, {
    message: "Assett name must be atleast 3 characters",
  }),
  description: z.string().min(10, {
    message: "Asset description must be atleast 10 characters",
  }),
  serialNumber: z.string().min(5, {
    message: "Asset serial no. must be atleast 5 characters",
  }),
  assetType: z.string().min(1, {
    message: "Please select a asset type.",
  }),
  category: z.string().min(1, {
    message: "Please select asset category.",
  }),
});

type AssetAddFormValues = z.infer<typeof formSchema>;

export const categories = [
  {
    title: "Electronics",
    value: "electronics",
  },
  {
    title: "Furnitures",
    value: "furnitures",
  },
  {
    title: "Office Supplies",
    value: "office-supplies",
  },
];

export default function AssetAddForm() {
  const form = useForm<AssetAddFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
      serialNumber: "",
      assetType: "",
      category: "",
    },
  });

  const onSubmit = async (data: AssetAddFormValues) => {
    console.log(data);
  };

  return (
    <>
      <section>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-8 px-1 w-full"
          >
            <div className="grid sm:grid-cols-2 gap-8">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Asset name</FormLabel>
                    <FormControl>
                      <Input
                        type="text"
                        placeholder="Asset name"
                        {...field}
                        className="w-full"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="category"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Category</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a category" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {categories.map((option: any, index: number) => (
                          <SelectItem key={index} value={option?.value}>
                            {option?.title}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="grid sm:grid-cols-2 gap-8">
              <FormField
                control={form.control}
                name="serialNumber"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Serial number</FormLabel>
                    <FormControl>
                      <Input
                        type="text"
                        placeholder="Serial Number"
                        {...field}
                        className="w-full"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="assetType"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Asset type</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select asset type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {categories.map((option: any, index: number) => (
                          <SelectItem key={index} value={option?.value}>
                            {option?.title}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="grid sm:grid-cols-2 gap-8">
              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Asset description</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Tell us a little bit about this asset"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Make sure to describe the asset well
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <Button>Add asset</Button>
          </form>
        </Form>
      </section>
    </>
  );
}
