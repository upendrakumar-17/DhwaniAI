import React from "react";
import { RxCross2 } from "react-icons/rx";
import "./Sidebar.css";

const Sidebar = ({ isOpen, onCloseSidebar }) => {
    return (
        <div className={`sidebar-container ${isOpen ? "open" : ""}`}>
            <div className="sidebar-header">
                <div>DhwaniAI</div>
                <div className="sidebar-close-button" onClick={onCloseSidebar}><RxCross2 /></div>
            </div>
            <div className="sidebar-body">
                <div>New Chat</div>
                <div>Chat 1</div>
                <div>Chat 2</div>
            </div>
            <div className="sidebar-footer">
                <div>MADE BY</div>
                <div>UPENDRA KUMAR</div>
            </div>
        </div>
    );
};

export default Sidebar;