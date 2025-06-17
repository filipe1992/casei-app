const withMT = require("@material-tailwind/react/utils/withMT");

module.exports = withMT({
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#fce7f3',
          DEFAULT: '#ec4899',
          dark: '#be185d',
        },
        secondary: {
          light: '#f3e8ff',
          DEFAULT: '#a855f7',
          dark: '#7e22ce',
        },
        accent: {
          light: '#dbeafe',
          DEFAULT: '#3b82f6',
          dark: '#1d4ed8',
        }
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
})