import React from 'react';
import './Loading.css';

const Loading = () => {
    const pathDefinition = "M0 510H479.5L495 501L511 532.5L526.5 479L540 555.5L556 458.5L570.5 577L585.5 436L599.5 599L615 415L630 617.5L645 393.5L661 640.5L676 372.5L691.5 659.5L705.5 353L720.5 682L736.5 353L751 659.5L765 372.5L780 640.5L793.5 393.5L809 617.5L823.5 415L839 599L855 436L869.5 577L884.5 458.5L899.5 555.5L915.5 479L931.5 532.5L944 501L959 510H1439.5";

    return (
        <div className="loading-screen-container">
            <div className="loading-wave-wrapper">
                <svg 
                    viewBox="0 300 1440 420" 
                    fill="none" 
                    xmlns="http://www.w3.org/2000/svg"
                    className="loading-svg"
                >
                    <defs>
                        <linearGradient id="wave-gradient" x1="0" y1="0" x2="1440" y2="0" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stopColor= "var(--accent)" />
                            <stop offset="50%" stopColor="var(--accent)" />
                            <stop offset="100%" stopColor="var(--accent)" />
                        </linearGradient>
                    </defs>

                    {/* Underlying guide track */}
                    <path 
                        d={pathDefinition} 
                        className="wave-path-bg" 
                    />

                    {/* Infinite moving glowing pulse */}
                    <path 
                        d={pathDefinition} 
                        className="wave-path-glow" 
                    />
                </svg>
            </div>
        </div>
    );
};

export default Loading;