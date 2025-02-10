export default function BottomShadowDivider() {
    return (
        <svg width="100%" height="100%" viewBox="0 0 1280 140" fill="none" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="fadeDown1" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="var(--bottom-divider-color, #fff)"></stop>
                    <stop offset="100%" stopColor="var(--bottom-divider-color, #fff)" stopOpacity="0"></stop>
                </linearGradient>
            </defs>
            <path d="M 0 0 L 0 140 L 1280 140 L 1280 0 Z" fill="url(#fadeDown1)"></path>
        </svg>
    );
    }
