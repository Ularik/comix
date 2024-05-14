$(document).ready(function() {
    $('#grade').change(function() { // Обработчик изменения значения в select
        const selectedRating = $(this).val(); // Получаем выбранное значение
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Получаем CSRF токен из формы
        const formData = new FormData();
        formData.append('grade', selectedRating);

        $.ajax({
            url: window.location.href, // Укажите адрес сервера
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken); // Добавляем CSRF токен к запросу
            },
            success: function(response) {
                // Обработка успешного ответа от сервера
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Обработка ошибки
                console.error(xhr, status, error);
            }
        });
    });
});

$(document).ready(function() {
    function handleAction(button, actionType, svgFilled, svgEmpty) {
        button.click(function(event) {    // Обработчик клика по кнопке
            event.preventDefault();

            // Переключаем состояние кнопки немедленно для предотвращения задержки
            const currentState = $(this).data(actionType);
            const newState = !currentState;
            $(this).data(actionType, newState);
            $(this).html(newState ? svgFilled : svgEmpty);

            const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

            $.ajax({
                url: window.location.href,    // Получаем адрес сервера
                type: 'POST',
                data: { [actionType]: newState },
                headers: { 'X-CSRFToken': csrfToken },
                success: function(response) {
                    console.log(response);
                },
                error: function(xhr, status, error) {
                    console.error(xhr, status, error);
                }
            });
        });
    }
    const likeSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-balloon-heart-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8.49 10.92C19.412 3.382 11.28-2.387 8 .986 4.719-2.387-3.413 3.382 7.51 10.92l-.234.468a.25.25 0 1 0 .448.224l.04-.08c.009.17.024.315.051.45.068.344.208.622.448 1.102l.013.028c.212.422.182.85.05 1.246-.135.402-.366.751-.534 1.003a.25.25 0 0 0 .416.278l.004-.007c.166-.248.431-.646.588-1.115.16-.479.212-1.051-.076-1.629-.258-.515-.365-.732-.419-1.004a2 2 0 0 1-.037-.289l.008.017a.25.25 0 1 0 .448-.224l-.235-.468ZM6.726 1.269c-1.167-.61-2.8-.142-3.454 1.135-.237.463-.36 1.08-.202 1.85.055.27.467.197.527-.071.285-1.256 1.177-2.462 2.989-2.528.234-.008.348-.278.14-.386"/></svg>'
    const likeEmptySvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-balloon-heart" viewBox="0 0 16 16"><path fill-rule="evenodd" d="m8 2.42-.717-.737c-1.13-1.161-3.243-.777-4.01.72-.35.685-.451 1.707.236 3.062C4.16 6.753 5.52 8.32 8 10.042c2.479-1.723 3.839-3.29 4.491-4.577.687-1.355.587-2.377.236-3.061-.767-1.498-2.88-1.882-4.01-.721zm-.49 8.5c-10.78-7.44-3-13.155.359-10.063q.068.062.132.129.065-.067.132-.129c3.36-3.092 11.137 2.624.357 10.063l.235.468a.25.25 0 1 1-.448.224l-.008-.017c.008.11.02.202.037.29.054.27.161.488.419 1.003.288.578.235 1.15.076 1.629-.157.469-.422.867-.588 1.115l-.004.007a.25.25 0 1 1-.416-.278c.168-.252.4-.6.533-1.003.133-.396.163-.824-.049-1.246l-.013-.028c-.24-.48-.38-.758-.448-1.102a3 3 0 0 1-.052-.45l-.04.08a.25.25 0 1 1-.447-.224l.235-.468ZM6.013 2.06c-.649-.18-1.483.083-1.85.798-.131.258-.245.689-.08 1.335.063.244.414.198.487-.043.21-.697.627-1.447 1.359-1.692.217-.073.304-.337.084-.398"/></svg>'
    const bookmarkSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-check-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M2 15.5V2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5m8.854-9.646a.5.5 0 0 0-.708-.708L7.5 7.793 6.354 6.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0z"/></svg>'
    const bookmarkEmptySvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark" viewBox="0 0 16 16"><path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/></svg>'

    handleAction($('button[name="like"]'), 'comix_like', likeSvg, likeEmptySvg);
    handleAction($('button[name="bookmark"]'), 'comix_bookmark', bookmarkSvg, bookmarkEmptySvg);
});



