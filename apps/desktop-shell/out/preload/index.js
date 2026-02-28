"use strict";
const electron = require("electron");
electron.contextBridge.exposeInMainWorld("electron", {
  setIgnoreMouseEvents: (ignore) => electron.ipcRenderer.send("set-ignore-mouse-events", ignore)
});
