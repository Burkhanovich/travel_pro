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
        // Brand palette — Unitur deep blue & orange (darkened)
        primary: {
          DEFAULT: "#2E6DA4",
          light: "#6BA1CD",
          dark: "#1F4F77",
        },
        secondary: {
          DEFAULT: "#EC6A33",
          light: "#F4733D",
          dark: "#C8521F",
        },
        accent: "#EAF1F8",
        dark: "#16202E",
        // Official brand namespace (matches primary/secondary)
        brand: {
          blue: "#2E6DA4",
          blueDark: "#1F4F77",
          blueLight: "#6BA1CD",
          orange: "#EC6A33",
          orangeDark: "#C8521F",
          ink: "#16202E",
        },
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
