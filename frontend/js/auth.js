const Auth = {
    _user: null,

    getToken() {
        return localStorage.getItem('access_token');
    },

    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    },

    setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    },

    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        this._user = null;
    },

    isAuthenticated() {
        return !!this.getToken();
    },

    async login(username, password) {
        const resp = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.detail || 'Login failed');
        }
        const data = await resp.json();
        this.setTokens(data.access_token, data.refresh_token);
        await this.fetchUser();
    },

    async fetchUser() {
        try {
            this._user = await API.get('/auth/me');
        } catch {
            this.clearTokens();
            this._user = null;
        }
        return this._user;
    },

    getUser() {
        return this._user;
    },

    hasRole(minRole) {
        const hierarchy = { operator: 0, manager: 1, admin: 2 };
        if (!this._user) return false;
        return (hierarchy[this._user.role] ?? 0) >= (hierarchy[minRole] ?? 99);
    },

    async refreshTokens() {
        const refresh = this.getRefreshToken();
        if (!refresh) return false;
        try {
            const resp = await fetch('/api/v1/auth/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refresh }),
            });
            if (!resp.ok) return false;
            const data = await resp.json();
            this.setTokens(data.access_token, data.refresh_token);
            return true;
        } catch {
            return false;
        }
    },

    logout() {
        this.clearTokens();
        window.location.hash = '#/login';
    },
};
