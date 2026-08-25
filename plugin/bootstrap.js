var ZoteroCodexChat = {
    scope: null,
    rootURI: null,
};

function install() {}

async function startup({ id, version, rootURI }) {
    ZoteroCodexChat.rootURI = rootURI;
    ZoteroCodexChat.scope = {
        Zotero,
        Services,
        ChromeUtils,
        Cc,
        Ci,
    };
    Services.scriptloader.loadSubScript(
        rootURI + "content/vendor/katex/katex.min.js",
        ZoteroCodexChat.scope,
        "UTF-8"
    );
    Services.scriptloader.loadSubScript(
        rootURI + "content/main.js",
        ZoteroCodexChat.scope,
        "UTF-8"
    );
    await ZoteroCodexChat.scope.ZoteroCodexChatPlugin.startup({ id, version, rootURI });
}

async function onMainWindowLoad({ window }) {
    await ZoteroCodexChat.scope?.ZoteroCodexChatPlugin.onMainWindowLoad(window);
}

async function onMainWindowUnload({ window }) {
    await ZoteroCodexChat.scope?.ZoteroCodexChatPlugin.onMainWindowUnload(window);
}

async function shutdown({ id }, reason) {
    if (reason === APP_SHUTDOWN) {
        return;
    }
    await ZoteroCodexChat.scope?.ZoteroCodexChatPlugin.shutdown();
    ZoteroCodexChat.scope = null;
}

function uninstall() {}
