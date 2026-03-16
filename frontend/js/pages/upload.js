const UploadPage = {
    async render(container) {
        let docTypes = [];
        try {
            docTypes = await API.get('/document-types');
        } catch { /* no types available */ }

        container.innerHTML = `
            <div class="page-header">
                <h1>Загрузка документов</h1>
            </div>
            <div class="card">
                ${FileUpload.render('upload')}
                <div class="form-group mt-4">
                    <label for="doc-type">Тип документа (необязательно)</label>
                    <select id="doc-type" class="form-control">
                        <option value="">Автоопределение</option>
                        ${docTypes.map(t => `<option value="${t.slug}">${t.name}</option>`).join('')}
                    </select>
                </div>
                <div id="upload-error"></div>
                <button id="btn-upload" class="btn btn-primary mt-2" disabled>Отправить на обработку</button>
            </div>
            <div id="upload-result"></div>
        `;

        FileUpload.init('upload');

        const btnUpload = document.getElementById('btn-upload');
        const observer = new MutationObserver(() => {
            btnUpload.disabled = FileUpload.getFiles().length === 0;
        });
        observer.observe(document.getElementById('upload-list'), { childList: true });

        btnUpload.addEventListener('click', async () => {
            const files = FileUpload.getFiles();
            if (files.length === 0) return;

            btnUpload.disabled = true;
            btnUpload.innerHTML = '<span class="spinner"></span> Отправка...';
            const errEl = document.getElementById('upload-error');
            errEl.innerHTML = '';

            try {
                const formData = new FormData();
                files.forEach(f => formData.append('files', f));
                const docType = document.getElementById('doc-type').value;
                if (docType) formData.append('document_type_slug', docType);

                const result = await API.upload('/documents/process', formData);

                document.getElementById('upload-result').innerHTML = `
                    <div class="alert alert-success">
                        Задание создано! 
                        <a href="#/jobs/${result.job_id}">Перейти к результату</a>
                    </div>
                `;
                FileUpload.clear();
                document.getElementById('upload-list').innerHTML = '';
            } catch (err) {
                errEl.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
            } finally {
                btnUpload.disabled = false;
                btnUpload.textContent = 'Отправить на обработку';
            }
        });
    },
};
