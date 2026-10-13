import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 正式本机演示由FastAPI托管dist，同源运行。dev仅辅助编辑页面。
export default defineConfig({ plugins: [vue()] })
