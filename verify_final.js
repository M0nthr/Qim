
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 800 });

  await page.goto('file://' + process.cwd() + '/index.html');

  // Wait for initial load
  await page.waitForTimeout(1000);

  // Go to question 5 (Matching - Long Mode)
  await page.evaluate(() => {
    window.qimam.currentQuestion = 4;
    window.qimam.renderQuestion();
  });
  await page.waitForTimeout(500);
  await page.screenshot({ path: '/home/jules/verification/long_mode_check.png' });

  // Trigger burst manually to capture it
  await page.evaluate(() => {
    window.qimam.showBurst(0); // TF icon
  });
  await page.waitForTimeout(300); // Wait for animation to be visible
  await page.screenshot({ path: '/home/jules/verification/burst_capture.png' });

  await browser.close();
})();
