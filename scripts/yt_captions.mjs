import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  
  // Set a normal user agent
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36');

  await page.goto('https://www.youtube.com/watch?v=DkDEDHL0dn0', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));
  
  // Dump the full page and search for key data
  const html = await page.content();
  
  // Search for various patterns
  const patterns = [
    [/"lengthSeconds":"(\d+)"/, 'lengthSeconds'],
    [/"approxDurationMs":"(\d+)"/, 'approxDurationMs'],
    [/"shortDescription":"((?:[^"\\]|\\.)*)"/s, 'description'],
    [/"captionTracks":\[(.*?)\]/s, 'captions'],
    [/"title":"((?:[^"\\]|\\.)*)"/, 'title'],
  ];
  
  for (const [pat, name] of patterns) {
    const m = html.match(pat);
    if (m) {
      let val = m[1];
      if (name === 'lengthSeconds') {
        const s = parseInt(val);
        console.log(`${name}: ${val}s = ${Math.floor(s/3600)}h ${Math.floor((s%3600)/60)}m ${s%60}s`);
      } else if (name === 'approxDurationMs') {
        const s = parseInt(val) / 1000;
        console.log(`${name}: ${Math.floor(s/3600)}h ${Math.floor((s%3600)/60)}m ${Math.floor(s%60)}s`);
      } else if (name === 'description') {
        console.log(`${name}: ${val.replace(/\\n/g, '\n').substring(0, 2000)}`);
      } else {
        console.log(`${name}: ${val.substring(0, 500)}`);
      }
    } else {
      console.log(`${name}: NOT FOUND`);
    }
  }
  
  // Check if bot detection page
  if (html.includes('confirm you') || html.includes('bot')) {
    console.log('\n⚠️ YouTube bot detection triggered');
  }
  
  await browser.close();
})();
