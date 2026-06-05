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
        primary: {
          DEFAULT: "#1B4332",
          light: "#2D6A4F",
          dark: "#0D2B1F",
        },
        secondary: {
          DEFAULT: "#D4A853",
          light: "#E2BE7A",
          dark: "#B8872A",
        },
        accent: "#F8F5F0",
        dark: "#0D1B2A",
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
