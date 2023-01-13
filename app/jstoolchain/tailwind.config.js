/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "../templates/*.html",
    "../accounts/templates/accounts/*.html",
    "../accounts/templates/registration/*.html",
    "../blog/templates/blog/*.html",
    "../profile/templates/profile/*.html",
  ],
  theme: {
    colors: {
      "seth-blue": {
        400: "#05386B",
        600: "#05056B",
      },
      teal: colors.teal,
      slate: colors.slate,
    },
    extend: {},
  },
  plugins: [require("@tailwindcss/typography")],
};
