// Fixed realistic desktop Chrome user-agent (less strict CORS)
const fingerprint = {
    vendor: "Google",
    renderer: "ANGLE (Intel)",
    userAgent:
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    language: "en-US",
};

// Sembunyikan automation markers
Object.defineProperty(navigator, "webdriver", {
    get: () => false,
});

// Override toString untuk hide Proxy
const handler = {
    get: (target, prop) => {
        if (prop === "toString") {
            return () => "[object Object]";
        }
        return Reflect.get(target, prop);
    },
};
new Proxy(navigator, handler);

// Tambah fake plugins
Object.defineProperty(navigator, "plugins", {
    get: () => [
        { name: "Chrome PDF Plugin", description: "Portable Document Format" },
        { name: "Chrome PDF Viewer", description: "Portable Document Format" },
        {
            name: "Native Client Executable",
            description: "Native Client Executable",
        },
    ],
});

// Set languages dengan fixed fingerprint
Object.defineProperty(navigator, "languages", {
    get: () => [fingerprint.language, "en"],
});

// Set userAgent dengan fixed fingerprint
Object.defineProperty(navigator, "userAgent", {
    get: () => fingerprint.userAgent,
});

// Set platform
Object.defineProperty(navigator, "platform", {
    get: () => "Win32",
});

// Set maxTouchPoints (Desktop tidak ada touch)
Object.defineProperty(navigator, "maxTouchPoints", {
    get: () => 0,
});

// Set deviceMemory
Object.defineProperty(navigator, "deviceMemory", {
    get: () => 8,
});

// Set hardwareConcurrency
Object.defineProperty(navigator, "hardwareConcurrency", {
    get: () => 4,
});

// Chrome runtime
window.chrome = {
    runtime: {},
    app: {},
    loadTimes: function () {},
    csi: function () {},
};

// Add window properties (Desktop 1920x1080)
Object.defineProperty(window, "outerWidth", {
    get: () => 1920,
});

Object.defineProperty(window, "outerHeight", {
    get: () => 1080,
});

Object.defineProperty(window, "innerWidth", {
    get: () => 1903,
});

Object.defineProperty(window, "innerHeight", {
    get: () => 987,
});

// Hide offscreenBuffering
window.offscreenBuffering = true;

// Spoof screen properties (Desktop 1920x1080)
Object.defineProperty(screen, "width", {
    get: () => 1920,
});

Object.defineProperty(screen, "height", {
    get: () => 1080,
});

Object.defineProperty(screen, "availWidth", {
    get: () => 1920,
});

Object.defineProperty(screen, "availHeight", {
    get: () => 1040,
});

Object.defineProperty(screen, "colorDepth", {
    get: () => 24,
});

Object.defineProperty(screen, "pixelDepth", {
    get: () => 24,
});

// Sembunyikan headless detection
const originalQuery = window.matchMedia;
window.matchMedia = function (query) {
    if (query === "(prefers-color-scheme: dark)") {
        return {
            matches: false,
            media: query,
            onchange: null,
            addListener: () => {},
            removeListener: () => {},
            addEventListener: () => {},
            removeEventListener: () => {},
            dispatchEvent: () => true,
        };
    }
    return originalQuery(query);
};

// Override permission
if (navigator.permissions && navigator.permissions.query) {
    const originalQuery2 = navigator.permissions.query;
    navigator.permissions.query = (parameters) =>
        parameters.name === "notifications"
            ? Promise.resolve({ state: Notification.permission })
            : originalQuery2(parameters);
}

// WebGL Spoofing dengan random fingerprint
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function (parameter) {
    if (parameter === 37445) {
        return fingerprint.vendor;
    }
    if (parameter === 37446) {
        return fingerprint.renderer;
    }
    return getParameter(parameter);
};

// WebGL2 Spoofing dengan random fingerprint
const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
WebGL2RenderingContext.prototype.getParameter = function (parameter) {
    if (parameter === 37445) {
        return fingerprint.vendor;
    }
    if (parameter === 37446) {
        return fingerprint.renderer;
    }
    return getParameter2(parameter);
};

// Canvas fingerprinting protection
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function (type) {
    if (type === "image/png" || type === "image/jpeg") {
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==";
    }
    return originalToDataURL.apply(this, arguments);
};

// Canvas fingerprinting protection untuk getImageData
const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
CanvasRenderingContext2D.prototype.getImageData = function () {
    const imageData = originalGetImageData.apply(this, arguments);
    // Modifikasi pixel data untuk avoid fingerprinting
    for (let i = 0; i < imageData.data.length; i += 4) {
        imageData.data[i] = Math.floor(Math.random() * 256); // Red
        imageData.data[i + 1] = Math.floor(Math.random() * 256); // Green
        imageData.data[i + 2] = Math.floor(Math.random() * 256); // Blue
    }
    return imageData;
};

// Expose reCAPTCHA callbacks untuk debugging
window.__recaptchaDebug = {
    onLoad: () => {
        console.log("✅ reCAPTCHA loaded");
    },
    onError: () => {
        console.log("❌ reCAPTCHA error");
    },
};

// Override reCAPTCHA callback
window.grecaptchaReady = true;
if (window.grecaptcha) {
    const originalExecute = window.grecaptcha.execute;
    window.grecaptcha.execute = function (...args) {
        console.log("🤖 grecaptcha.execute called", args);
        return originalExecute.apply(this, args);
    };
}
