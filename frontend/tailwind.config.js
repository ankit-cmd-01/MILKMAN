/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#8B1E2D",
        primaryDark: "#6F1824",
        lightBlue: "#38BDF8",
        lightBlueDark: "#0EA5E9",
        lightBrown: "#C4A484",
        textPrimary: "#000000",
        textSecondary: "#333333",
      },
      borderRadius: {
        xl: "0.75rem",
      },
    },
  },
  plugins: [],
}
