function redirectToUrl(param) {
        // Получаем текущий URL и параметры запроса
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    const params = url.searchParams;

        // Добавляем или изменяем параметр в зависимости от выбранной кнопки
    params.set(param.split('=')[0], param.split('=')[1]);

        // Собираем новый URL
    const newUrl = url.pathname + '?' + params.toString();

        // Перенаправляем пользователя на новый URL
    window.location.href = newUrl;
}

function openNextPage(action) {
    // Получаем текущий URL и параметры запроса
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    const params = url.searchParams;

    // Получаем текущее значение параметра 'page'
    let currentPage = parseInt(params.get('page')) || 0;

    // Увеличиваем значение параметра 'page' на 1
    if (action === 'next') {
        currentPage++;
    } else if (action === 'prev' && currentPage > 0) {
        currentPage--;
    }

    // Устанавливаем новое значение параметра 'page'
    params.set('page', currentPage);

    // Собираем новый URL
    const newUrl = url.pathname + '?' + params.toString();

    // Перенаправляем пользователя на новый URL
    window.location.href = newUrl;
}


