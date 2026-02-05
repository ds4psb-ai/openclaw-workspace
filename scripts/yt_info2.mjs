import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  
  // Intercept requests to find player response
  let playerResponse = null;
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('/youtubei/v1/player') || url.includes('/youtubei/v1/next')) {
      try {
        const json = await response.json();
        if (json.videoDetails) playerResponse = json;
      } catch(e) {}
    }
  });

  await page.goto('https://www.youtube.com/watch?v=DkDEDHL0dn0', { waitUntil: 'networkidle2', timeout: 30000 });
  
  // Click consent/cookie buttons if present
  try {
    await page.click('button[aria-label*="Accept"], button[aria-label*="agree"], #yDmH0d button');
  } catch(e) {}
  
  await new Promise(r => setTimeout(r, 5000));
  
  // Try clicking play
  try { await page.click('.ytp-large-play-button'); } catch(e) {}
  await new Promise(r => setTimeout(r, 2000));

  // Get page HTML and extract data
  const html = await page.content();
  
  // Look for duration in page source
  const durationMatch = html.match(/"lengthSeconds":"(\d+)"/);
  const descMatch = html.match(/"shortDescription":"((?:[^"\\]|\\.)*)"/);
  const chaptersMatch = html.match(/"chapterRenderer"(.*?)(?="chapterRenderer"|$)/g);
  
  console.log('Duration seconds:', durationMatch?.[1] || 'not found');
  
  if (durationMatch) {
    const s = parseInt(durationMatch[1]);
    console.log(`Duration: ${Math.floor(s/3600)}h ${Math.floor((s%3600)/60)}m ${s%60}s`);
  }
  
  if (descMatch) {
    const desc = descMatch[1].replace(/\\n/g, '\n').replace(/\\"/g, '"');
    console.log(`\nDescription:\n${desc.substring(0, 3000)}`);
  }
  
  // Also try subtitles/captions URL
  const captionsMatch = html.match(/"captionTracks":\[(.*?)\]/);
  if (captionsMatch) {
    console.log(`\nCaptions found: ${captionsMatch[1].substring(0, 500)}`);
  }
  
  if (playerResponse) {
    console.log('\nPlayer response found!');
    console.log('Duration:', playerResponse.videoDetails?.lengthSeconds);
  }
  
  await browser.close();
})();
