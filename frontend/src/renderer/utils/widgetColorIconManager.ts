export type WidgetType = 'doc' | 'assignment' | 'notepdf' | 'folder' | string;

export interface WidgetStyle {
    icon: string;
    color: string;
}

const widgetStyleMap: Record<WidgetType, WidgetStyle> = {
    doc: {
        icon: 'Document',
        color: 'green',
    },
    assignment: {
        icon: 'Notebook',
        color: 'indigo',
    },
    notepdf: {
        icon: 'DataAnalysis',
        color: 'blue',
    },
    folder : {
        icon: 'FolderOpened',
        color: 'purple',
    },
};

/*
* AI generated
* 我用AI生成了若干推荐的前、背景色搭配，省略了手动调色的时间。
* */

const colorPalette = {
    headerColor: {
        red: '#F87171',
        green: '#34D399',
        blue: '#60A5FA',
        purple: '#A78BFA',
        orange: '#FB923C',
        teal: '#2DD4BF',
        gray: '#9CA3AF',
        sky: '#38BDF8',
        indigo: '#6366F1',
        navy: '#1E3A8A',
        sapphire: '#0F52BA',
        cobalt: '#3B82F6',
        steel: '#4682B4',
        slate: '#64748B',
        denim: '#1E40AF',
        turquoise: '#06B6D4',
        azure: '#1FB6FF'
    },
    bodyColor: {
        red: '#FEE2E2',
        green: '#D1FAE5',
        blue: '#DBEAFE',
        purple: '#EDE9FE',
        orange: '#FFEDD5',
        teal: '#CCFBF1',
        gray: '#E5E7EB',
        sky: '#E0F2FE',
        indigo: '#E0E7FF',
        navy: '#DBEAFE',
        sapphire: '#E0F2FF',
        cobalt: '#DBEAFE',
        steel: '#D6EAF8',
        slate: '#F1F5F9',
        denim: '#E0E7FF',
        turquoise: '#CFFAFE',
        azure: '#E0F7FF'
    }
}

export function getWidgetStyle(type: string): WidgetStyle {
    return widgetStyleMap[type] ?? {
        icon: 'Box', // 默认图标
        color: 'gray',
    };
}

export function getHeaderColor(color: string): string {
    return colorPalette.headerColor[color] || '#60A5FA';
}

export function getBodyColor(color: string): string {
    return colorPalette.bodyColor[color] || '#DBEAFE';
}
