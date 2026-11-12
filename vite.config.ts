import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { copyFileSync } from 'node:fs';
import { normalizeBase } from './scripts/base';
export default defineConfig({base:normalizeBase(process.env.VITE_BASE_PATH),plugins:[react(),{name:'pages-fallback',closeBundle(){copyFileSync('dist/index.html','dist/404.html');}}],build:{target:'es2022'}});
