const DocTypesPage = {
    async render(container) {
        const types = await API.get('/document-types');

        container.innerHTML = `
            <div class="page-header">
                <h1>Типы документов</h1>
                ${Auth.hasRole('admin') ? '<a href="#/doc-types/new" class="btn btn-primary">Создать тип</a>' : ''}
            </div>

            <div class="card">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Название</th>
                                <th>Slug</th>
                                <th>Статус</th>
                                <th>Версия</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            ${types.map(t => `
                                <tr>
                                    <td><strong>${t.name}</strong>${t.description ? `<br><span class="text-sm text-muted">${t.description}</span>` : ''}</td>
                                    <td><code>${t.slug}</code></td>
                                    <td>${t.is_active ? '<span class="badge badge-completed">Активен</span>' : '<span class="badge badge-failed">Неактивен</span>'}</td>
                                    <td>v${t.version}</td>
                                    <td class="text-right">
                                        ${Auth.hasRole('admin') ? `<a href="#/doc-types/${t.slug}" class="btn btn-sm btn-outline">Редактировать</a>` : `<a href="#/doc-types/${t.slug}" class="btn btn-sm btn-outline">Просмотр</a>`}
                                    </td>
                                </tr>
                            `).join('')}
                            ${types.length === 0 ? '<tr><td colspan="5" class="text-muted" style="text-align:center">Нет типов документов</td></tr>' : ''}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    },
};
