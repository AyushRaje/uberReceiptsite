// JavaScript (script.js)
const pdfExcelContainer = document.getElementById('pdfExcelContainer');
const convertButton = document.getElementById('convertButton');
const downloadButtonContainer = document.getElementById('downloadButtonContainer');
const downloadButton = document.getElementById('downloadButton');
const downloadLink = document.getElementById('downloadLink');

const dropContainer = document.getElementById('dropContainer');
const fileInput = document.getElementById("pdfFileInput");
const fileLabel = document.getElementById("pdfinputlabel")


convertButton.addEventListener('click', async () => {
    const pdfFile = document.getElementById('pdfFileInput').files[0];

    if (!pdfFile) {
        alert('Please select a PDF file.');
        return;
    }

    const formData = new FormData();
    formData.append('pdfFile', pdfFile);

    const response = await fetch('/convert', {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        // PDF to Excel conversion was successful.
        const excelFilePath = await response.text();
        alert('Conversion successful!');
        
        // Display the Excel file in the PDF/Excel container.
        // pdfExcelContainer.innerHTML = `<iframe src="${"/static/output.xlsx"}" width="100%" height="500"></iframe>`;
        document.getElementById('pdfFileInput').value = '';
        // Show the download button and link it to the Excel file.
        downloadButtonContainer.style.display = 'block';
        downloadButton.addEventListener('click', () => {
            window.location.href = "/static/output.xlsx";
        });
    } else {
        // PDF to Excel conversion failed.
        const data = await response.json();
        alert(data.message);
    }
});

dropContainer.addEventListener("dragover",function(e){
    e.preventDefault();
    dropContainer.classList.add("drag-over");
});
dropContainer.addEventListener("dragleave", function (e) {
    e.preventDefault();
    dropContainer.classList.remove("drag-over");
});
dropContainer.addEventListener("drop", function (e) {
    e.preventDefault();
    dropContainer.classList.remove("drag-over");

    const droppedFile = e.dataTransfer.files[0];

    if (droppedFile) {
        fileInput.files = e.dataTransfer.files; // Set the selected file in the input element
        fileLabel.textContent = droppedFile.name;
    }
});