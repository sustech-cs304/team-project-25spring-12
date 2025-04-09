function isElectron(): boolean {
    return !!(window && window.process && window.process.type);
}

async function downloadInBrowser(url: string, filename: string) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
}

export async function downloadFile(url: string, filename: string) {
    if (isElectron()) {
        await window.electronAPI.downloadFile(url, filename);
    } else {
        await downloadInBrowser(url, filename);
    }
}
