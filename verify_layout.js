const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Set viewport for mobile
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('file://' + process.cwd() + '/index.html');

  // Wait for Alpine to init
  await page.waitForSelector('.glass-capsule');

  // Initial state screenshot
  await page.screenshot({ path: 'verify_initial.png' });

  // Check large animation overlay
  await page.evaluate(() => {
    window.Alpine.store('qimamEngine').showLargeAnim = true;
  });
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'verify_large_anim.png' });

  // Navigate to next section to trigger another large anim
  for(let i=0; i<5; i++) {
    await page.click('button:has-text("السؤال التالي")');
    await page.waitForTimeout(100);
  }
  await page.screenshot({ path: 'verify_section_transition.png' });

  await browser.close();
})();
