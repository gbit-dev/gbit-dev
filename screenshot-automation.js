const playwright = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const projects = [
  {
    name: 'React-Glass-Calculator',
    repo: 'https://github.com/gbit-dev/React-Glass-Calculator.git',
    port: 5173,
    command: 'npm install && npm run dev',
    screenshots: ['screenshot1.png', 'screenshot2.png'],
    waitTime: 5000
  },
  {
    name: 'interactive-todo-list',
    repo: 'https://github.com/gbit-dev/interactive-todo-list.git',
    port: null,
    command: 'start with live-server',
    screenshots: ['screenshot1.png', 'screenshot2.png'],
    waitTime: 3000
  },
  {
    name: 'lumina-agency',
    repo: 'https://github.com/gbit-dev/lumina-agency.git',
    port: 5173,
    command: 'npm install && npm run dev',
    screenshots: ['screenshot1.png', 'screenshot2.png'],
    waitTime: 6000
  },
  {
    name: 'modern-landing-page',
    repo: 'https://github.com/gbit-dev/modern-landing-page.git',
    port: null,
    command: 'start with live-server',
    screenshots: ['screenshot1.png', 'screenshot2.png'],
    waitTime: 3000
  },
  {
    name: 'nova-studios',
    repo: 'https://github.com/gbit-dev/nova-studios.git',
    port: 5173,
    command: 'npm install && npm run dev',
    screenshots: ['screenshot1.png', 'screenshot2.png'],
    waitTime: 6000
  },
  {
    name: 'portfolio-website',
    repo: 'https://github.com/gbit-dev/portfolio-website.git',
    port: 5173,
    command: 'npm install && npm run dev',
    screenshots: ['screenshot1.png', 'screenshot2.png'],
    waitTime: 7000
  },
  {
    name: 'projeto-clima-js',
    repo: 'https://github.com/gbit-dev/projeto-clima-js.git',
    port: null,
    command: 'start with live-server',
    screenshots: ['screenshot1.png', 'screenshot2.png'],
    waitTime: 4000
  }
];

(async () => {
  const browser = await playwright.chromium.launch({ headless: false });
  
  for (const project of projects) {
    console.log(`\n📸 Processing ${project.name}...`);
    
    try {
      // Clone repository
      if (!fs.existsSync(project.name)) {
        console.log(`Cloning ${project.name}...`);
        execSync(`git clone ${project.repo} ${project.name}`);
      }
      
      // Install and run
      console.log(`Starting server for ${project.name}...`);
      const startTime = Date.now();
      
      const context = await browser.newContext({
        viewport: { width: 1440, height: 900 }
      });
      
      const page = await context.newPage();
      
      // Navigate to localhost
      let url = `http://localhost:${project.port || 8080}`;
      if (!project.port) {
        url = `http://localhost:8000`;
      }
      
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.waitForTimeout(project.waitTime);
      
      // Take screenshots
      console.log(`Taking screenshots for ${project.name}...`);
      
      // Screenshot 1 - Full page
      await page.screenshot({ 
        path: `${project.name}/public/screenshot-1.png`,
        fullPage: false
      });
      
      // Scroll and take screenshot 2
      await page.evaluate(() => {
        window.scrollBy(0, window.innerHeight);
      });
      await page.waitForTimeout(1000);
      
      await page.screenshot({ 
        path: `${project.name}/public/screenshot-2.png`,
        fullPage: false
      });
      
      await context.close();
      
      console.log(`✅ Screenshots saved for ${project.name}`);
      
    } catch (error) {
      console.error(`❌ Error processing ${project.name}:`, error.message);
    }
  }
  
  await browser.close();
  console.log('\n✨ All screenshots completed!');
})();
