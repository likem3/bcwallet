window.addEventListener('load', function () {
    function generateModalHTML() {
        var modalHTML = `
            <div id="myModal" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <img class="modal-image" id="modalImg" src="" alt="">
                    <p id="addressBill"></p>
                    <p id="addressTxt"></p>
                    <p id="addressCrcy"></p>
                </div>
            </div>
        `;
    
        var contentDiv = document.getElementById('content');
        contentDiv.insertAdjacentHTML('afterend', modalHTML);
    }
    
    generateModalHTML()


    var buttons = document.getElementsByClassName("qr-image");
    var modal = document.querySelector(".modal");
    var span = modal.querySelector(".close");

    for (var i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function() {
            modal.style.display = "block";
            modalImg.src = this.src;
            modalImg.alt = this.alt;
            modalImg.style.width = '100%'
            if(this.dataset.amount) {
                addressBill.innerHTML = `<strong>Amount : </strong>${this.dataset.amount}`;
            }
            addressTxt.innerHTML = `<strong>Address : </strong>${this.dataset.address}`;
            addressCrcy.innerHTML = `<strong>Currency : </strong>${this.alt}`;
        });
    }

    span.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
        modal.style.display = "none";
        }
    };

})
