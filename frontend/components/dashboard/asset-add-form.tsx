"use client";

import { useRouter } from "next/navigation";
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
import { apiUrl } from "@/lib/axios";
import { useEffect, useState } from "react";
import { toast } from "../ui/use-toast";

const formSchema = z.object({
  name: z.string().min(3, {
    message: "Asset name must be atleast 3 characters",
  }),
  description: z.string().min(10, {
    message: "Asset description must be atleast 10 characters",
  }),
  assetType: z.string().min(1, {
    message: "Please add an asset type.",
  }),
  departmentName: z.string().min(1, {
    message: "Please add an asset department.",
  }),
  category: z.string().min(1, {
    message: "Please select an asset category.",
  }),
  status: z.string().min(1, {
    message: "Please select asset status.",
  }),
});

type AssetAddFormValues = z.infer<typeof formSchema>;

export type Category = {
  id: number;
  name: string;
};

export type Department = {
  id: number;
  name: string;
};

export default function AssetAddForm() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [adding, setAdding] = useState<boolean>(false);
  const router = useRouter();

  const getCategories = async () => {
    const accessToken = localStorage.getItem("access");
    const { data } = await apiUrl.get("/categories/", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    setCategories(data);
  };

  const getDepartments = async () => {
    const accessToken = localStorage.getItem("access");
    const { data } = await apiUrl.get("/departments/", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    setDepartments(data);
  };

  useEffect(() => {
    getCategories();
    getDepartments();
  }, []);

  const form = useForm<AssetAddFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
      assetType: "",
      category: "",
      departmentName: "",
      status: "",
    },
  });

  const onSubmit = async (data: AssetAddFormValues) => {
    const randomNumber = Math.floor(Math.random() * 1000000);
    const serialNumber = `AS${randomNumber}`;

    const payload = {
      ...data,
      serialNumber,
    };

    try {
      const accessToken = localStorage.getItem("access");
      setAdding(true);
      const { data } = await apiUrl.post("/assets/", payload, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      setAdding(false);
      toast({
        title: "Success",
        description: data?.message || "Asset added successfully",
      });
      router.push("/dashboard/assets");
    } catch (error: any) {
      toast({
        title: "Error",
        description:
          error?.response?.data?.message ||
          "Something went wrong, Please try again",
        variant: "destructive",
      });
      setAdding(false);
    }
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
                        {categories?.map((option: Category) => (
                          <SelectItem key={option?.id} value={option?.name}>
                            {option?.name}
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
                name="departmentName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Department name</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a department" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {departments?.map((option: Department) => (
                          <SelectItem key={option?.id} value={option?.name}>
                            {option?.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
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
                    <FormControl>
                      <Input
                        type="text"
                        placeholder="Asset type"
                        {...field}
                        className="w-full"
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
              <FormField
                control={form.control}
                name="status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Status</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Available">Available</SelectItem>
                        <SelectItem value="Maintenance">Maintenance</SelectItem>
                        <SelectItem value="Booked">Booked</SelectItem>
                        <SelectItem value="In use">In use</SelectItem>
                        <SelectItem value="Archived">Archived</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <Button type="submit" disabled={adding} aria-disabled={adding}>
              {adding ? "Adding..." : "Add asset"}
            </Button>
          </form>
        </Form>
      </section>
    </>
  );
}
