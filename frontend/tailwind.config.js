
import daisyui from 'daisyui'
import typography from '@tailwindcss/typography'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [daisyui, typography],
  daisyui: {
    themes: ['cupcake', 'night', 'nord', 'emerald', 'retro', 'cyberpunk', 'valentine', 'halloween', 'garden', 'forest']
  }
}

