import { Button } from "@/components/ui/button";

const Home = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <header className="bg-white shadow-md py-4">
        <div className="container mx-auto px-6 flex justify-between items-center">
          <h1 className="text-3xl font-semibold text-gray-800">Asset Management</h1>
          <nav>
            <ul className="flex space-x-6 text-lg">
              <li><a href="#" className="text-gray-700 hover:text-gray-900">Home</a></li>
              <li><a href="#" className="text-gray-700 hover:text-gray-900">About</a></li>
              
              <li><Button className="text-white">Sign Up</Button></li>
              <li><Button className="text-white">Sign In</Button></li>
            </ul>
          </nav>
        </div>
      </header>

      <section className="flex-grow flex flex-col items-center justify-center text-center p-8">
        <h2 className="text-5xl font-bold mb-6 text-gray-800">Welcome to Asset Management System</h2>
        <p className="text-xl mb-10 text-gray-600">Manage your assets efficiently and effectively with our top-notch solutions.</p>
        <Button className="px-6 py-3 text-lg bg-blue-600 text-white hover:bg-blue-700">Get Started</Button>
      </section>

      <footer className="bg-white shadow-inner py-4">
        <div className="container mx-auto px-6 text-center text-gray-600">
          <p>&copy; 2024 Asset Management. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
