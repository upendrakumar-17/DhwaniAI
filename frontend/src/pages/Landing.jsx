import React from "react";
import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

const Landing = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    return (
        <div>
            <Navbar onOpenSidebar={() => setIsSidebarOpen(true)} />
            <Sidebar isOpen={isSidebarOpen} onCloseSidebar={() => setIsSidebarOpen(false)} />
            <h1>Landing</h1>
        </div>
    );
};

export default Landing;