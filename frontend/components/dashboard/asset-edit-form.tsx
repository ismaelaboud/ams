"use client";

import { useRouter } from "next/navigation";
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
import React, { useEffect, useState } from "react";
import { toast } from "../ui/use-toast";
import { Label } from "../ui/label";
import { Category, Department } from "./asset-add-form";

export type CurrentAsset = {
  id: number;
  category_id: number;
  category_name: string;
  name: string;
  assetType: string;
  description: string;
  serialNumber: string;
  dateRecorded: string;
  status: string;
  departmentName: string;
};

export default function AssetAddForm({ params }: { params: { id: string } }) {
  const [asset, setAsset] = useState<CurrentAsset | undefined>(undefined);
  const [categories, setCategories] = useState<Category[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [updating, setUpdating] = useState<boolean>(false);
  const [assetName, setAssetName] = useState<string>("");
  const [category, setCategory] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [serialNumber, setSerialNumber] = useState<string>("");
  const [departmentName, setDepartmentName] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [assetType, setAssetType] = useState<string>("");
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
    const getCurrentAsset = async () => {
      const accessToken = localStorage.getItem("access");
      const { data } = await apiUrl.get(`/assets/${params?.id}/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setAsset(data);
    };

    setAssetName(asset?.name ?? "");
    setCategory(asset?.category_name ?? "");
    setDescription(asset?.description ?? "");
    setSerialNumber(asset?.serialNumber ?? "");
    setDepartmentName(asset?.departmentName ?? "");
    setStatus(asset?.status ?? "");
    setAssetType(asset?.assetType ?? "");

    getCurrentAsset();
    getCategories();
    getDepartments();
  }, [
    params?.id,
    asset?.assetType,
    asset?.category_name,
    asset?.departmentName,
    asset?.description,
    asset?.name,
    asset?.serialNumber,
    asset?.status,
  ]);

  const handleAssetUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const payload = {
      category,
      name: assetName,
      assetType,
      description,
      serialNumber,
      status,
      departmentName,
    };

    try {
      const accessToken = localStorage.getItem("access");
      setUpdating(true);
      const { data } = await apiUrl.put(
        `/assets/detail/${params?.id}/`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      setUpdating(false);
      toast({
        title: "Success",
        description: data?.message || "Asset updated successfully",
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
      setUpdating(false);
    }
  };

  return (
    <>
      <section>
        <>
          <form onSubmit={handleAssetUpdate} className="space-y-8 px-1 w-full">
            <div className="grid sm:grid-cols-2 gap-8">
              <div>
                <Label className="block mb-3">Asset name</Label>
                <Input
                  type="text"
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setAssetName(e.target.value)
                  }
                  className="w-full"
                  defaultValue={assetName}
                  name="name"
                />
              </div>
              <div>
                <Label className="block mb-3">Category</Label>
                <Select
                  onValueChange={(value) => setCategory(value)}
                  defaultValue={category}
                  name="category"
                >
                  <SelectTrigger>
                    <SelectValue placeholder={category} />
                  </SelectTrigger>
                  <SelectContent>
                    {categories?.map((option: Category) => (
                      <SelectItem key={option?.id} value={option?.name}>
                        {option?.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid sm:grid-cols-2 gap-8">
              <div>
                <Label className="block mb-3">Department name</Label>
                <Select
                  onValueChange={(value) => setDepartmentName(value)}
                  defaultValue={departmentName}
                  name="departmentName"
                >
                  <SelectTrigger>
                    <SelectValue placeholder={departmentName} />
                  </SelectTrigger>
                  <SelectContent>
                    {departments?.map((option: Department) => (
                      <SelectItem key={option?.id} value={option?.name}>
                        {option?.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label className="block mb-3">Asset type</Label>
                <Input
                  type="text"
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setAssetType(e.target.value)
                  }
                  className="w-full"
                  defaultValue={assetType}
                  name="assetType"
                />
              </div>
            </div>
            <div className="grid sm:grid-cols-2 gap-8">
              <div>
                <Label className="block mb-3">Serial number</Label>
                <Input
                  type="text"
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setSerialNumber(e.target.value)
                  }
                  className="w-full"
                  defaultValue={serialNumber}
                  name="serialNumber"
                  disabled
                />
                <p className="mt-3 text-sm text-muted-foreground">
                  This value is readonly
                </p>
              </div>
              <div>
                <Label className="block mb-3">Status</Label>
                <Select
                  onValueChange={(value) => setStatus(value)}
                  defaultValue={status}
                  name="status"
                >
                  <SelectTrigger>
                    <SelectValue placeholder={status} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Available">Available</SelectItem>
                    <SelectItem value="Maintenance">Maintenance</SelectItem>
                    <SelectItem value="Booked">Booked</SelectItem>
                    <SelectItem value="In use">In use</SelectItem>
                    <SelectItem value="Archived">Archived</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid sm:grid-cols-2 gap-8">
              <div>
                <Label className="block mb-3">Asset description</Label>
                <Textarea
                  name="description"
                  defaultValue={description}
                  className="resize-none"
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                    setDescription(e.target.value)
                  }
                />
                <p className="mt-3 text-sm text-muted-foreground">
                  Make sure to describe the asset well
                </p>
              </div>
            </div>
            <Button type="submit" disabled={updating} aria-disabled={updating}>
              {updating ? "Updating..." : "Update asset"}
            </Button>
          </form>
        </>
      </section>
    </>
  );
}
