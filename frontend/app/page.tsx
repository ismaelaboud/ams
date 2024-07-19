import { Button } from "@/components/ui/button";
import  RegistrationForm from "@/components/Registration/RegistrationForm";

export default function Home() {
  return (
    <main className="grid place-items-center h-screen p-24">
      <RegistrationForm />

      <Button>Contribute</Button>

    </main>
  );
}
