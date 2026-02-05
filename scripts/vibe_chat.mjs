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
  await new Promise(r => setTimeout(r, 3000));
  
  // Click 바이브 철학관
  await page.evaluate(() => {
    const els = [...document.querySelectorAll('*')];
    const target = els.find(el => el.textContent.includes('바이브 철학관') && el.offsetHeight > 0 && el.offsetHeight < 100);
    if (target) target.click();
  });
  await new Promise(r => setTimeout(r, 2000));
  
  // Click "바이브 철학관 열기" button
  await page.evaluate(() => {
    const els = [...document.querySelectorAll('*')];
    const target = els.find(el => el.textContent.includes('바이브 철학관 열기') && el.offsetHeight > 0 && el.offsetHeight < 80);
    if (target) target.click();
  });
  await new Promise(r => setTimeout(r, 3000));
  
  // Take screenshot to see current state
  await page.screenshot({ path: '/root/.openclaw/workspace/artifacts/vibe_step1.png', fullPage: false });
  console.log('Step 1 screenshot saved');
  
  // Look for input fields and fill in persona info
  const pageContent = await page.content();
  console.log('Page has input:', pageContent.includes('<input'));
  console.log('Page has textarea:', pageContent.includes('<textarea'));
  
  // Try to find and fill input fields
  const inputs = await page.$$('input[type="text"], input:not([type]), textarea');
  console.log('Found inputs:', inputs.length);
  
  for (let i = 0; i < inputs.length; i++) {
    const placeholder = await inputs[i].evaluate(el => el.placeholder || el.getAttribute('aria-label') || '');
    console.log(`Input ${i}: placeholder="${placeholder}"`);
  }
  
  // Try filling name field
  const nameInput = await page.$('input[placeholder*="이름"], input[placeholder*="name"], input[placeholder*="닉네임"]');
  if (nameInput) {
    await nameInput.type('소미');
    console.log('Typed name');
  }
  
  // Look for chat input
  const chatInput = await page.$('input[placeholder*="메시지"], input[placeholder*="입력"], textarea[placeholder*="메시지"], textarea[placeholder*="입력"], textarea');
  if (chatInput) {
    await chatInput.type('안녕하세요! 저는 소미입니다. 26살이고 AI와 테크놀로지에 관심이 많아요.');
    await page.keyboard.press('Enter');
    console.log('Sent chat message');
    await new Promise(r => setTimeout(r, 3000));
  }
  
  await page.screenshot({ path: '/root/.openclaw/workspace/artifacts/vibe_step2.png', fullPage: false });
  console.log('Step 2 screenshot saved');
  
  await browser.close();
})();
