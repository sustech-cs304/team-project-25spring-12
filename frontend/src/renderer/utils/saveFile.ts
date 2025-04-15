/*
* 按照不同平台，将下载的文件（blob = response.data）保存到本地。
* */

function isElectron(): boolean {
    return !!(window && window.process && window.process.type);
}

function saveBlobInBrowser(blob: Blob, filename: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

async function saveBlobInElectron(blob: Blob, filename: string) {
    const arrayBuffer = await blob.arrayBuffer();
    await window.electronAPI.saveFile(arrayBuffer, filename);
}

export async function saveFile(blob: Blob, filename: string) {
    if (isElectron()) {
        await saveBlobInElectron(blob, filename);
    } else {
        saveBlobInBrowser(blob, filename);
    }
}