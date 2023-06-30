const os = require('os');
const { execSync } = require('child_process');
const { Builder, By } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
require('dotenv').config();

const makeLogin = async (link) => {
  const options = new chrome.Options();
  options.headless = false;
  const driver = new Builder().forBrowser('chrome').setChromeOptions(options).build();

  await driver.get(link);
  await new Promise((resolve) => {
    setTimeout(resolve, 20000);
  });

  return driver;
};

const enterConversation = async (driver, contact_name) => {
  const spanElement = await driver.findElement(By.xpath(`//span[@title='${contact_name}']`));
  await spanElement.click();
};

const searchBySpecificMessage = async (driver, message) => {
  let seconds_pass = 0;

  const findElement = async () => {
    try {
      await driver.findElement(By.xpath(`//span[.='${message}']`));
      console.log('Element found!');
      playSong('acorda_pedrinho.mp3');
    } catch {
      seconds_pass += 1;
      console.log(`Not Found. Waiting more... Total ${seconds_pass} seconds`);
      setTimeout(findElement, 1000);
    }
  };

  findElement();

  await new Promise((resolve) => {
    setTimeout(resolve, 30000);
  });

  driver.quit();
};

const playSong = (song_path) => {
  if (os.platform() === 'darwin') {
    // macOS
    execSync(`afplay ${song_path}`);
  } else if (os.platform().startsWith('win')) {
    // Windows
    execSync(`start ${song_path}`);
  } else if (os.platform().startsWith('linux')) {
    // Linux
    execSync(`xdg-open ${song_path}`);
  } else {
    console.log('Unsupported platform. Cannot play song.');
  }
};

(async () => {
  const link = 'https://web.whatsapp.com/';
  const contact_name = process.env.CONTACT_NAME;

  const driver = await makeLogin(link);
  await enterConversation(driver, contact_name);
  await searchBySpecificMessage(driver, '.');
})();
