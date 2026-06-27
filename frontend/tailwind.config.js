/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#07111f",
        },
      },
      boxShadow: {
        soft: "0 20px 60px rgba(15, 23, 42, 0.35)",
      },
    },
  },
  plugins: [],
};

