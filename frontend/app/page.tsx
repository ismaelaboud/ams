import { Button } from "@/components/ui/button";
import { LoginForm } from "@/components/login/auth/Login-Form";
export default function Home() {
  return (
    <main className="grid place-items-center h-screen p-24">
      <LoginForm />
      <Button>Contribute</Button>
    </main>
  );
}
