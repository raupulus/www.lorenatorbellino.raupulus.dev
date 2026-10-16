/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{html,js}"
  ],
  theme: {
    extend: {
      colors: {
        torbellino: {
          coral: "#F87157",
          peach: "#FCD499",
          plum: "#3F173B",
          wine: "#78364D",
          red: "#DC2626",
          denim: "#4A7499",
          mint: "#B1CAB2",
          lilac: "#CAA5D9",
          cream: "#FFF9F5",
          sand: "#F3E2D8",
          dark: "#241424"
        }
      },
      fontFamily: {
        sans: [
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          '"Helvetica Neue"',
          'Arial',
          'sans-serif'
        ]
      }
    },
  },
  plugins: [],
}
