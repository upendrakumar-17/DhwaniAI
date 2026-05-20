import React from "react";
import { MdMenu } from "react-icons/md";
import { FaUser } from "react-icons/fa";
import { CiMenuKebab } from "react-icons/ci";
import "./Navbar.css";


const Navbar = ({ onOpenSidebar }) => {
    return (
        <>
            <div className="navbar-container">
                <div className="navbar-left">
                    <div className="navbar-button sidebar-open-button" onClick={onOpenSidebar}><MdMenu /></div>
                    <div className="navbar-link"> DhwaniAI</div>
                </div>
                <div className="navbar-right">
                    <div className="navbar-link" ><FaUser /></div>
                    <div className="navbar-button"><CiMenuKebab /></div>
                </div>
            </div>
            
        </>
    );
};

export default Navbar;