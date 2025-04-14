import {contextBridge, ipcRenderer} from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  sendMessage: (message: string) => ipcRenderer.send('message', message)
})

contextBridge.exposeInMainWorld('electronAPI', {
  downloadFile: (url: string, filename: string) =>
      ipcRenderer.invoke('download-file', url, filename),
});