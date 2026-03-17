const DocTypeEditorPage = {
    async render(container, params) {
        const isNew = params.slug === 'new';
        let dt = null;
        let plugins = [];

        try { plugins = await API.get('/document-types/plugins'); } catch { /* ignore */ }

        if (!isNew) {
            dt = await API.get(`/document-types/${params.slug}`);
        }

        const mdPlugins = plugins.filter(p => p.type === 'markdown');
        const jsonPlugins = plugins.filter(p => p.type === 'json');

        container.innerHTML = `
            <div class="page-header">
                <h1>${isNew ? 'Новый тип документа' : `Редактирование: ${dt.name}`}</h1>
                <a href="#/doc-types" class="btn btn-outline">Назад</a>
            </div>

            <form id="dt-form">
                <div class="grid grid-2 mb-4">
                    <div class="card">
                        <h3 class="mb-4">Основные данные</h3>
                        <div class="form-group">
                            <label>Slug</label>
                            <input type="text" id="dt-slug" class="form-control" value="${dt?.slug || ''}" ${!isNew ? 'readonly' : ''} required>
                        </div>
                        <div class="form-group">
                            <label>Название</label>
                            <input type="text" id="dt-name" class="form-control" value="${dt?.name || ''}" required>
                        </div>
                        <div class="form-group">
                            <label>Описание</label>
                            <input type="text" id="dt-description" class="form-control" value="${dt?.description || ''}">
                        </div>
                        <div class="form-group">
                            <label>Подсказки для роутера</label>
                            <input type="text" id="dt-hints" class="form-control" value="${dt?.router_hints || ''}">
                        </div>
                    </div>

                    <div class="card">
                        <h3 class="mb-4">Постобработчики</h3>
                        <div class="form-group">
                            <label>Markdown постобработчики</label>
                            ${mdPlugins.map(p => `
                                <label style="display:flex;align-items:center;gap:6px;margin-bottom:4px;font-weight:normal">
                                    <input type="checkbox" class="md-plugin" value="${p.name}"
                                        ${(dt?.markdown_postprocessors || []).includes(p.name) ? 'checked' : ''}>
                                    ${p.name} <span class="text-sm text-muted">— ${p.description}</span>
                                </label>
                            `).join('')}
                            ${mdPlugins.length === 0 ? '<p class="text-sm text-muted">Нет доступных плагинов</p>' : ''}
                        </div>
                        <div class="form-group">
                            <label>JSON постобработчики</label>
                            ${jsonPlugins.map(p => `
                                <label style="display:flex;align-items:center;gap:6px;margin-bottom:4px;font-weight:normal">
                                    <input type="checkbox" class="json-plugin" value="${p.name}"
                                        ${(dt?.json_postprocessors || []).includes(p.name) ? 'checked' : ''}>
                                    ${p.name} <span class="text-sm text-muted">— ${p.description}</span>
                                </label>
                            `).join('')}
                            ${jsonPlugins.length === 0 ? '<p class="text-sm text-muted">Нет доступных плагинов</p>' : ''}
                        </div>
                    </div>
                </div>

                <div class="card mb-4">
                    <h3 class="mb-4">JSON Schema</h3>
                    <textarea id="dt-schema" class="form-control" style="min-height:200px">${dt ? JSON.stringify(dt.json_schema, null, 2) : '{}'}</textarea>
                    <p class="text-sm text-muted mt-2">Полная JSON Schema: задайте структуру (<code>type</code>, <code>properties</code>) и описание (<code>description</code>) для каждого ключа и вложенных объектов. Схема используется для подсказок LLM и валидации результата.</p>
                </div>

                <div class="grid grid-2 mb-4">
                    <div class="card">
                        <h3 class="mb-4">System Prompt</h3>
                        <textarea id="dt-system-prompt" class="form-control" style="min-height:250px">${dt?.system_prompt || ''}</textarea>
                    </div>
                    <div class="card">
                        <h3 class="mb-4">User Prompt</h3>
                        <textarea id="dt-user-prompt" class="form-control" style="min-height:250px">${dt?.user_prompt || ''}</textarea>
                        <p class="text-sm text-muted mt-2">Используйте {report} для вставки текста документа, {format_instructions} для схемы.</p>
                    </div>
                </div>

                <div id="dt-error"></div>
                <div class="flex gap-2">
                    <button type="submit" class="btn btn-primary">${isNew ? 'Создать' : 'Сохранить'}</button>
                    ${!isNew ? '<button type="button" id="btn-test" class="btn btn-outline">Тестировать</button>' : ''}
                    ${!isNew ? '<button type="button" id="btn-deactivate" class="btn btn-danger">Деактивировать</button>' : ''}
                </div>
            </form>

            <div id="test-result" class="mt-4"></div>
        `;

        // Form submit
        document.getElementById('dt-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const errEl = document.getElementById('dt-error');
            errEl.innerHTML = '';

            let schema;
            try {
                schema = JSON.parse(document.getElementById('dt-schema').value);
            } catch {
                errEl.innerHTML = '<div class="alert alert-error">Невалидный JSON Schema</div>';
                return;
            }

            const body = {
                slug: document.getElementById('dt-slug').value,
                name: document.getElementById('dt-name').value,
                description: document.getElementById('dt-description').value || null,
                json_schema: schema,
                system_prompt: document.getElementById('dt-system-prompt').value,
                user_prompt: document.getElementById('dt-user-prompt').value,
                router_hints: document.getElementById('dt-hints').value || null,
                markdown_postprocessors: [...document.querySelectorAll('.md-plugin:checked')].map(c => c.value),
                json_postprocessors: [...document.querySelectorAll('.json-plugin:checked')].map(c => c.value),
            };

            try {
                if (isNew) {
                    await API.post('/document-types', body);
                } else {
                    await API.put(`/document-types/${params.slug}`, body);
                }
                window.location.hash = '#/doc-types';
            } catch (err) {
                errEl.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
            }
        });

        // Test button
        document.getElementById('btn-test')?.addEventListener('click', async () => {
            const sampleText = prompt('Вставьте текст документа для тестирования:');
            if (!sampleText) return;
            const resultEl = document.getElementById('test-result');
            resultEl.innerHTML = '<div class="card"><div class="spinner"></div> Тестирование...</div>';
            try {
                const result = await API.post(`/document-types/${params.slug}/test`, { sample_text: sampleText });
                resultEl.innerHTML = `
                    <div class="card">
                        <h3 class="mb-2">Результат теста</h3>
                        <p>Валидность: ${result.is_valid ? '✓' : '✗'} | Время: ${result.processing_time_ms}ms</p>
                        ${JsonViewer.render(result.extracted_json)}
                    </div>
                `;
            } catch (err) {
                resultEl.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
            }
        });

        // Deactivate
        document.getElementById('btn-deactivate')?.addEventListener('click', async () => {
            if (!confirm('Деактивировать тип документа?')) return;
            await API.del(`/document-types/${params.slug}`);
            window.location.hash = '#/doc-types';
        });
    },
};
