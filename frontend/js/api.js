const API = {
    BASE: '/api/v1',

    async _fetch(url, options = {}) {
        const token = Auth.getToken();
        const headers = { ...(options.headers || {}) };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        if (!(options.body instanceof FormData) && !headers['Content-Type']) {
            headers['Content-Type'] = 'application/json';
        }

        let resp = await fetch(this.BASE + url, { ...options, headers });

        if (resp.status === 401 && Auth.getRefreshToken()) {
            const refreshed = await Auth.refreshTokens();
            if (refreshed) {
                headers['Authorization'] = `Bearer ${Auth.getToken()}`;
                resp = await fetch(this.BASE + url, { ...options, headers });
            }
        }

        if (!resp.ok) {
            const err = await resp.json().catch(() => ({ detail: resp.statusText }));
            const error = new Error(err.detail || `HTTP ${resp.status}`);
            error.status = resp.status;
            throw error;
        }
        return resp.json();
    },

    get(url) { return this._fetch(url); },

    post(url, body) {
        return this._fetch(url, {
            method: 'POST',
            body: body instanceof FormData ? body : JSON.stringify(body),
        });
    },

    put(url, body) {
        return this._fetch(url, {
            method: 'PUT',
            body: JSON.stringify(body),
        });
    },

    del(url) {
        return this._fetch(url, { method: 'DELETE' });
    },

    upload(url, formData) {
        return this._fetch(url, {
            method: 'POST',
            body: formData,
            headers: {},
        });
    },
};
