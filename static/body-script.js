var questionCount = 0;

function createWhitespace() {
    return document.createTextNode("\u00A0");
}

function createQuestionField() {
    var questionField = document.createElement("input");
    questionField.type = "text";
    questionField.name = "question_" + questionCount;
    questionField.placeholder = "Question ...";
    questionField.required = true;
    return questionField;
}

function createAnswerField() {
    var answerField = document.createElement("input");
    answerField.type = "text";
    //answerField.name = "answer_" + questionCount;
    answerField.placeholder = "Answer ...";
    answerField.readOnly = true;
    return answerField;
}

function createRemoveQuestionButton(containerToRemove) {
    var removeButton = document.createElement("input");
    removeButton.type = "button";
    removeButton.value = "⨯";
    removeButton.addEventListener('click', 
        () => containerToRemove.remove(), false);
    return removeButton;
}

function createLink(guid) {
    var link = document.createElement("a");
    link.href = window.location + "../user-form/" + guid;
    link.appendChild(document.createTextNode("Created form"))
    return link;
}

function appendNewQuestion() {
    var questionSection = document.getElementById("question-section");

    var questionContainer = document.createElement("div");
    questionContainer.classList.add("edit-question");
    questionContainer.appendChild(createQuestionField());
    questionContainer.appendChild(createWhitespace());
    questionContainer.appendChild(createAnswerField());
    questionContainer.appendChild(createWhitespace());
    questionContainer.appendChild(createRemoveQuestionButton(questionContainer));
    questionCount++;

    questionSection.appendChild(questionContainer);
}

function emplaceNoQuestionsMessage() {
    var messageContainer = document.getElementById("message-container");
    var message = "You cannot create a form without questions.";
    var messageTextNode = document.createTextNode(message);
    messageContainer.replaceChildren(messageTextNode);
}

function emplaceLinkToCreatedForm(guid) {
    var messageContainer = document.getElementById("message-container");
    var message = "You have successfully created a new form: ";
    var messageTextNode = document.createTextNode(message);
    messageContainer.replaceChildren(
        messageTextNode, createLink(guid));
}

function convertFormDataToJson(form) {
    var formData = new FormData(form);
    var obj = {};
    formData.forEach((value, key) => obj[key] = value);
    return {
        hasQuestions: Object.keys(obj).length > 2,
        json: JSON.stringify(obj), 
    };
}

function submitForm(event) {
    event.preventDefault();

    var result = convertFormDataToJson(event.target); 
    if (!result.hasQuestions) {
        emplaceNoQuestionsMessage();
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
        (data) => emplaceLinkToCreatedForm(data.guid)
    );

    console.log('Sending request ...');
}

document.getElementById('editable-form')
    .addEventListener('submit', submitForm);