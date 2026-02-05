import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  
  // Go to academy page
  await page.goto('https://www.prompty.co.kr/academy', { waitUntil: 'networkidle2', timeout: 30000 });
  
  // Wait for the app to render
  await page.waitForSelector('div[style*="opacity"]', { timeout: 10000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 3000));
  
  // Click on 바이브 철학관 menu item
  const menuItems = await page.$$('text/바이브 철학관');
  if (menuItems.length > 0) {
    await menuItems[0].click();
    await new Promise(r => setTimeout(r, 2000));
  } else {
    // Try finding by text content
    await page.evaluate(() => {
      const els = [...document.querySelectorAll('*')];
      const target = els.find(el => el.textContent.includes('바이브 철학관') && el.offsetHeight > 0 && el.offsetHeight < 100);
      if (target) target.click();
    });
    await new Promise(r => setTimeout(r, 2000));
  }
  
  // Take screenshot
  await page.screenshot({ path: '/root/.openclaw/workspace/artifacts/vibe_screenshot.png', fullPage: false });
  
  // Also take full page
  await page.screenshot({ path: '/root/.openclaw/workspace/artifacts/vibe_screenshot_full.png', fullPage: true });
  
  console.log('Screenshots saved!');
  await browser.close();
})();
