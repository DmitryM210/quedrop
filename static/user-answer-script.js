var urlParameters = window.location.pathname.split("/");
var privateGuid = urlParameters[urlParameters.length - 2];

function isEmptyOrWhitespace(str){
    return str === null || str.match(/^ *$/) !== null;
}

function convertFormDataToJson(form) {
    var formData = new FormData(form);
    var obj = {};

    obj['private_guid'] = privateGuid;
    //console.log(urlParameters[urlParameters.length - 2]);
    obj['title'] = document.getElementById('title').innerText;
    obj['description'] = document.getElementById('description').innerText;
    
    formData.forEach((value, key) => {
        var questionContainer = document.getElementById(key)
        var answerId = questionContainer.getAttribute("data-answer")
        var questionId = questionContainer.getAttribute("data-question")
        obj[key] = {
            question: document.getElementById(questionId).innerText,
            answer: document.getElementById(answerId).innerText,
            correct: value,
        }
    });

    return JSON.stringify(obj);
}

function submitCheck(event) {
    event.preventDefault();

    var result = convertFormDataToJson(event.target);
    
    var confirm = window.confirm('Are you sure you want to end checking?');
    if (!confirm) return;

    var target = window.location.href + "/" + event.target.getAttribute('action');
    var request = new Request(target, {
        method: 'POST',
        body: result,
        headers: {
            'Content-Type': 'application/json',
        },
    });
    
    // sending request asynchronously
    fetch(request)
    .then(
        (response) => response.json(),
        (error) => console.error(error)
    )
    .then(
        (data) => {
            console.log(data);
            window.location.replace(window.location.origin + "/form-list/" + privateGuid);
        }
    );
    
    console.log('Sending request ...');
}

document.getElementById('check-form')
    .addEventListener('submit', submitCheck);