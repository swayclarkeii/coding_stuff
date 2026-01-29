// Step 1: Navigate to Invoice database and get initial snapshot
console.log('Navigating to Invoice database...');
await page.goto('https://www.notion.so/2f41c288bb28814aa434e23b9c714d3c');
await page.waitForLoadState('networkidle');
await page.waitForTimeout(2000);

console.log('Getting page snapshot...');
const snapshot = await accessibilitySnapshot({ page });
console.log(JSON.stringify(snapshot, null, 2));
