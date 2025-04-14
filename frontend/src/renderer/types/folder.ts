export interface FolderPageItem {
    id: number;
    name: string;
}

export interface Folder {
    id: number;
    index: number;
    name: string;
    visible: boolean;
    pages: FolderPageItem[];
}