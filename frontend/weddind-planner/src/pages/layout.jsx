import React, { useState } from 'react';
import { Outlet } from "react-router-dom";
import TopBar from "../components/TopBar";
import Sidebar from "../components/SideBar";

const Layout = () => {
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

    return (
        <div className="relative min-h-screen bg-gray-50">
            <TopBar 
                title="Dashboard" 
                onMenuToggle={toggleSidebar}
            />
            <Sidebar 
                isOpen={sidebarOpen} 
                onNavigate={() => {}}
            />
            <main className={`absolute top-16 right-0 bottom-0 overflow-y-auto p-6 transition-all duration-300 ease-in-out ${sidebarOpen ? 'left-80' : 'left-0 md:left-16'} ${!sidebarOpen && 'peer-hover:left-80'}`}>
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
