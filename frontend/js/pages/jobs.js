const JobsPage = {
    _page: 1,
    _status: '',

    async render(container) {
        this._page = 1;
        this._status = '';
        await this._load(container);
    },

    async _load(container) {
        const params = new URLSearchParams({ page: this._page, page_size: 20 });
        if (this._status) params.set('status', this._status);

        const data = await API.get(`/documents/jobs?${params}`);
        const totalPages = Math.ceil(data.total / data.page_size) || 1;

        container.innerHTML = `
            <div class="page-header">
                <h1>Задания</h1>
                <a href="#/upload" class="btn btn-primary">Новое задание</a>
            </div>

            <div class="card mb-4">
                <div class="flex gap-2">
                    <select id="filter-status" class="form-control" style="width:auto">
                        <option value="">Все статусы</option>
                        <option value="pending" ${this._status === 'pending' ? 'selected' : ''}>Ожидание</option>
                        <option value="completed" ${this._status === 'completed' ? 'selected' : ''}>Завершено</option>
                        <option value="failed" ${this._status === 'failed' ? 'selected' : ''}>Ошибка</option>
                    </select>
                </div>
            </div>

            <div class="card">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Статус</th>
                                <th>Тип</th>
                                <th>Файлы</th>
                                <th>Валидность</th>
                                <th>Время</th>
                                <th>Дата создания</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.items.map(j => `
                                <tr style="cursor:pointer" onclick="location.hash='#/jobs/${j.id}'">
                                    <td>${StatusBadge.render(j.status)}</td>
                                    <td>${j.detected_type || '—'}</td>
                                    <td>${j.files.length}</td>
                                    <td>${j.is_valid === null ? '—' : (j.is_valid ? '✓' : '✗')}</td>
                                    <td>${j.processing_time_ms ? (j.processing_time_ms / 1000).toFixed(1) + 's' : '—'}</td>
                                    <td class="text-muted">${new Date(j.created_at).toLocaleString('ru')}</td>
                                </tr>
                            `).join('')}
                            ${data.items.length === 0 ? '<tr><td colspan="6" class="text-muted" style="text-align:center">Нет заданий</td></tr>' : ''}
                        </tbody>
                    </table>
                </div>

                ${totalPages > 1 ? `
                    <div class="pagination">
                        <button ${this._page <= 1 ? 'disabled' : ''} data-page="${this._page - 1}">←</button>
                        <span class="text-sm text-muted" style="padding:6px 12px">${this._page} / ${totalPages}</span>
                        <button ${this._page >= totalPages ? 'disabled' : ''} data-page="${this._page + 1}">→</button>
                    </div>
                ` : ''}
            </div>
        `;

        document.getElementById('filter-status')?.addEventListener('change', (e) => {
            this._status = e.target.value;
            this._page = 1;
            this._load(container);
        });

        container.querySelectorAll('.pagination button').forEach(btn => {
            btn.addEventListener('click', () => {
                this._page = parseInt(btn.dataset.page);
                this._load(container);
            });
        });
    },
};
