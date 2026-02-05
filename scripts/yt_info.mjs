import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });
  
  await page.goto('https://www.youtube.com/watch?v=DkDEDHL0dn0', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));
  
  // Extract info from the page
  const info = await page.evaluate(() => {
    // Try to get duration
    const durationEl = document.querySelector('.ytp-time-duration');
    const titleEl = document.querySelector('h1.ytd-watch-metadata yt-formatted-string, title');
    const descEl = document.querySelector('#description-text, #description');
    const chaptersEls = document.querySelectorAll('ytd-macro-markers-list-item-renderer');
    
    let chapters = [];
    chaptersEls.forEach(el => {
      const time = el.querySelector('#time')?.textContent?.trim();
      const title = el.querySelector('#details h4')?.textContent?.trim();
      if (time && title) chapters.push({ time, title });
    });
    
    // Get from meta tags
    const metaDuration = document.querySelector('meta[itemprop="duration"]')?.content;
    const metaTitle = document.querySelector('meta[name="title"]')?.content;
    const metaDesc = document.querySelector('meta[name="description"]')?.content;
    
    // Get from ytInitialPlayerResponse if available
    let playerData = null;
    try {
      const scripts = document.querySelectorAll('script');
      for (const s of scripts) {
        if (s.textContent.includes('ytInitialPlayerResponse')) {
          const match = s.textContent.match(/ytInitialPlayerResponse\s*=\s*({.*?});/);
          if (match) playerData = JSON.parse(match[1]);
        }
      }
    } catch(e) {}
    
    return {
      title: metaTitle || titleEl?.textContent?.trim(),
      duration: durationEl?.textContent || metaDuration,
      description: metaDesc || descEl?.textContent?.trim()?.substring(0, 3000),
      chapters,
      playerDuration: playerData?.videoDetails?.lengthSeconds,
      playerTitle: playerData?.videoDetails?.title,
    };
  });
  
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})();
