let grouped = {};

function openImageModal(partNumber, clickedImageIndex = 0) {
    const imageList = grouped[partNumber].images;
    const enlargedImage = document.getElementById('enlargedImage');
    enlargedImage.src = `/image/${imageList[clickedImageIndex].replace(/\\/g, '/')}`;
    enlargedImage.dataset.currentImageIndex = clickedImageIndex; 
    enlargedImage.dataset.partNumber = partNumber; 
    $('#imageModal').modal('show');
}

function copy(element){
    const tempInput = document.createElement('input');
    tempInput.value = element.previousElementSibling.textContent.trim();
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);
    
    const tooltip = element.nextElementSibling;
    tooltip.style.visibility = "visible";
    tooltip.style.opacity = "1";
    setTimeout(() => {
        tooltip.style.opacity = "0";
    }, 1500); 
}



document.getElementById('prevImage').addEventListener('click', function(e) {
    e.preventDefault();
    switchModalImage(-1);
});

document.getElementById('nextImage').addEventListener('click', function(e) {
    e.preventDefault();
    switchModalImage(1);
});

function switchModalImage(direction) {
    const imgElement = document.getElementById('enlargedImage');
    const currentImageIndex = +imgElement.dataset.currentImageIndex; 
    const partNumber = imgElement.dataset.partNumber;
    const imageList = grouped[partNumber].images;

    let newIndex = currentImageIndex + direction;
    if (newIndex < 0) newIndex = imageList.length - 1;
    if (newIndex >= imageList.length) newIndex = 0; 

    imgElement.src = `/image/${imageList[newIndex].replace(/\\/g, '/')}`;
    imgElement.dataset.currentImageIndex = newIndex;
}

function closeImageModal() {
    $('#imageModal').modal('hide');
}

function handleKeyPress(event) {
    if (event.keyCode === 13 && event.target.id === 'searchQuery') {
        search();
    }
}

function search() {
    const query = document.getElementById("searchQuery").value;
    if (query === "") {
        return;
    }
    const searchType = document.querySelector('input[name="searchType"]:checked').value;

    let endpoint;
    if (searchType === "part") {
        endpoint = `/costco/search-part?query=${query}`;
    } else {
        endpoint = `/costco/search?query=${query}`;
    }

    fetch(endpoint)
    .then(response => response.json())
    .then(data => {
        let uniquePartNumbers = new Set(data.map(item => item.part_number));
        document.getElementById("resultsCount").innerText = `Total Results: ${uniquePartNumbers.size}`;
        grouped = {};
        data.forEach(item => {
            
            if (!grouped[item.part_number]) {
                grouped[item.part_number] = {
                    description: item.description,
                    images: []
                };
            }
            grouped[item.part_number].images.push(item.image);
        });

        const displayType = document.getElementById("displayType").value;
        if (displayType === 'grid') {
            let html = '<div class="row">'; 

            for (const partNumber in grouped) {
                const item = grouped[partNumber];
                
                html += `<div class="col-md-3 mb-4">`;  
                html += `<div class="image-card">`;

                html += `<div id="carousel${partNumber}" class="carousel slide" data-ride="carousel">`;
                html += `<div class="carousel-inner">`;

                item.images.forEach((imgSrc, index) => {
                    html += `
                    <div class="carousel-item ${index === 0 ? 'active' : ''}">
                        <img src="/image/${imgSrc.replace(/\\/g, '/')}" class="d-block w-100" cursor: pointer;" onclick="openImageModal('${partNumber}', ${index})" alt="Image for ${partNumber}">
                    </div>`;
                });

                html += `</div>`;

                if (item.images.length > 1) {
                    html += `
                    <a class="carousel-control-prev" href="#carousel${partNumber}" role="button" data-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="sr-only">Previous</span>
                    </a>
                    <a class="carousel-control-next" href="#carousel${partNumber}" role="button" data-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="sr-only">Next</span>
                    </a>`;
                }
                
                html += `</div>`;
                html += `<p class="copy-container">
                        <strong>${partNumber}</strong>
                        <span class="material-icons copy-icon" onclick="copy(this)">content_copy</span>
                        <span class="tooltip">Copied!</span>
                    </p>`;
                html += `<p style="font-size: 0.8rem;">${item.description}</p>`;

                html += `</div>`;
                html += `</div>`;
            }

            html += '</div>';
            document.getElementById("results").innerHTML = html;

        } else {
            let html = '<table class="table table-bordered">'; 
            html += '<thead>';
            html += '<tr>';
            html += '<th class="part-number-column">Part Number</th>';
            html += '<th class="text-center">Description</th>';
            html += '<th class="text-center">Image</th>';
            html += '</tr>';
            html += '</thead>';
            html += '<tbody>';

            for (const partNumber in grouped) {
                const item = grouped[partNumber];
                html += `<tr>`; 
                html += `<td class="copy-table-cell">
                    <span class="part-number">${partNumber}</span>
                    <i class="material-icons copy-icon" onclick="copy(this)">content_copy</i>
                    <span class="tooltip-text">Copied!</span>
                    </td>`;
                html += `<td>${item.description}</td>`;

                html += `<td style="position: relative; width: 200px;">`;
                html += `<div id="carousel${partNumber}" class="carousel slide" data-ride="carousel">`;
                html += `<div class="carousel-inner">`;

                item.images.forEach((imgSrc, index) => {
                    html += `
                    <div class="carousel-item ${index === 0 ? 'active' : ''}">
                        <img src="/image/${imgSrc.replace(/\\/g, '/')}" class="d-block w-100" style="max-width: 100%; max-height: 150px; object-fit: contain;" cursor: pointer;" onclick="openImageModal('${partNumber}', ${index})" alt="Image for ${partNumber}">
                    </div>`;
                });

                html += `</div>`;
                if (item.images.length > 1) { 
                    html += `<a class="carousel-control-prev" href="#carousel${partNumber}" role="button" data-slide="prev" style="position: absolute; top: 50%; transform: translateY(-50%); left: -10px; background: rgba(255, 255, 255, 0.5); z-index: 1;">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="sr-only">Previous</span>
                    </a>
                    <a class="carousel-control-next" href="#carousel${partNumber}" role="button" data-slide="next" style="position: absolute; top: 50%; transform: translateY(-50%); right: -10px; background: rgba(255, 255, 255, 0.5); z-index: 1;">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="sr-only">Next</span>
                    </a>`;
                }

                html += `</div>`;
                html += `</td>`;
                html += `</tr>`;
            }

            html += '</tbody>';
            html += '</table>';

            
            document.getElementById("results").innerHTML = html;
        }
        window.scrollTo({top: 0});
        
    
    });
}

const searchbar = document.getElementById('search-section');
let ogcontainer = document.getElementById('upper-container');
let originalwidth = getComputedStyle(ogcontainer).width;
const stickyPoint = searchbar.getBoundingClientRect().bottom + searchbar.ownerDocument.defaultView.pageYOffset;
window.addEventListener('scroll',
function() {
    if (window.pageYOffset > stickyPoint) {
        searchbar.classList.add('sticky');
        searchbar.style.width = originalwidth;
    } else {
        searchbar.classList.remove('sticky');
        searchbar.style.width = ''
    }

})

window.addEventListener('resize',
function() {
    originalwidth = getComputedStyle(ogcontainer).width;
    if (searchbar.classList.contains('sticky')) {
        searchbar.style.width = originalwidth;
    }
})
