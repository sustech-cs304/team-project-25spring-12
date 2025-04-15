import {uploadFile as apiUploadFile} from "../api/file";
import {FileMeta} from "../types/fileMeta";

export function useUploader() {
    const upload = async (file: File): Promise<FileMeta> => {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("visibility", "");

        const response = await apiUploadFile(formData);
        return response.data;
    };

    return {
        upload,
    };
}
