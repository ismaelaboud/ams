"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/auth";

export default function ProfileDetails() {
  const { user } = useAuth();
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");

  useEffect(() => {
    setUsername(user[0]?.user?.username);
    setEmail(user[0]?.user?.email);
    setFirstName(user[0]?.user?.firstName);
    setLastName(user[0]?.user?.lastName);
  }, [user]);

  const handleProfileUpdate = async (e: any) => {
    e.preventDefault();
    console.log(username, email, firstName, lastName);
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
            <span className="text-sm text-muted-foreground">
              {user[0]?.user?.firstName} {user[0]?.user?.lastName}
            </span>
          </div>
          <div>
            <span className="font-medium mr-2">Username:</span>
            <span className="text-sm text-muted-foreground">
              {user[0]?.user?.username}
            </span>
          </div>
          <div>
            <span className="font-medium mr-2">Email:</span>
            <span className="text-sm text-muted-foreground">
              {user[0]?.user?.email}
            </span>
          </div>
          <div className="mb-4">
            <span className="font-medium mr-2">Account created on:</span>
            <span className="text-sm text-muted-foreground">
              {new Date(user[0]?.user?.date_joined).toLocaleString()}
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
        <form onSubmit={handleProfileUpdate} className="space-y-8 px-1 w-full">
          <div className="grid sm:grid-cols-2 gap-8">
            <div>
              <Label className="block mb-3">Firstname</Label>
              <Input
                type="text"
                placeholder="Firstname"
                onChange={(e) => setFirstName(e.target.value)}
                className="w-full"
                defaultValue={firstName}
              />
            </div>
            <div>
              <Label className="block mb-3">Lastname</Label>
              <Input
                type="text"
                placeholder="Lastname"
                onChange={(e) => setLastName(e.target.value)}
                className="w-full"
                defaultValue={lastName}
              />
            </div>
          </div>
          <div className="grid sm:grid-cols-2 gap-8">
            <div>
              <Label className="block mb-3">Username</Label>
              <Input
                type="text"
                placeholder="Username"
                onChange={(e) => setUsername(e.target.value)}
                className="w-full"
                defaultValue={username}
              />
            </div>
            <div>
              <Label className="block mb-3">Email</Label>
              <Input
                type="email"
                placeholder="Email address"
                onChange={(e) => setEmail(e.target.value)}
                className="w-full"
                defaultValue={email}
              />
            </div>
          </div>
          <Button type="submit">Update</Button>
        </form>
      </section>
    </>
  );
}
