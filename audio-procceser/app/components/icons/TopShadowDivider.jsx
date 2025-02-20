export default function TopShadowDivider() {
    return (
        <svg width="100%" height="100%" viewBox="0 0 1280 140" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="fadeUp0" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="var(--top-divider-color, #999)" stopOpacity="0"></stop>
                    <stop offset="100%" stopColor="var(--top-divider-color, #999)"></stop>
                </linearGradient>
            </defs>
            <path d="M 0 0 L 0 140 L 1280 140 L 1280 0 Z" fill="url(#fadeUp0)"></path>
        </svg>
    );
}
