document.addEventListener("DOMContentLoaded", function() {
    var pageCurElement = document.getElementById("page-cure");
    var pageNumElement = document.getElementById("page-num");

    // Debugging output
    console.log("Page Current Element:", pageCurElement);
    console.log("Page Number Element:", pageNumElement);

    if (pageCurElement && pageNumElement) {
        var pageCur = Number(pageCurElement.value);
        var pageNum = Number(pageNumElement.value);

        if (pageCur === pageNum) {
            document.getElementById('show-more').classList.add('disabled');
        }
    } else {
        console.error("Page current or page number element not found.");
    }
});

function showMore() {
    var pageCurElement = document.getElementById("page-cure");
    var pageNumElement = document.getElementById("page-num");

    // Check if elements exist
    if (!pageCurElement || !pageNumElement) {
        console.error("Page current or page number element not found.");
        return;
    }

    var pageCur = Number(pageCurElement.value);
    var pageNum = Number(pageNumElement.value);

    // Increment current page
    pageCur += 1;

    fetch("?page=" + pageCur, { 
        headers: {
            "X-Requested-With": 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.text();
    })
    .then(data => {
        var pollContainer = document.getElementsByClassName("poll-container")[0];
        if (pollContainer) {
            pollContainer.innerHTML += data; 
        } else {
            console .error("Poll container not found.");
        }

        pageCurElement.value = pageCur;

        if (pageCur === pageNum) {
            document.getElementById("show-more").classList.add("disabled");
        }
    })
    .catch(error => console.log("Error:", error));
}

function updatePagination(pageCur) {
    var numPages = document.getElementsByClassName("pagination")[0];
    if (!numPages) {
        console.error("Pagination element not found.");
        return;
    }

    let ind = 1;

    for (let nP of numPages.children) {
        nP.classList.remove("active");
        nP.classList.remove("disabled");

        if (pageCur === ind) {
            nP.classList.add("disabled");
        }
        ind++;
    }
}