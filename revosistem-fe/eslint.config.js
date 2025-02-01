import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    languageOptions: {
      globals: globals.browser,
    },
    settings: {
      react: {
        version: "detect", // Deteksi otomatis versi React
      },
    },
    rules: {
      "react/react-in-jsx-scope": "off", // Tidak perlu impor React sejak React 17
    },
  },
  pluginJs.configs.recommended,
  pluginReact.configs.flat.recommended,
];
