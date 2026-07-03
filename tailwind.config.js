/**
 * ⚠️ DEPRECATED — NOT USED.
 *
 * The project runs Tailwind CSS v4 with a CSS-first config in
 * `tailwind_src/input.css` (@theme, @source, @plugin). This JS config is
 * ignored by the build (there is no `@config` directive in input.css).
 *
 * All values below already live in input.css @theme; the old `typography`
 * h2/h3 Playfair overrides were ported to the `.prose` rules at the bottom of
 * input.css. Kept only for historical reference — safe to delete.
 *
 * @type {import('tailwindcss').Config}
 */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./apps/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        // APPROVED brand palette — blue + yellow
        primary: {
          DEFAULT: "#4497CB",
          light: "#B4D2E8",
          dark: "#2B7BAD",
        },
        secondary: {
          DEFAULT: "#FFB81C",
          light: "#FFB81C",
          dark: "#D89A0E",
        },
        accent: "#E4F0F9",
        dark: "#1D2939",
        // Official brand namespace
        brand: {
          blue: "#4497CB",
          blueDark: "#2B7BAD",
          blueLight: "#B4D2E8",
          bluePale: "#E4F0F9",
          yellow: "#FFB81C",
          yellowDark: "#D89A0E",
          yellowPale: "#FFF6E0",
          gold: "#B8860B",
          ink: "#1D2939",
          ctaBg: "#3E6C8F",
          ctaLine: "#ECB456",
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
