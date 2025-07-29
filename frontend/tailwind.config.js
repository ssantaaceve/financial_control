/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'mono': ['Roboto Mono', 'monospace'],
      },
      colors: {
        'main-bg': 'var(--main-bg)',
        'text-color': 'var(--text-color)',
        'card-bg': 'var(--card-bg)',
        'border-color': 'var(--border-color)',
      },
      backgroundColor: {
        'main-bg': 'var(--main-bg)',
        'card-bg': 'var(--card-bg)',
      },
      textColor: {
        'text-color': 'var(--text-color)',
      },
      borderColor: {
        'border-color': 'var(--border-color)',
      },
    },
  },
  plugins: [],
} 