const FileUpload = {
    _files: [],

    render(containerId) {
        this._files = [];
        return `
            <div class="upload-zone" id="${containerId}-zone">
                <div style="font-size:2rem">📄</div>
                <p><strong>Перетащите PDF файлы сюда</strong></p>
                <p class="text-sm text-muted">или нажмите для выбора</p>
                <input type="file" id="${containerId}-input" multiple accept=".pdf" style="display:none">
            </div>
            <ul class="file-list" id="${containerId}-list"></ul>
        `;
    },

    init(containerId) {
        const zone = document.getElementById(`${containerId}-zone`);
        const input = document.getElementById(`${containerId}-input`);
        if (!zone || !input) return;

        zone.addEventListener('click', () => input.click());
        zone.addEventListener('dragover', (e) => { e.preventDefault(); zone.classList.add('dragover'); });
        zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            this._addFiles(containerId, e.dataTransfer.files);
        });
        input.addEventListener('change', () => {
            this._addFiles(containerId, input.files);
            input.value = '';
        });
    },

    _addFiles(containerId, fileList) {
        for (const f of fileList) {
            if (f.type === 'application/pdf' && !this._files.some(x => x.name === f.name)) {
                this._files.push(f);
            }
        }
        this._renderList(containerId);
    },

    _renderList(containerId) {
        const list = document.getElementById(`${containerId}-list`);
        if (!list) return;
        list.innerHTML = this._files.map((f, i) => `
            <li class="file-item">
                <span>📄 ${f.name} (${(f.size / 1024).toFixed(1)} KB)</span>
                <span class="remove" data-idx="${i}">&times;</span>
            </li>
        `).join('');
        list.querySelectorAll('.remove').forEach(btn => {
            btn.addEventListener('click', () => {
                this._files.splice(parseInt(btn.dataset.idx), 1);
                this._renderList(containerId);
            });
        });
    },

    getFiles() {
        return this._files;
    },

    clear() {
        this._files = [];
    },
};
