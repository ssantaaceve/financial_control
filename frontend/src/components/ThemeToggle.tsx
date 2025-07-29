import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';

const ThemeToggle: React.FC = () => {
  const { theme, toggleTheme, isDark } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className={`
        fixed top-4 right-4 z-50
        p-3 rounded-full shadow-lg
        transition-all duration-300 ease-in-out
        transform hover:scale-110 active:scale-95
        ${isDark 
          ? 'bg-white/20 backdrop-blur-sm border border-white/30 text-white hover:bg-white/30' 
          : 'bg-gray-800/20 backdrop-blur-sm border border-gray-300/30 text-gray-800 hover:bg-gray-800/30'
        }
      `}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
    >
      <div className="relative w-6 h-6 flex items-center justify-center">
        {/* Sol */}
        <SunIcon 
          className={`
            absolute w-6 h-6 transition-all duration-300 ease-in-out
            ${isDark 
              ? 'opacity-0 rotate-90 scale-0' 
              : 'opacity-100 rotate-0 scale-100'
            }
          `}
        />
        
        {/* Luna */}
        <MoonIcon 
          className={`
            absolute w-6 h-6 transition-all duration-300 ease-in-out
            ${isDark 
              ? 'opacity-100 rotate-0 scale-100' 
              : 'opacity-0 -rotate-90 scale-0'
            }
          `}
        />
      </div>
    </button>
  );
};

export default ThemeToggle; 