import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        liquid: {
          orange: '#FF6B00',
          'orange-light': '#FF8533',
          'orange-dark': '#CC5500',
          black: '#000000',
          'gray-900': '#0A0A0A',
          'gray-800': '#1A1A1A',
          'gray-700': '#2A2A2A',
          'gray-600': '#3A3A3A',
          'gray-500': '#6B7280',
          'gray-400': '#9CA3AF',
          'gray-300': '#D1D5DB',
        },
      },
      backgroundImage: {
        'gradient-orange': 'linear-gradient(135deg, #FF6B00 0%, #FF8533 100%)',
      },
    },
  },
  plugins: [],
};

export default config;