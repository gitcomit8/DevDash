/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        primary: "#1E3A8A" /* Muted blue */,
        "primary-dark": "#172554" /* Darker blue for hover */,
        secondary: "#64748B" /* Muted gray-blue */,
        accent: "#10B981" /* Teal accent */,
      },
    },
  },
  plugins: [],
};
