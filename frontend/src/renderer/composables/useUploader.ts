import {uploadFile} from "../api/file";
import {FileMeta} from "../types/fileMeta";

export function useUploader() {
    const upload = async (file: File): Promise<FileMeta> => {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("visibility", "public");  // 之后可以区分权限

        const response = await uploadFile(formData);
        return response.data;
    };

    return {
        upload,
    };
}
