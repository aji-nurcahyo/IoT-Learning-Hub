import { test, expect } from '@playwright/test';
test('beranda, theme, navigasi, pencarian, filter, dan chapter',async({page},info)=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('./');await expect(page.getByRole('heading',{name:'Internet of Things Learning Hub.'})).toBeVisible();
 await expect(page.locator('.level-card')).toHaveCount(4);await expect(page.locator('.track-card')).toHaveCount(5);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.getByLabel('Tema tampilan').selectOption('dark');await expect(page.locator('html')).toHaveAttribute('data-theme','dark');await page.reload();await expect(page.getByLabel('Tema tampilan')).toHaveValue('dark');
 await page.screenshot({path:`test-results/${info.project.name}-home-dark.png`,fullPage:true});
 await page.getByLabel('Tema tampilan').selectOption('light');await page.screenshot({path:`test-results/${info.project.name}-home-light.png`,fullPage:true});
 await page.getByLabel('Tema tampilan').selectOption('system');await page.emulateMedia({colorScheme:'dark'});expect(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor)).toBe('rgb(17, 27, 24)');
 await page.getByRole('link',{name:'Jelajahi kurikulum'}).click();await expect(page.locator('.chapter-row')).toHaveCount(40);
 await page.getByRole('searchbox').fill('MQTT');await expect(page.locator('.chapter-row')).toHaveCount(3);
 await page.getByRole('combobox',{name:'Level',exact:true}).selectOption('1');await expect(page.getByRole('heading',{name:'Belum ada chapter yang sesuai'})).toBeVisible();await page.getByRole('button',{name:'Reset filter'}).click();
 await page.getByRole('combobox',{name:'Ketersediaan',exact:true}).selectOption('available');await expect(page.locator('.chapter-row')).toHaveCount(20);await page.getByRole('combobox',{name:'Ketersediaan',exact:true}).selectOption('all');
 await page.getByRole('searchbox').fill('21');await page.locator('.chapter-row').click();await expect(page.getByRole('heading',{name:'IoT Data Models, Telemetry & Event Design'})).toBeVisible();await expect(page.locator('.resource-card a[download]')).toHaveCount(0);
 await page.locator('.chapter-nav a').last().click();await expect(page.getByRole('heading',{name:'Raspberry Pi, Linux & IoT Gateways'})).toBeVisible();
 await page.goBack();await expect(page.getByRole('heading',{name:'IoT Data Models, Telemetry & Event Design'})).toBeVisible();await page.reload();await expect(page.getByRole('heading',{name:'IoT Data Models, Telemetry & Event Design'})).toBeVisible();expect(errors).toEqual([]);
});
test('Getting Started, TOC, mode baca, download nyata, dan menu mobile',async({page},info)=>{
 await page.goto('./');if(info.project.name==='mobile')await page.getByRole('button',{name:'Buka navigasi'}).click();await page.getByRole('navigation',{name:'Navigasi utama'}).getByRole('link',{name:'Getting Started'}).click();
 await expect(page.locator('.prose table')).toHaveCount(2);await page.getByRole('button',{name:'Mode baca fokus'}).click();await expect(page.locator('.reading-grid aside')).toBeHidden();await page.getByRole('button',{name:'Keluar mode fokus'}).click();
 await page.getByRole('complementary',{name:'Daftar isi'}).getByRole('link',{name:'Troubleshooting',exact:true}).click();expect(page.url()).toContain('#/getting-started');
 for(const a of await page.locator('.downloads a').all()){const res=await page.request.get((await a.getAttribute('href'))!);expect(res.ok()).toBeTruthy();expect(res.headers()['content-type']).not.toContain('text/html');}
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);await page.screenshot({path:`test-results/${info.project.name}-reading.png`,fullPage:true});
});
test('template Markdown dan Reveal.js, fragment, math, code, notes, serta cleanup',async({page},info)=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('./#/templates');await expect(page.locator('.reveal')).toHaveClass(/ready/);
 await expect(page.locator('.reading-grid aside')).not.toContainText('Ini bukan heading daftar isi');await expect(page.locator('.prose .katex').first()).toBeVisible();await expect(page.locator('.prose pre code.hljs').first()).toBeVisible();await expect(page.locator('.prose table')).toHaveCount(2);
 await page.getByRole('button',{name:'Berikutnya →'}).click();await expect(page.locator('.reveal section.present h2')).toHaveText('Satu aliran, beberapa lapisan');await page.getByRole('button',{name:'Berikutnya →'}).click();await expect(page.locator('.reveal .fragment')).toHaveClass(/visible/);
 await page.getByRole('button',{name:'Berikutnya →'}).click();await expect(page.locator('.reveal section.present pre code')).toBeVisible();await page.getByRole('button',{name:'Berikutnya →'}).click();await expect(page.locator('.reveal section.present .katex')).toBeVisible();
 await page.getByRole('button',{name:'Catatan presenter'}).click();await expect(page.locator('.deck-area .notice')).toContainText('KaTeX');await page.screenshot({path:`test-results/${info.project.name}-slides.png`,fullPage:true});
 if(info.project.name==='mobile')await page.getByRole('button',{name:'Buka navigasi'}).click();await page.getByRole('navigation',{name:'Navigasi utama'}).getByRole('link',{name:'Beranda',exact:true}).click();await expect(page.locator('.reveal')).toHaveCount(0);expect(errors).toEqual([]);
});
test('tracks, batas chapter, dan halaman tidak ditemukan',async({page})=>{
 await page.goto('./#/tracks');await page.locator('.track-card').first().click();await expect(page.getByRole('heading',{name:'Rencana topik'})).toBeVisible();await page.locator('.chapter-row').first().click();await expect(page.getByRole('heading',{name:'Tujuan pembelajaran'})).toBeVisible();
 await page.goto('./#/chapter/1');await expect(page.locator('.chapter-nav a')).toHaveCount(1);await page.goto('./#/chapter/40');await expect(page.locator('.chapter-nav a')).toHaveCount(1);
 await page.goto('./#/chapter/1/reading');await expect(page.locator('.prose h1')).toContainText('Chapter 01');await page.locator('.prose img').scrollIntoViewIfNeeded();await expect(page.locator('.prose img')).toBeVisible();
 await page.goto('./#/chapter/10/slides');await expect(page.locator('.reveal')).toHaveClass(/ready/);await expect(page.locator('.reveal section.present h2')).toContainText('Capstone');
 await page.goto('./#/chapter/20/slides');await expect(page.locator('.reveal')).toHaveClass(/ready/);await expect(page.locator('.reveal section.present h2')).toContainText('Capstone');
 await page.goto('./#/chapter/10/exercises');await expect(page.locator('.prose h1')).toContainText('Latihan Bertingkat');
 await page.goto('./#/chapter/21/reading');await expect(page.getByRole('heading',{name:'Materi belum tersedia'})).toBeVisible();await page.goto('./#/unknown');await expect(page.getByRole('heading',{name:'Halaman tidak ditemukan.'})).toBeVisible();
});
