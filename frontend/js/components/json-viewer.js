const JsonViewer = {
    render(data) {
        if (!data) return '<div class="json-viewer">null</div>';
        const json = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
        const highlighted = this._highlight(json);
        return `<div class="json-viewer">${highlighted}</div>`;
    },

    _highlight(json) {
        return json.replace(/("(?:\\.|[^"\\])*")\s*:/g, '<span class="json-key">$1</span>:')
            .replace(/:\s*("(?:\\.|[^"\\])*")/g, ': <span class="json-string">$1</span>')
            .replace(/:\s*(\d+\.?\d*)/g, ': <span class="json-number">$1</span>')
            .replace(/:\s*(true|false)/g, ': <span class="json-boolean">$1</span>')
            .replace(/:\s*(null)/g, ': <span class="json-null">$1</span>');
    },
};
