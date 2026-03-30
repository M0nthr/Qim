const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const filePath = 'file://' + path.resolve('index.html');

  // Desktop mode - Long Question
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto(filePath);

  await page.evaluate(() => {
    const app = window.Alpine.find(document.querySelector('[x-data]'));
    app.currentQ = 10; // Order section
  });
  await page.waitForTimeout(500);

  const sideNavVisible = await page.isVisible('.side-nav-btn');
  console.log('Side Nav Visible (Desktop Order):', sideNavVisible);
  await page.screenshot({ path: 'desktop_order_mode.png' });

  // Mobile mode
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(500);
  const footerVisible = await page.isVisible('.footer-hub');
  console.log('Mobile Footer Visible:', footerVisible);
  await page.screenshot({ path: 'mobile_mode.png' });

  await browser.close();
})();
