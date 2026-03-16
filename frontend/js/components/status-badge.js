const StatusBadge = {
    LABELS: {
        pending: 'Ожидание',
        ocr_in_progress: 'OCR',
        routing: 'Маршрутизация',
        extracting: 'Извлечение',
        validating: 'Валидация',
        completed: 'Готово',
        failed: 'Ошибка',
    },

    render(status) {
        const label = this.LABELS[status] || status;
        return `<span class="badge badge-${status}">${label}</span>`;
    },

    isProcessing(status) {
        return ['pending', 'ocr_in_progress', 'routing', 'extracting', 'validating'].includes(status);
    },
};
