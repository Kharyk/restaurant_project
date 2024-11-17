function showMore() {
    var pageCur = Number(document.getElementById("page-cure").value);
    var pageNum = Number(document.getElementById("page-num").value);

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
            document.getElementsByClassName("poll-container")[0].innerHTML += data; 
            document.getElementById("page-cure").value = pageCur;

            if (pageCur === pageNum) {
                document.getElementById("show-more").classList.add("disabled");
            }
        })
        .catch(error => console.log("Error:", error));
}

window.addEventListener("load", function() {
    var pageCur = Number(document.getElementById("page-cure").value);
    var pageNum = Number(document.getElementById("page-num").value);

    if (pageCur === pageNum) {
        this.document.getElementById('show-more').classList.add('disabled');
    }
});

function updatePagination() {
    var numPages = document.getElementsByClassName("pagination")[0];
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