const LoginPage = {
    async render(container) {
        container.innerHTML = `
            <div class="login-wrapper">
                <div class="card login-card">
                    <h1>Doc2JSON</h1>
                    <p class="subtitle">Войдите в систему</p>
                    <div id="login-error"></div>
                    <form id="login-form">
                        <div class="form-group">
                            <label for="username">Имя пользователя</label>
                            <input type="text" id="username" class="form-control" required autofocus>
                        </div>
                        <div class="form-group">
                            <label for="password">Пароль</label>
                            <input type="password" id="password" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-primary" style="width:100%">Войти</button>
                    </form>
                </div>
            </div>
        `;

        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const errEl = document.getElementById('login-error');
            errEl.innerHTML = '';
            const btn = e.target.querySelector('button');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> Вход...';

            try {
                await Auth.login(
                    document.getElementById('username').value,
                    document.getElementById('password').value,
                );
                window.location.hash = '#/dashboard';
            } catch (err) {
                errEl.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
            } finally {
                btn.disabled = false;
                btn.textContent = 'Войти';
            }
        });
    },
};
