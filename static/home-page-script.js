var uuidInput = document.getElementById("uuid-input");

function startAnswerClick(event) {
    event.preventDefault();

    var uuid = uuidInput.value;
    if (uuid.trim() == 0)
        return alert("Please, specify uuid first.");

    var redirect = window.location.origin + "/user-form/" + uuid;
    window.location.replace(redirect);

    return false;
}