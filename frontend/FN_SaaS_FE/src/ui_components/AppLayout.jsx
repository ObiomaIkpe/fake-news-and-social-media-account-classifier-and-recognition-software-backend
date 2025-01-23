import { Outlet } from "react-router-dom";
import Footer from "./Footer";
import { ToastContainer } from "react-toastify";
import NavBar from "./NavBar";
import { useEffect, useState } from "react";

const AppLayout = ({isAuthenticated, username, setIsAuthenticated, setUsername}) => {

    useEffect(function() {
        if(localStorage.getItem("dark") === null){
          localStorage.setItem("dark", "false")
        }
      }, []);

    const [darkMode, setDarkMode] = useState(localStorage.getItem("dark") === 'true');   

    const handleDarkMode = () => {
        const newDarkMode = !darkMode
        setDarkMode(newDarkMode)
        localStorage.setItem("dark", newDarkMode ? "true" : "false")
    }
    
  return (
    <div className={darkMode ? "dark" : ""}>
    <main className="w-full bg-[#ffffff] dark:bg-[#181A2A]">
      <NavBar  
      darkMode={darkMode} 
      handleDarkMode={handleDarkMode} 
      username={username}
      isAuthenticated={isAuthenticated}
      setIsAuthenticated={setIsAuthenticated}
      setUsername={setUsername}
      />
      <ToastContainer />
      <Outlet />
      <Footer />
    </main>
    </div>
  );
};

export default AppLayout;