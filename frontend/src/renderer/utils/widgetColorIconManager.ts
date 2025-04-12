export type WidgetType = 'doc' | 'assignment' | 'notepdf' | string;

export interface WidgetStyle {
    icon: string;
    color: 'red' | 'green' | 'blue' | 'purple' | 'orange' | 'teal' | 'gray';
}

const widgetStyleMap: Record<WidgetType, WidgetStyle> = {
    doc: {
        icon: 'Document',
        color: 'green',
    },
    assignment: {
        icon: 'Notebook',
        color: 'orange',
    },
    notepdf: {
        icon: 'DataAnalysis',
        color: 'blue',
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
    },
    bodyColor: {
        red: '#FEE2E2',
        green: '#D1FAE5',
        blue: '#DBEAFE',
        purple: '#EDE9FE',
        orange: '#FFEDD5',
        teal: '#CCFBF1',
        gray: '#E5E7EB',
    },
};

export function getWidgetStyle(type: WidgetType): WidgetStyle {
    return widgetStyleMap[type] ?? {
        icon: 'Box', // 默认图标
        color: 'gray',
    };
}

export function getHeaderColor(color: WidgetStyle['color']): string {
    return colorPalette.headerColor[color] || '#60A5FA';
}

export function getBodyColor(color: WidgetStyle['color']): string {
    return colorPalette.bodyColor[color] || '#DBEAFE';
}
