const DashboardPage = {
    async render(container) {
        const jobs = await API.get('/documents/jobs?page=1&page_size=5');

        const stats = { pending: 0, processing: 0, completed: 0, failed: 0 };
        jobs.items.forEach(j => {
            if (j.status === 'completed') stats.completed++;
            else if (j.status === 'failed') stats.failed++;
            else if (j.status === 'pending') stats.pending++;
            else stats.processing++;
        });

        container.innerHTML = `
            <div class="page-header">
                <h1>Дашборд</h1>
                <a href="#/upload" class="btn btn-primary">Загрузить документ</a>
            </div>

            <div class="grid grid-4 mb-4">
                <div class="card stat-card">
                    <div class="stat-value">${jobs.total}</div>
                    <div class="stat-label">Всего заданий</div>
                </div>
                <div class="card stat-card">
                    <div class="stat-value" style="color:var(--warning)">${stats.pending + stats.processing}</div>
                    <div class="stat-label">В обработке</div>
                </div>
                <div class="card stat-card">
                    <div class="stat-value" style="color:var(--success)">${stats.completed}</div>
                    <div class="stat-label">Завершено</div>
                </div>
                <div class="card stat-card">
                    <div class="stat-value" style="color:var(--danger)">${stats.failed}</div>
                    <div class="stat-label">Ошибки</div>
                </div>
            </div>

            <div class="card">
                <h3 class="mb-4">Последние задания</h3>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Статус</th>
                                <th>Тип</th>
                                <th>Файлы</th>
                                <th>Время</th>
                                <th>Дата</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${jobs.items.map(j => `
                                <tr style="cursor:pointer" onclick="location.hash='#/jobs/${j.id}'">
                                    <td>${StatusBadge.render(j.status)}</td>
                                    <td>${j.detected_type || '—'}</td>
                                    <td>${j.files.length} файл(ов)</td>
                                    <td>${j.processing_time_ms ? (j.processing_time_ms / 1000).toFixed(1) + 's' : '—'}</td>
                                    <td class="text-muted">${new Date(j.created_at).toLocaleString('ru')}</td>
                                </tr>
                            `).join('')}
                            ${jobs.items.length === 0 ? '<tr><td colspan="5" class="text-muted" style="text-align:center">Нет заданий</td></tr>' : ''}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    },
};
