import type {WidgetUnion} from "./widgets";

export interface Page {
    id: number;
    name: string;
    index: number;
    visible: boolean;
    widgets: WidgetUnion[];
}