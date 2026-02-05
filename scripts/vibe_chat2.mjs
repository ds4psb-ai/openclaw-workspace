import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  
  await page.goto('https://www.prompty.co.kr/academy', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));
  
  // Click 바이브 철학관 in sidebar
  await page.evaluate(() => {
    const els = [...document.querySelectorAll('div, span, p, a, button')];
    for (const el of els) {
      if (el.textContent.trim() === '바이브 철학관' && el.offsetHeight > 0 && el.offsetHeight < 60) {
        el.click();
        console.log('Clicked 바이브 철학관');
        break;
      }
    }
  });
  await new Promise(r => setTimeout(r, 2000));
  
  // Screenshot the vibe page
  await page.screenshot({ path: '/root/.openclaw/workspace/artifacts/vibe_page.png', fullPage: false });
  console.log('Vibe page screenshot saved');
  
  // Now try clicking the 열기 button and see where it goes
  const [newPage] = await Promise.all([
    new Promise(resolve => browser.once('targetcreated', async target => {
      const p = await target.page();
      resolve(p);
    })),
    page.evaluate(() => {
      const els = [...document.querySelectorAll('*')];
      const btn = els.find(el => el.textContent.includes('바이브 철학관 열기') && el.offsetHeight > 0 && el.offsetHeight < 80);
      if (btn) btn.click();
    })
  ]).catch(() => [null]);
  
  if (newPage) {
    await new Promise(r => setTimeout(r, 5000));
    const url = newPage.url();
    console.log('New tab URL:', url);
    await newPage.screenshot({ path: '/root/.openclaw/workspace/artifacts/vibe_aistudio.png', fullPage: false });
    console.log('AI Studio screenshot saved');
  } else {
    console.log('No new tab opened, checking current page...');
    // Maybe it navigated in same tab
    await new Promise(r => setTimeout(r, 3000));
    console.log('Current URL:', page.url());
    await page.screenshot({ path: '/root/.openclaw/workspace/artifacts/vibe_aistudio.png', fullPage: false });
  }
  
  await browser.close();
})();
