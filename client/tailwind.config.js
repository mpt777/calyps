import { skeleton, contentPath } from "@skeletonlabs/skeleton/plugin";
import * as themes from "@skeletonlabs/skeleton/themes";
import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'selector',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,svelte}",
    contentPath(import.meta.url, "svelte"),
  ],
  theme: {
    extend: {},
  },
  plugins: [
    forms,
    skeleton({
      // NOTE: each theme included will increase the size of your CSS bundle
      themes: [themes.mona],
    }),
  ],
  safelist: [
    'bg-warning-500',
    "preset-filled-error-500",
    'preset-tonal-error',
  ]
};