/* global document, Zotero */

var ZoteroCodexChatPreferences = {
    prefix: "extensions.zotero-codex-chat.",
    defaults: {
        defaultLanguage: "zh-CN",
        tone: "academic",
        generalPrompt: "",
        fontSize: "13",
        webSearchMode: "live",
    },
    strings: {
        "zh-CN": {
            title: "Paper Chat for Zotero",
            description: "这些设置会自动保存；对话规则从下一条提问开始生效。",
            language: "默认回答语言",
            languageOptions: ["跟随提问语言", "简体中文", "English", "日本語", "Deutsch", "Français", "Español", "한국어"],
            tone: "风格与语气",
            toneOptions: ["学术严谨", "简洁直接", "教学讲解", "批判分析"],
            webSearch: "联网检索",
            webSearchOptions: ["实时联网（推荐）", "仅使用缓存索引", "关闭联网检索"],
            webSearchHelp: "用于查询当前论文之外的网页和厂商资料；本地文件仍保持只读。修改后从下一次提问开始生效。",
            fontSize: "界面字体大小",
            prompt: "通用 Prompt / 固定规则",
            placeholder: "例如：先给出一句话结论；比较方法时必须列出证据所在页码；遇到不确定内容时明确标注。",
            help: "这里适合填写长期偏好。当前论文路径、只读安全约束和用户本次问题仍会由插件自动添加。",
            reset: "恢复默认",
            saved: "设置已自动保存",
            restored: "已恢复默认设置",
        },
        en: {
            title: "Paper Chat for Zotero",
            description: "Settings are saved automatically; conversation rules apply from the next question.",
            language: "Default response language",
            languageOptions: ["Follow the question language", "简体中文", "English", "日本語", "Deutsch", "Français", "Español", "한국어"],
            tone: "Style and tone",
            toneOptions: ["Academic and rigorous", "Concise and direct", "Tutorial", "Critical analysis"],
            webSearch: "Web search",
            webSearchOptions: ["Live web search (recommended)", "Cached search index only", "Disable web search"],
            webSearchHelp: "Retrieves web and vendor sources outside the current paper; local files remain read-only. Changes apply from the next question.",
            fontSize: "Interface font size",
            prompt: "General prompt / persistent rules",
            placeholder: "For example: start with a one-sentence conclusion; cite page numbers when comparing methods; clearly mark uncertainty.",
            help: "Use this for long-term preferences. The current paper, read-only safety rules, and your current question are still added automatically.",
            reset: "Restore defaults",
            saved: "Settings saved automatically",
            restored: "Default settings restored",
        },
    },

    locale() {
        const requested = Zotero.Prefs.get("intl.locale.requested", true) || Zotero.locale || "en-US";
        return /^zh(?:-|$)/i.test(requested) ? "zh-CN" : "en";
    },

    get(name) {
        const value = Zotero.Prefs.get(this.prefix + name, true);
        return value === undefined || value === null ? this.defaults[name] : value;
    },

    set(name, value) {
        Zotero.Prefs.set(this.prefix + name, String(value), true);
        try {
            globalThis.Services?.prefs?.savePrefFile(null);
        } catch (error) {}
    },

    applyLocale(doc) {
        const strings = this.strings[this.locale()];
        doc.getElementById("zcc-pref-title").textContent = strings.title;
        doc.getElementById("zcc-pref-description").textContent = strings.description;
        doc.getElementById("zcc-pref-language-label").textContent = strings.language;
        [...doc.getElementById("zcc-pref-language").options].forEach((option, index) => {
            option.textContent = strings.languageOptions[index];
        });
        doc.getElementById("zcc-pref-tone-label").textContent = strings.tone;
        [...doc.getElementById("zcc-pref-tone").options].forEach((option, index) => {
            option.textContent = strings.toneOptions[index];
        });
        doc.getElementById("zcc-pref-web-search-label").textContent = strings.webSearch;
        [...doc.getElementById("zcc-pref-web-search").options].forEach((option, index) => {
            option.textContent = strings.webSearchOptions[index];
        });
        doc.getElementById("zcc-pref-web-search-help").textContent = strings.webSearchHelp;
        doc.getElementById("zcc-pref-font-size-label").textContent = strings.fontSize;
        doc.getElementById("zcc-pref-prompt-label").textContent = strings.prompt;
        doc.getElementById("zcc-pref-prompt").placeholder = strings.placeholder;
        doc.getElementById("zcc-pref-help").textContent = strings.help;
        doc.getElementById("zcc-pref-reset").textContent = strings.reset;
    },

    init(doc) {
        const root = doc.getElementById("zcc-preferences");
        if (!root) return;
        this.applyLocale(doc);
        const language = doc.getElementById("zcc-pref-language");
        const tone = doc.getElementById("zcc-pref-tone");
        const webSearch = doc.getElementById("zcc-pref-web-search");
        const fontSize = doc.getElementById("zcc-pref-font-size");
        const fontSizeValue = doc.getElementById("zcc-pref-font-size-value");
        const prompt = doc.getElementById("zcc-pref-prompt");
        const status = doc.getElementById("zcc-pref-status");
        const strings = this.strings[this.locale()];
        const showSaved = () => {
            status.textContent = strings.saved;
        };
        const updateFontSizeValue = () => {
            fontSizeValue.textContent = `${fontSize.value} px`;
        };
        const load = () => {
            language.value = this.get("defaultLanguage");
            tone.value = this.get("tone");
            webSearch.value = this.get("webSearchMode");
            fontSize.value = this.get("fontSize");
            updateFontSizeValue();
            prompt.value = this.get("generalPrompt");
            showSaved();
        };

        if (root.dataset.initialized !== "true") {
            root.dataset.initialized = "true";
            language.addEventListener("change", () => {
                this.set("defaultLanguage", language.value);
                showSaved();
            });
            tone.addEventListener("change", () => {
                this.set("tone", tone.value);
                showSaved();
            });
            webSearch.addEventListener("change", () => {
                this.set("webSearchMode", webSearch.value);
                showSaved();
            });
            fontSize.addEventListener("input", () => {
                this.set("fontSize", fontSize.value);
                updateFontSizeValue();
                showSaved();
            });
            prompt.addEventListener("input", () => {
                this.set("generalPrompt", prompt.value);
                showSaved();
            });
            doc.getElementById("zcc-pref-reset").addEventListener("click", () => {
                for (const [name, value] of Object.entries(this.defaults)) this.set(name, value);
                load();
                status.textContent = strings.restored;
            });
            doc.defaultView.addEventListener("pagehide", () => {
                this.set("defaultLanguage", language.value);
                this.set("tone", tone.value);
                this.set("webSearchMode", webSearch.value);
                this.set("fontSize", fontSize.value);
                this.set("generalPrompt", prompt.value);
            });
        }
        load();
    },
};

(function initializePreferences() {
    let attempts = 0;
    const run = () => {
        if (document.getElementById("zcc-preferences")) {
            ZoteroCodexChatPreferences.init(document);
            return;
        }
        if (attempts++ < 20) document.defaultView.setTimeout(run, 25);
    };
    run();
    document.defaultView.addEventListener("pageshow", run);
})();
