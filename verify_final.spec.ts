import { test, expect } from '@playwright/test';

test('verify assessment and adaptive footer', async ({ page }) => {
  await page.goto('file://' + process.cwd() + '/index.html');
  await page.setViewportSize({ width: 1280, height: 800 });

  // Check identity info
  const identity = page.locator('.identity-info');
  await expect(identity).toBeVisible();

  // Move to question 9 (Order - long question type)
  await page.evaluate(() => {
    const app = (window as any).Alpine.find(document.querySelector('[x-data]'));
    app.currentQ = 9;
  });

  await page.waitForTimeout(500);

  // Check if side-nav-btn is visible (desktop + long question)
  const sideNav = page.locator('.side-nav-btn');
  await expect(sideNav).toBeVisible();

  // Take screenshot of desktop long question mode
  await page.screenshot({ path: 'desktop_long_q.png' });

  // Check mobile mode
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(500);

  // Footer hub should be visible and not transparent
  const footerHub = page.locator('.footer-hub');
  await expect(footerHub).toBeVisible();
  const bgColor = await footerHub.evaluate(el => window.getComputedStyle(el).backgroundColor);
  console.log('Mobile Footer BG:', bgColor);

  await page.screenshot({ path: 'mobile_footer.png' });
});
