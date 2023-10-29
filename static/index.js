// Function to shuffle an array randomly
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Function to display articles in a random order
function displayRandomArticles() {
    const container = document.querySelector('.container');
    if (!container) {
        console.error('Container element not found.');
        return;
    }

    const articles = Array.from(container.querySelectorAll('.article'));

    // Shuffle the articles randomly
    shuffleArray(articles);

    // Clear the current content
    container.innerHTML = '';

    // Append the shuffled articles back to the container
    articles.forEach(article => {
        container.appendChild(article);
    });
}

// Run the function on page load to display articles randomly
document.addEventListener('DOMContentLoaded', function() {
    displayRandomArticles();

    // Function to fetch data from the server
    function fetchDataFromServer() {
        // Make a GET request to the server's API endpoint
        fetch('/api/get_data')
            .then(response => response.json())
            .then(data => {
                // Handle the data received from the server
                console.log(data);

                // You can update the HTML content with the fetched data
                // For example, you can display the data in a specific element
                // document.getElementById('data-container').textContent = data.message;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Run the function to fetch data from the server
    fetchDataFromServer();
});


// 모달 창 열기
const memoModal = document.getElementById('memoModal');
const displayMemo = document.getElementById('displayMemo');
const memoText = document.getElementById('memoText');
const memoContent = document.getElementById('memoContent');

// 저장 버튼 클릭 시
const saveMemoButton = document.getElementById('saveMemo');
saveMemoButton.addEventListener('click', () => {
    const memo = memoText.value;

    // 저장된 메모를 표시 창에 표시
    memoContent.textContent = memo;

    // 모달 창 닫기
    memoModal.style.display = 'none';
    displayMemo.style.display = 'block'; // 메모 표시 창 표시
});

// 모달 창 닫기
const closeModal = document.querySelector('.close');
closeModal.addEventListener('click', () => {
    memoModal.style.display = 'none';
});

// 모달 창 열기 버튼
const openModalButton = document.createElement('button');
openModalButton.textContent = 'Add Memo';
openModalButton.className = 'open-modal-button';

// 모달 창 열기 버튼을 웹 페이지에 추가
document.body.appendChild(openModalButton);

// 모달 창 열기 버튼을 클릭하면 모달 창을 엽니다.
openModalButton.addEventListener('click', () => {
    memoModal.style.display = 'block';
    memoText.value = ''; // 메모 텍스트 영역 초기화
    displayMemo.style.display = 'none'; // 메모 표시 창 숨김
});
