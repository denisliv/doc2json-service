const Router = {
    routes: {
        '/login': { render: LoginPage.render, public: true },
        '/dashboard': { render: DashboardPage.render },
        '/upload': { render: UploadPage.render },
        '/jobs': { render: JobsPage.render },
        '/jobs/:id': { render: JobDetailPage.render },
        '/doc-types': { render: DocTypesPage.render },
        '/doc-types/:slug': { render: DocTypeEditorPage.render },
        '/users': { render: UsersPage.render },
    },

    async init() {
        window.addEventListener('hashchange', () => this.handleRoute());
        if (Auth.isAuthenticated()) {
            await Auth.fetchUser();
        }
        this.handleRoute();
    },

    async handleRoute() {
        const hash = window.location.hash.slice(1) || '/dashboard';
        const { handler, params } = this._matchRoute(hash);

        if (!handler) {
            document.getElementById('content').innerHTML = '<div class="card"><h2>404</h2><p>Страница не найдена</p></div>';
            return;
        }

        if (!handler.public && !Auth.isAuthenticated()) {
            window.location.hash = '#/login';
            return;
        }

        if (handler.public && hash === '/login' && Auth.isAuthenticated()) {
            window.location.hash = '#/dashboard';
            return;
        }

        this._updateNav(hash);
        const content = document.getElementById('content');
        content.innerHTML = '<div style="text-align:center;padding:40px"><div class="spinner"></div></div>';

        try {
            await handler.render(content, params);
        } catch (e) {
            if (e.status === 403) {
                content.innerHTML = `
                    <div class="card" style="text-align:center;padding:40px">
                        <h2>Нет доступа</h2>
                        <p class="text-muted">Недостаточно прав для просмотра этой страницы</p>
                        <a href="#/dashboard" class="btn btn-primary" style="margin-top:16px">На главную</a>
                    </div>`;
            } else {
                content.innerHTML = `<div class="alert alert-error">${e.message}</div>`;
            }
        }
    },

    _matchRoute(path) {
        for (const [pattern, handler] of Object.entries(this.routes)) {
            const regex = new RegExp('^' + pattern.replace(/:(\w+)/g, '([^/]+)') + '$');
            const match = path.match(regex);
            if (match) {
                const paramNames = [...pattern.matchAll(/:(\w+)/g)].map(m => m[1]);
                const params = {};
                paramNames.forEach((name, i) => params[name] = match[i + 1]);
                return { handler, params };
            }
        }
        return { handler: null, params: {} };
    },

    _updateNav(currentPath) {
        const navbar = document.getElementById('navbar');
        const navMenu = document.getElementById('nav-menu');
        const navUser = document.getElementById('nav-user');

        if (!Auth.isAuthenticated()) {
            navbar.classList.add('hidden');
            return;
        }

        navbar.classList.remove('hidden');
        const user = Auth.getUser();
        navUser.textContent = user ? `${user.full_name || user.username} (${user.role})` : '';

        const links = [
            { path: '/dashboard', label: 'Дашборд', role: 'operator' },
            { path: '/upload', label: 'Загрузка', role: 'operator' },
            { path: '/jobs', label: 'Задания', role: 'operator' },
            { path: '/doc-types', label: 'Типы', role: 'manager' },
            { path: '/users', label: 'Пользователи', role: 'admin' },
        ];

        navMenu.innerHTML = links
            .filter(l => Auth.hasRole(l.role))
            .map(l => `<a href="#${l.path}" class="nav-link ${currentPath.startsWith(l.path) ? 'active' : ''}">${l.label}</a>`)
            .join('');
    },
};

document.addEventListener('DOMContentLoaded', () => Router.init());
