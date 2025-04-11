export const setProperty = (prop: string, val: any, dom = document.documentElement) => {
    dom.style.setProperty(prop, val);
};

export const mix = (color1: string, color2: string, weight: number = 0.5): string => {
    let color = '#';
    for (let i = 0; i <= 2; i++) {
        const c1 = parseInt(color1.substring(1 + i * 2, 3 + i * 2), 16);
        const c2 = parseInt(color2.substring(1 + i * 2, 3 + i * 2), 16);
        const c = Math.round(c1 * weight + c2 * (1 - weight));
        color += c.toString(16).padStart(2, '0');
    }
    return color;
};

/*
* AI generated
* 这段代码由 DeepSeek 生成，我要求它使用哈希算法，用courseCode动态生成一个颜色
* 来美化 DDL 日历、课程卡片等外观表现。
* */
export function getCourseColor(courseCode: string): string {
    // 哈希函数 - 将字符串转换为哈希值
    const hash = stringToHash(courseCode)

    // 使用哈希值生成HSL颜色
    const hue = hash % 360  // 色调 (0-359)
    const saturation = 70 + (hash % 15)  // 饱和度 (70-85%)
    const lightness = 50 + (hash % 10)  // 明度 (50-60%)

    return `hsl(${hue}, ${saturation}%, ${lightness}%)`
}

// 辅助函数：将字符串转换为稳定的哈希值
function stringToHash(str: string): number {
    let hash = 0
    if (str.length === 0) return hash

    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i)
        hash = ((hash << 5) - hash) + char
        hash = hash & hash // 转换为32位整数
    }

    return Math.abs(hash)
}

// 辅助函数：根据背景色决定文字颜色（确保可读性）
export function getTextColor(bgColor: string): string {
    // 如果是HSL颜色，提取亮度值
    if (bgColor.startsWith('hsl')) {
        const lightnessMatch = bgColor.match(/[\d.]+(?=%\))/)
        if (lightnessMatch) {
            const lightness = parseFloat(lightnessMatch[0])
            return lightness > 60 ? '#333' : '#fff'
        }
    }
    return '#fff' // 默认返回白色文字
}