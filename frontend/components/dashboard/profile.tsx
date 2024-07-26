"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/auth";

export default function ProfileDetails() {
  const { loading, logoutUser, user, updateProfile, updatePassword } =
    useAuth();
  // const [username, setUsername] = useState<string>("");
  // const [email, setEmail] = useState<string>("");
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");
  const [oldPassword, setOldPassword] = useState<string>("");
  const [newPassword, setNewPassword] = useState<string>("");
  const [newPasswordConfirm, setNewPasswordConfirm] = useState<string>("");

  useEffect(() => {
    // setUsername(user?.user?.username);
    // setEmail(user?.user?.email);
    setFirstName(user?.user?.firstName);
    setLastName(user?.user?.lastName);
  }, [user]);

  // console.log(user);

  const handleProfileUpdate = async (e: any) => {
    e.preventDefault();
    updateProfile(firstName, lastName);
  };

  const handlePasswordUpdate = async (e: any) => {
    e.preventDefault();
    updatePassword(oldPassword, newPassword, newPasswordConfirm);
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
              {user?.user?.firstName} {user?.user?.lastName}
            </span>
          </div>
          <div>
            <span className="font-medium mr-2">Username:</span>
            <span className="text-sm text-muted-foreground">
              {user?.user?.username}
            </span>
          </div>
          <div>
            <span className="font-medium mr-2">Email:</span>
            <span className="text-sm text-muted-foreground">
              {user?.user?.email}
            </span>
          </div>
          <div className="mb-4">
            <span className="font-medium mr-2">Account created on:</span>
            <span className="text-sm text-muted-foreground">
              {new Date(user?.user?.date_joined).toLocaleString()}
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
          {/* <div className="grid sm:grid-cols-2 gap-8">
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
          </div> */}
          <Button disabled={loading} aria-disabled={loading} type="submit">
            {loading ? "Updating..." : "Update"}
          </Button>
        </form>
      </section>
      <section>
        <Separator />
        <div className="my-6">
          <h2 className="text-xl font-bold tracking-tight">Update password</h2>
          <p className="text-sm text-muted-foreground tracking-tight">
            Update your password here
          </p>
        </div>
        <form onSubmit={handlePasswordUpdate} className="space-y-8 px-1 w-full">
          <div className="grid sm:grid-cols-2 gap-8">
            <div>
              <Label className="block mb-3">Old password</Label>
              <Input
                type="password"
                placeholder="********"
                onChange={(e) => setOldPassword(e.target.value)}
                className="w-full"
                value={oldPassword}
                required
              />
            </div>
            <div>
              <Label className="block mb-3">New password</Label>
              <Input
                type="password"
                placeholder="********"
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full"
                value={newPassword}
                required
              />
            </div>
            <div>
              <Label className="block mb-3">Confirm new password</Label>
              <Input
                type="password"
                placeholder="********"
                onChange={(e) => setNewPasswordConfirm(e.target.value)}
                className="w-full"
                value={newPasswordConfirm}
                required
              />
            </div>
          </div>

          <Button disabled={loading} aria-disabled={loading} type="submit">
            {loading ? "Updating..." : "Update"}
          </Button>
          <Separator />
        </form>
        <Button
          onClick={logoutUser}
          variant="destructive"
          disabled={loading}
          aria-disabled={loading}
          type="submit"
          className="my-8"
        >
          {loading ? "Wait..." : "Logout"}
        </Button>
      </section>
    </>
  );
}
