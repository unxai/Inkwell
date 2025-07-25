/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'inkwell-blue': '#1A365D',
        'inkwell-teal': '#4FD1C5',
      },
      fontFamily: {
        sans: ['Source Sans Pro', 'Noto Sans SC', 'sans-serif'],
      },
    },
  },
  plugins: [],
}