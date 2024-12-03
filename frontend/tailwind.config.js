/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // ここにカスタムテーマの設定を追加できます
      colors: {
        // カスタムカラーの追加例
        primary: {
          light: '#4da6ff',
          DEFAULT: '#0066cc',
          dark: '#004d99',
        },
      },
      spacing: {
        // カスタムスペーシングの追加例
        '128': '32rem',
      },
    },
  },
  plugins: [],
}
