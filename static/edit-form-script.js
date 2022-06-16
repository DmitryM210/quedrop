var questionCount = 0;

function hasDuplicates(array) {
    return (new Set(array)).size !== array.length;
}

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

function createLink(text, target, guid) {
    var link = document.createElement("a");
    link.href = window.location + "../" + target + "/" + guid;
    link.appendChild(document.createTextNode(text))
    return link;
}

function appendNewQuestion() {
    var questionSection = document.getElementById("question-section");

    var questionContainer = document.createElement("div");
    questionContainer.classList.add("edit-question");
    questionContainer.classList.add("question_answer");
    questionContainer.appendChild(createQuestionField());
    //questionContainer.appendChild(createWhitespace());
    //questionContainer.appendChild(createAnswerField());
    questionContainer.appendChild(createWhitespace());
    questionContainer.appendChild(createRemoveQuestionButton(questionContainer));
    questionCount++;

    questionSection.appendChild(questionContainer);
}

function showMessage(message) {
    var messageContainer = document.getElementById("message-container");
	messageContainer.style.display = "block";
    var messageTextNode = document.createTextNode(message);
    messageContainer.replaceChildren(messageTextNode);
}

function emplaceLinkToCreatedForm(publicGuid, privateGuid) {
    var messageContainer = document.getElementById("message-container");
	messageContainer.style.display = "block";
    var message = "You have successfully created a new form: ";
    var messageTextNode = document.createTextNode(message);
    var linkContainer = document.createElement("div");
    linkContainer.appendChild(createLink(
        "Created form", "user-form", publicGuid));
    linkContainer.appendChild(createWhitespace())
    linkContainer.appendChild(createLink(
        "Answers list", "form-list", privateGuid));
	var guidContainer = document.createElement("p");
	guidContainer.innerHTML = "Student's uuid: " + publicGuid;
	linkContainer.appendChild(guidContainer)
    messageContainer.replaceChildren(messageTextNode, linkContainer);
}

function convertFormDataToJson(form) {
    var formData = new FormData(form);
    var obj = {};
    var questions = [];
    formData.forEach((value, key) => {
        if (key.startsWith("question"))
            questions.push(value);
        obj[key] = value
    });
    return {
        hasQuestions: questions.length > 0,
        hasDuplicates: hasDuplicates(questions),
        json: JSON.stringify(obj), 
    };
}

function submitForm(event) {
    event.preventDefault();

    var result = convertFormDataToJson(event.target); 
    if (!result.hasQuestions) {
        showMessage("You cannot create a form without questions.");
        return;
    }
    if (result.hasDuplicates) {
        showMessage("There cannot be any identical questions.");
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
        (data) => emplaceLinkToCreatedForm(
            data.public_guid, data.private_guid)
    );

    console.log('Sending request ...');
}

document.getElementById('editable-form')
    .addEventListener('submit', submitForm);