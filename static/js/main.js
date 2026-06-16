
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function handleFetchError(response) {
    if (response.status === 401 || response.status === 403) {
        showAlert('Ошибка доступа. Пожалуйста, войдите снова.', 'danger');
        setTimeout(() => {
            window.location.href = '/accounts/login/';
        }, 2000);
        const err = new Error('HTTP ' + response.status);
        err.status = response.status;
        throw err;
    }
    if (!response.ok) {
        const err = new Error('HTTP ' + response.status);
        err.status = response.status;
        throw err;
    }
    return response.json();
}

function showAlert(message, type = "success") {

    const alertContainer = document.createElement("div");
    alertContainer.className =
        `alert alert-${type} position-fixed top-0 end-0 m-3 shadow`;
    alertContainer.style.zIndex = "9999";
    alertContainer.innerText = message;

    document.body.appendChild(alertContainer);

    setTimeout(() => {
        alertContainer.remove();
    }, 3000);
}



document.addEventListener("click", function (e) {

    if (e.target.classList.contains("add-to-cart-btn")) {

        const button = e.target;
        const productId = button.dataset.productId;

        button.innerHTML =
            `<span class="spinner-border spinner-border-sm"></span> Добавление...`;
        button.disabled = true;

        fetch("/api/cart-items/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                product: productId,
                quantity: 1
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка добавления");
            }
            return response.json();
        })
        .then(data => {

            button.innerHTML = "✅ Добавлено";
            showAlert("Товар добавлен в корзину!", "success");

            setTimeout(() => {
                button.innerHTML = "🛒 Добавить в корзину";
                button.disabled = false;
            }, 1500);
        })
        .catch(error => {

            button.innerHTML = "🛒 Добавить в корзину";
            button.disabled = false;

            showAlert("Ошибка при добавлении товара", "danger");
        });

    }
});
