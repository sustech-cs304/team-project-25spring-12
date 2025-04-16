// 根据文件后缀返回对应的 Element Plus 图标
import {Box, Document, Folder, Headset, Picture, Tools, VideoCamera} from "@element-plus/icons-vue";

export const getFileIcon = (filename: string) => {
    const ext = filename.split(".").pop()?.toLowerCase();
    if (["zip", "apk", "rar", "7z", "tar", "gz", "bz2", "xz"].includes(ext || "")) return Box;
    if (["exe", "bat", "sh", "jar", "msi", "app", "com", "vbs"].includes(ext || "")) return Tools;
    if (["png", "jpg", "jpeg", "gif", "svg"].includes(ext || "")) return Picture;
    if (["mp4", "avi", "mkv", "mov"].includes(ext || "")) return VideoCamera;
    if (["pdf", "doc", "docx", "txt", "md"].includes(ext || "")) return Document;
    if (["mp3", "wav", "flac", "aac"].includes(ext || "")) return Headset;
    return Folder;
};