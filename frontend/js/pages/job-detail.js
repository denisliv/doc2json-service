const JobDetailPage = {
    _pollTimer: null,

    async render(container, params) {
        this._stopPolling();
        await this._load(container, params.id);
    },

    async _load(container, jobId) {
        const job = await API.get(`/documents/jobs/${jobId}`);

        container.innerHTML = `
            <div class="page-header">
                <h1>Задание</h1>
                <div class="flex gap-2">
                    ${job.status === 'completed' || job.status === 'failed' ? `
                        <button class="btn btn-outline" id="btn-retry">Повторить</button>
                    ` : ''}
                    ${Auth.hasRole('manager') ? `
                        <button class="btn btn-danger btn-sm" id="btn-delete">Удалить</button>
                    ` : ''}
                    <a href="#/jobs" class="btn btn-outline">Назад</a>
                </div>
            </div>

            <div class="grid grid-2 mb-4">
                <div class="card">
                    <h3 class="mb-2">Информация</h3>
                    <table>
                        <tr><td class="text-muted">Статус</td><td>${StatusBadge.render(job.status)}</td></tr>
                        <tr><td class="text-muted">Тип документа</td><td>${job.detected_type || '—'}</td></tr>
                        <tr><td class="text-muted">Валидность</td><td>${job.is_valid === null ? '—' : (job.is_valid ? '✓ Валиден' : '✗ Не валиден')}</td></tr>
                        <tr><td class="text-muted">Время обработки</td><td>${job.processing_time_ms ? (job.processing_time_ms / 1000).toFixed(1) + ' сек' : '—'}</td></tr>
                        <tr><td class="text-muted">Создано</td><td>${new Date(job.created_at).toLocaleString('ru')}</td></tr>
                        ${job.completed_at ? `<tr><td class="text-muted">Завершено</td><td>${new Date(job.completed_at).toLocaleString('ru')}</td></tr>` : ''}
                    </table>
                </div>
                <div class="card">
                    <h3 class="mb-2">Файлы (${job.files.length})</h3>
                    <ul class="file-list">
                        ${job.files.map(f => `
                            <li class="file-item">
                                <span>📄 ${f.name} (${f.size ? (f.size / 1024).toFixed(1) + ' KB' : '—'})</span>
                                <a href="/api/v1/documents/jobs/${jobId}/files/${f.id}" target="_blank" class="btn btn-sm btn-outline">Скачать</a>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>

            ${job.error_message ? `<div class="alert alert-error mb-4">${job.error_message}</div>` : ''}

            ${job.validation_errors ? `
                <div class="card mb-4">
                    <h3 class="mb-2">Ошибки валидации</h3>
                    <table>
                        <thead><tr><th>Путь</th><th>Ошибка</th></tr></thead>
                        <tbody>
                            ${(Array.isArray(job.validation_errors) ? job.validation_errors : []).map(e => `
                                <tr><td><code>${e.path}</code></td><td>${e.message}</td></tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            ` : ''}

            ${job.extracted_json ? `
                <div class="card">
                    <div class="flex-between mb-2">
                        <h3>Результат JSON</h3>
                        <div class="flex gap-2">
                            <button class="btn btn-sm btn-outline" id="btn-copy">Копировать</button>
                            <button class="btn btn-sm btn-outline" id="btn-download">Скачать</button>
                        </div>
                    </div>
                    ${JsonViewer.render(job.extracted_json)}
                </div>
            ` : ''}
        `;

        // Polling for in-progress jobs
        if (StatusBadge.isProcessing(job.status)) {
            this._pollTimer = setTimeout(() => this._load(container, jobId), 3000);
        }

        // Retry button
        document.getElementById('btn-retry')?.addEventListener('click', async () => {
            await API.post(`/documents/jobs/${jobId}/retry`);
            this._load(container, jobId);
        });

        // Delete button
        document.getElementById('btn-delete')?.addEventListener('click', async () => {
            if (!confirm('Удалить задание?')) return;
            await API.del(`/documents/jobs/${jobId}`);
            window.location.hash = '#/jobs';
        });

        // Copy JSON
        document.getElementById('btn-copy')?.addEventListener('click', () => {
            navigator.clipboard.writeText(JSON.stringify(job.extracted_json, null, 2));
        });

        // Download JSON
        document.getElementById('btn-download')?.addEventListener('click', () => {
            const blob = new Blob([JSON.stringify(job.extracted_json, null, 2)], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `result-${jobId}.json`;
            a.click();
        });
    },

    _stopPolling() {
        if (this._pollTimer) {
            clearTimeout(this._pollTimer);
            this._pollTimer = null;
        }
    },
};
