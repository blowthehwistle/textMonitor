let dataSent = false;
let startTime = new Date();
let endTime;
let authorInfoClicked = false;
let articleId = window.articleId; // Retrieve articleId from global window object
let feedbackRedirectUrl = ''; // Global variable to store the URL for redirection


function showQuestionModal(event, startTime, articleId, authorInfoClicked, targetUrl) {
    const endTime = new Date();
    feedbackRedirectUrl = targetUrl; // Store the URL to redirect after feedback

    console.log("Feedback Redirect URL:", feedbackRedirectUrl);
    console.log("Article ID:", articleId);
    console.log("Start Time:", startTime);
    console.log("Author Info Clicked:", authorInfoClicked);

    // Show the modal
    const modal = document.getElementById('questionModal');
    modal.style.display = 'block';
    sendData(articleId, startTime, endTime, authorInfoClicked);
    dataSent = true;
}

function submitAnswer() {
    // Get the user's feedback
    const feedback = document.getElementById('userAnswer').value;

    // Create a data object to send to the server
    const data = {
        articleId: window.articleId, // Ensure this is the correct variable
        feedback: feedback
    };

    // Send a POST request to the server
    fetch('/submit-feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("Redirecting..."); // Log before redirecting
        console.log("Redirect URL:", feedbackRedirectUrl); // Log the redirect URL
        window.location.href = feedbackRedirectUrl; // Redirect to the stored URL
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
function closeQuestionModal() {
    const questionModal = document.getElementById('questionModal');
    questionModal.style.display = 'none';
}

window.addEventListener("beforeunload", function(event) {
    if (!dataSent && !(window.location.href.includes('/end'))) {
        const endTime = new Date();
        sendData(articleId, startTime, endTime, authorInfoClicked);
    }
});

function sendData(articleId, startTime, endTime, authorInfoClicked) {
    const _duration = endTime.getTime() - startTime.getTime();
    const fstartTime = startTime.toISOString(); // ISO 8601 포맷으로 변환
    const fendTime = endTime.toISOString(); // ISO 8601 포맷으로 변환

    const visitData = {
        article_id: articleId,
        start_time: fstartTime,
        end_time: fendTime,
        duration: _duration,
        author_info_clicked: authorInfoClicked // author_info_clicked 추가
    };

    console.log('Sending visitData:', visitData); // Debugging statement

    // 서버에 POST 요청을 보냄
    fetch('/record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(visitData)
    })
    .then(response => {
        if (response.ok) {
            console.log('Visit recorded successfully.');
        } else {
            return response.json().then(errorData => {
                console.error('Failed to record visit. Status:', response.status, 'Response:', errorData);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
// // Function to show the question modal
// function showQuestionModal(startTime, articleId, authorInfoClicked) {
//     const endTime = new Date();
//     // Show the modal
//     const modal = document.getElementById('questionModal');
//     modal.style.display = 'block';
//     sendData(articleId, startTime, endTime, authorInfoClicked);
//     dataSent = true;
// }


// function submitAnswer() {
//     // Get the user's feedback
//     const feedback = document.getElementById('userAnswer').value;

//     // Create a data object to send to the server
//     const data = {
//         articleId: articleId, // Assuming articleId is defined globally
//         feedback: feedback
//     };

//     // Send a POST request to the server
//     fetch('/submit-feedback', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//     })
//     .then(result => {
//         console.log("Redirecting..."); // Log before redirecting
//         window.location.href = '/index'; // Redirect to index.html
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }

function openModal() {
    authorInfoClicked = true;

    // 모달 엘리먼트를 가져와서 스타일을 변경하여 모달을 보이게 합니다.
    const modal = document.getElementById('authorModal');
    modal.style.display = 'block';
}

function closeModal() {
    // 모달 엘리먼트를 가져와서 스타일을 변경하여 모달을 숨깁니다.
    const modal = document.getElementById('authorModal');
    modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const articleLinks = document.querySelectorAll('.random-article a');
    articleLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior

            // Get the URL to navigate to
            const targetUrl = event.target.href;

            // Show the question modal
            if (!dataSent) {
                console.log('Opening question modal with articleId:', window.articleId); // Debugging statement
                showQuestionModal(startTime, window.articleId, authorInfoClicked, targetUrl); // Show the modal with the target URL
            } else {
                window.location.href = targetUrl; // Navigate to the article if feedback is already submitted
            }
        });
    });
});