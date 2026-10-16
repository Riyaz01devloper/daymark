const { app, BrowserWindow, shell, session } = require('electron');
const path = require('path');

let mainWindow = null;

// Ensure single instance of app
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  function createWindow() {
    mainWindow = new BrowserWindow({
      width: 1240,
      height: 820,
      minWidth: 850,
      minHeight: 600,
      title: 'Daymark — Make room for what matters',
      icon: path.join(__dirname, 'icon.ico'),
      backgroundColor: '#f5f6f2',
      autoHideMenuBar: true,
      webPreferences: {
        preload: path.join(__dirname, 'preload.cjs'),
        nodeIntegration: false,
        contextIsolation: true,
        spellcheck: true,
      },
    });

    // Ensure cross-origin requests to backend pass CORS without origin issues
    session.defaultSession.webRequest.onBeforeSendHeaders((details, callback) => {
      const url = details.url;
      if (url.includes('onrender.com')) {
        details.requestHeaders['Origin'] = 'https://daymark-gamma-red.vercel.app';
      }
      callback({ cancel: false, requestHeaders: details.requestHeaders });
    });

    // Load compiled application
    const indexPath = path.join(__dirname, '../dist/index.html');
    mainWindow.loadFile(indexPath);

    // Open target="_blank" or external links in user's standard default browser
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
      if (url.startsWith('http:') || url.startsWith('https:')) {
        shell.openExternal(url);
      }
      return { action: 'deny' };
    });

    mainWindow.on('closed', () => {
      mainWindow = null;
    });
  }

  app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
      }
    });
  });

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });
}

