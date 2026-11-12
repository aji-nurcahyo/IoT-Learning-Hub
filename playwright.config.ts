import { defineConfig, devices } from '@playwright/test';
import { normalizeBase } from './scripts/base';
const base=normalizeBase(process.env.VITE_BASE_PATH),port=Number(process.env.IOT_QA_PORT||4173);
export default defineConfig({testDir:'tests/browser',timeout:30000,fullyParallel:false,workers:1,reporter:'list',use:{baseURL:`http://127.0.0.1:${port}${base}`,screenshot:'only-on-failure',trace:'retain-on-failure'},projects:[{name:'desktop',use:{...devices['Desktop Chrome'],channel:'chrome',viewport:{width:1440,height:1000}}},{name:'mobile',use:{...devices['Pixel 7'],channel:'chrome',viewport:{width:390,height:844}}}],webServer:{command:`npm run preview -- --port ${port} --strictPort`,url:`http://127.0.0.1:${port}${base}`,reuseExistingServer:false}});
