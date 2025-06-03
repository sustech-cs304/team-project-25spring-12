import {downloadFile} from "../api/file";
import {saveFile} from "../utils/saveFile";
import {FileMeta} from "../types/fileMeta";

export function useDownloader() {
    const getFile = async (file: FileMeta) => {
        const response = await downloadFile(file.id);
        return response.data;  // 获取到的文件信息
    }

    const download = async (file: FileMeta)=> {
        const blob = await getFile(file);
        await saveFile(blob, file.filename);  // 保存到本地
    };

    return {
        getFile,
        download,
    };
}