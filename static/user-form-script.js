function isEmptyOrWhitespace(str){
    return str === null || str.match(/^ *$/) !== null;
}

function convertFormDataToJson(form) {
    var formData = new FormData(form);
    var path = window.location.pathname;
    var obj = {};

    obj['public_guid'] = path.substring(path.lastIndexOf('/') + 1);
    obj['title'] = document.getElementById('title').innerText;
    obj['description'] = document.getElementById('description').innerText;
    
    var emptyAnswers = 0;
    formData.forEach((value, key) => {
        if (isEmptyOrWhitespace(value))
            emptyAnswers++;
        obj[key] = {
            question: document.getElementById(key).innerText,
            answer: value,
        }
    });
    return {
        allAnswered: emptyAnswers == 0,
        json: JSON.stringify(obj), 
    };
}

function submitAnswer(event) {
    event.preventDefault();

    var result = convertFormDataToJson(event.target); 
    if (!result.allAnswered) {
        console.log('There are empty answers ...');
        return;
    }

    var request = new Request(event.target.action, {
        method: 'POST',
        body: result.json,
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
            alert("You have succsessfully sent your answers to the server!");
            window.location.replace(window.location.origin);
        }
    );
    
    console.log('Sending request ...');
}

document.getElementById('answer-form')
    .addEventListener('submit', submitAnswer);