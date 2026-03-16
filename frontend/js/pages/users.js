const UsersPage = {
    async render(container) {
        await this._load(container);
    },

    async _load(container) {
        const users = await API.get('/admin/users');

        container.innerHTML = `
            <div class="page-header">
                <h1>Пользователи</h1>
                <button class="btn btn-primary" id="btn-add-user">Создать пользователя</button>
            </div>

            <div class="card">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Имя пользователя</th>
                                <th>Полное имя</th>
                                <th>Роль</th>
                                <th>Статус</th>
                                <th>Создан</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            ${users.map(u => `
                                <tr>
                                    <td><strong>${u.username}</strong></td>
                                    <td>${u.full_name || '—'}</td>
                                    <td><span class="badge badge-${u.role === 'admin' ? 'completed' : u.role === 'manager' ? 'processing' : 'pending'}">${u.role}</span></td>
                                    <td>${u.is_active ? '<span class="badge badge-completed">Активен</span>' : '<span class="badge badge-failed">Неактивен</span>'}</td>
                                    <td class="text-muted">${new Date(u.created_at).toLocaleDateString('ru')}</td>
                                    <td class="text-right">
                                        <button class="btn btn-sm btn-outline btn-edit" data-id="${u.id}" data-username="${u.username}" data-fullname="${u.full_name || ''}" data-role="${u.role}" data-active="${u.is_active}">Изменить</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>

            <div id="user-modal" class="hidden">
                <div style="position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:200;display:flex;align-items:center;justify-content:center">
                    <div class="card" style="width:450px;max-width:90vw">
                        <h3 id="modal-title" class="mb-4"></h3>
                        <form id="user-form">
                            <input type="hidden" id="uf-id">
                            <div class="form-group">
                                <label>Имя пользователя</label>
                                <input type="text" id="uf-username" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label>Полное имя</label>
                                <input type="text" id="uf-fullname" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>Пароль <span class="text-sm text-muted" id="pw-hint"></span></label>
                                <input type="password" id="uf-password" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>Роль</label>
                                <select id="uf-role" class="form-control">
                                    <option value="operator">operator</option>
                                    <option value="manager">manager</option>
                                    <option value="admin">admin</option>
                                </select>
                            </div>
                            <div class="form-group" id="uf-active-group" style="display:none">
                                <label><input type="checkbox" id="uf-active"> Активен</label>
                            </div>
                            <div id="modal-error"></div>
                            <div class="flex gap-2">
                                <button type="submit" class="btn btn-primary">Сохранить</button>
                                <button type="button" class="btn btn-outline" id="btn-cancel-modal">Отмена</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        `;

        // Add user
        document.getElementById('btn-add-user').addEventListener('click', () => {
            this._openModal(null);
        });

        // Edit user
        container.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', () => {
                this._openModal({
                    id: btn.dataset.id,
                    username: btn.dataset.username,
                    full_name: btn.dataset.fullname,
                    role: btn.dataset.role,
                    is_active: btn.dataset.active === 'true',
                });
            });
        });

        // Cancel modal
        document.getElementById('btn-cancel-modal')?.addEventListener('click', () => {
            document.getElementById('user-modal').classList.add('hidden');
        });

        // Form submit
        document.getElementById('user-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const errEl = document.getElementById('modal-error');
            errEl.innerHTML = '';
            const id = document.getElementById('uf-id').value;
            const isEdit = !!id;

            try {
                if (isEdit) {
                    const body = {
                        full_name: document.getElementById('uf-fullname').value || null,
                        role: document.getElementById('uf-role').value,
                        is_active: document.getElementById('uf-active').checked,
                    };
                    const pw = document.getElementById('uf-password').value;
                    if (pw) body.password = pw;
                    await API.put(`/admin/users/${id}`, body);
                } else {
                    const pw = document.getElementById('uf-password').value;
                    if (!pw) { errEl.innerHTML = '<div class="alert alert-error">Пароль обязателен</div>'; return; }
                    await API.post('/admin/users', {
                        username: document.getElementById('uf-username').value,
                        password: pw,
                        full_name: document.getElementById('uf-fullname').value || null,
                        role: document.getElementById('uf-role').value,
                    });
                }
                document.getElementById('user-modal').classList.add('hidden');
                this._load(container);
            } catch (err) {
                errEl.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
            }
        });
    },

    _openModal(user) {
        const modal = document.getElementById('user-modal');
        document.getElementById('modal-title').textContent = user ? 'Редактировать пользователя' : 'Новый пользователь';
        document.getElementById('uf-id').value = user?.id || '';
        document.getElementById('uf-username').value = user?.username || '';
        document.getElementById('uf-username').readOnly = !!user;
        document.getElementById('uf-fullname').value = user?.full_name || '';
        document.getElementById('uf-password').value = '';
        document.getElementById('pw-hint').textContent = user ? '(оставьте пустым, чтобы не менять)' : '';
        document.getElementById('uf-role').value = user?.role || 'operator';
        document.getElementById('uf-active-group').style.display = user ? '' : 'none';
        document.getElementById('uf-active').checked = user?.is_active ?? true;
        document.getElementById('modal-error').innerHTML = '';
        modal.classList.remove('hidden');
    },
};
