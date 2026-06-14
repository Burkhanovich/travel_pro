/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./apps/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        // Brand palette — Unitur blue & orange (approved pattern)
        primary: {
          DEFAULT: "#4F91C6",
          light: "#8CB7D9",
          dark: "#3B7AAD",
        },
        secondary: {
          DEFAULT: "#F4733D",
          light: "#F89B72",
          dark: "#D85F2C",
        },
        accent: "#EFF4F9",
        dark: "#1D2939",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        serif: ["Playfair Display", "ui-serif", "Georgia", "serif"],
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
      boxShadow: {
        soft: "0 4px 24px rgba(0,0,0,0.06)",
        card: "0 8px 40px rgba(0,0,0,0.08)",
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme("colors.gray.700"),
            a: {
              color: theme("colors.primary.DEFAULT"),
              "&:hover": { color: theme("colors.primary.light") },
            },
            h2: {
              fontFamily: '"Playfair Display", serif',
              color: theme("colors.dark"),
            },
            h3: {
              fontFamily: '"Playfair Display", serif',
              color: theme("colors.primary.DEFAULT"),
            },
          },
        },
      }),
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
  ],
};
