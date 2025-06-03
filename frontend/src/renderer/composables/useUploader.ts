import {uploadFile} from "../api/file";

export function useUploader() {
    const upload = async (file: File) => {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("visibility", "public");  // 之后可以区分权限

        return await uploadFile(formData);
    };

    return {
        upload,
    };
}
