import { app, shell, BrowserWindow, ipcMain } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'

const ORB_API = 'http://127.0.0.1:7777/v1/orb/state'

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 160,
        height: 170,
        show: false,
        autoHideMenuBar: true,
        transparent: true,  // Important for floating orb
        frame: false,       // No title bar
        alwaysOnTop: true,  // HUD always on top
        hasShadow: false,
        resizable: false,
        webPreferences: {
            preload: join(__dirname, '../preload/index.js'),
            sandbox: false,
            contextIsolation: true
        }
    })

    // Allow mouse events so -webkit-app-region: drag works for repositioning

    mainWindow.on('ready-to-show', () => {
        // Don't auto-show - orb visibility is controlled by JARVIS state
    })

    // Poll orb state: show when visible, hide when not
    let pollInterval
    mainWindow.webContents.on('did-finish-load', () => {
        pollInterval = setInterval(async () => {
            try {
                const res = await fetch(ORB_API)
                const data = await res.json()
                if (data.visible) {
                    if (!mainWindow.isVisible()) mainWindow.show()
                } else {
                    if (mainWindow.isVisible()) mainWindow.hide()
                }
            } catch {
                mainWindow.hide()
            }
        }, 400)
    })
    mainWindow.on('closed', () => {
        if (pollInterval) clearInterval(pollInterval)
    })

    mainWindow.webContents.setWindowOpenHandler((details) => {
        shell.openExternal(details.url)
        return { action: 'deny' }
    })

    if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
        mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
    } else {
        mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
    }

    // Handle IPC to allow click-through testing
    ipcMain.on('set-ignore-mouse-events', (event, ignore) => {
        const win = BrowserWindow.fromWebContents(event.sender)
        win.setIgnoreMouseEvents(ignore, { forward: true })
    })
}

app.whenReady().then(() => {
    electronApp.setAppUserModelId('com.jarvis.orb')
    app.on('browser-window-created', (_, window) => {
        optimizer.watchWindowShortcuts(window)
    })
    createWindow()
    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})
