// article.js

document.addEventListener("DOMContentLoaded", function() {

    window.history.pushState(null, '', location.href);

    window.onpopstate = () => {
    history.go(1);
    this.handleGoback();
};

});

function sendData(articleId, startTime, endTime) {
    const _duration = endTime.getTime() - startTime.getTime();
    const fstartTime = startTime.toISOString(); // ISO 8601 포맷으로 변환
    const fendTime = endTime.toISOString(); // ISO 8601 포맷으로 변환

    const visitData = {
        article_id: articleId,
        start_time: fstartTime,
        end_time: fendTime,
        duration: _duration
    };

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
            console.error('Failed to record visit.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function markAsRead(articleId, authorInfoClicked){
      // Make a POST request to the server to mark the article as read
      fetch('/mark-as-read', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ articleId: articleId, authorInfoClicked: authorInfoClicked })
    })
    .then(response => {
        if (response.ok) {
            console.log('Article marked as read.');
        } else {
            console.error('Failed to mark article as read.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to show the question modal
function showQuestionModal(startTime, articleId, authorInfoClicked) {
    const endTime = new Date();
    // Show the modal
    const modal = document.getElementById('questionModal');
    modal.style.display = 'block';
    sendData(articleId, startTime, endTime);
    markAsRead(articleId,authorInfoClicked);
}

function closeQuestionModal() {
    const questionModal = document.getElementById('questionModal');
    questionModal.style.display = 'none';
}

// Function to readingDone button and redirect to end.html
function ReadingDone(startTime, articleId) {
    const endTime = new Date();
    sendData(articleId, startTime, endTime);
    markAsRead(articleId, authorInfoClicked);
    window.location.href = '/end'; // Redirect to end
  
}

function submitAnswer() {
    // Get the user's feedback
    const feedback = document.getElementById('userAnswer').value;

    // Create a data object to send to the server
    const data = {
        articleId: articleId, // Assuming articleId is defined globally
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
    .then(result => {
        console.log("Redirecting..."); // Log before redirecting
        window.location.href = '/'; // Redirect to index.html
    })
    .catch(error => {
        console.error('Error:', error);
    });
}    


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
