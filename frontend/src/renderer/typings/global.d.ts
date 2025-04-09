export {};

declare global {
    interface Window {
        electronAPI: {
            downloadFile: (url: string, filename: string) => Promise<void>;
        };
    }
}
