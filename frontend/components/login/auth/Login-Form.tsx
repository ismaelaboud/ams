"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
// import { useRouter } from "next/router"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email({
    message: "Please enter a valid email address.",
  }),
  password: z.string().min(8, {
    message: "Password must be at least 8 characters.",
  }),
})

export function LoginForm() {
  // const router = useRouter()
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  const onSubmit = (data: z.infer<typeof formSchema>) => {
    console.log(data)
  }

  return (
    <div className="w-full max-w-md mx-auto bg-white shadow-md rounded-lg p-6 relative">
      <button
        type="button"
        className="absolute top-4 left-4 text-blue-500"
        // onClick={() => router.push('/dashboard')}
      >
        Back
      </button>
      <div className="mt-8">
        
      
        <h2 className ="text-3xl font-bold "> Login </h2>
        <p className= "mb-4 text-muted-foreground">Enter your credentials to login</p>
      
      
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder="example@example.com" {...field} />
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
          <div className="flex flex-col items-center space-y-4">
            <Button type="submit" className="w-full">Login</Button>
            <div className="flex justify-center mt-4">
            <button
                type="button"
                className="text-blue-500 ml-4"
                // onClick={() => router.push('/forgot-password')}
              >
                Forgot Password?
              </button>
            </div>
          </div>
        </form>
      </Form>
      </div>
    </div>
  )
}
