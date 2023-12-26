// memo.js

// Function to open the memo modal
function openMemo() {
    const memoModal = document.getElementById('memoModal');
    memoModal.style.display = 'block';
}

// Function to close the memo modal
function closeMemo() {
    const memoModal = document.getElementById('memoModal');
    memoModal.style.display = 'none';
}

// Function to save the memo content
function saveMemo() {
    const memoText = document.getElementById('memoText').value;
    const timestamp = new Date().toISOString(); // Format the timestamp as a string

    // Send a POST request to save the memo for the current article
    fetch('/save-memo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            articleId: articleId,
            memo: memoText,
            timestamp: timestamp, // Include the timestamp as a string
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Memo saved successfully') {
            // Memo saved successfully, clear the memo text box
            document.getElementById('memoText').value = '';

            // Add the new memo to the page
            const memoContainer = document.getElementById('memoContainer');
            const memoItem = document.createElement('p');
            memoItem.textContent = memoText;
            memoContainer.appendChild(memoItem);
        } else {
            console.error('Failed to save memo.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// Function to display all saved memos
function displayAllMemos() {
    // Send a GET request to retrieve all saved memos
    fetch('/get-all-memos')
        .then(response => response.json())
        .then(memos => {
            // Create an object to organize memos by article ID
            const memosByArticleId = {};

            // Organize memos by article ID
            memos.forEach(memo => {
                const articleId = memo.articleId;
                if (!memosByArticleId[articleId]) {
                    memosByArticleId[articleId] = [];
                }
                memosByArticleId[articleId].push(memo);
            });

            // Display all saved memos
            const memoContainer = document.getElementById('memoContainer');
            memoContainer.innerHTML = ''; // Clear the previous content

            for (const articleId in memosByArticleId) {
                const memosForArticle = memosByArticleId[articleId];

                // Get the title of the article from the first memo
                const articleTitle = memosForArticle[0].title;

                // Create a heading for the article
                const articleHeading = document.createElement('h3');
                articleHeading.textContent = `Memos from "${articleTitle}"`; 
                memoContainer.appendChild(articleHeading);

                // Create a list for memos in this article
                const memoList = document.createElement('ul');
                memosForArticle.forEach(memo => {
                    const memoItem = document.createElement('li');
                    memoItem.textContent = `Memo: ${memo.content}`;
                    memoList.appendChild(memoItem);
                });

                memoContainer.appendChild(memoList);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



// Initialize the memo display on page load
displayAllMemos();

// Initialize the memo display on page load
window.onload = function () {
    displayAllMemos();
};

