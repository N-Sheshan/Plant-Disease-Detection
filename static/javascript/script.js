// // selecting all required elements
// const dropArea = document.querySelector(".drag-area"),
//   dragText = dropArea.querySelector("header"),
//   button = dropArea.querySelector("button"),
//   input = dropArea.querySelector("input");
// let file; // this is a global variable and we'll use it inside multiple functions

// button.onclick = () => {
//   input.click(); // if user clicks on the button then the input also clicked
// };

// input.addEventListener("change", function () {
//   // getting user selected file and [0] this means if the user selects multiple files then we'll select only the first one
//   file = this.files[0];
//   dropArea.classList.add("active");
//   showFile(); // calling function
//   // Reset input value to allow selecting the same file again
//   this.value = null;
// });

// // If user Drag File Over DropArea
// dropArea.addEventListener("dragover", (event) => {
//   event.preventDefault(); // preventing from default behavior
//   dropArea.classList.add("active");
//   dragText.textContent = "Release to Upload File";
// });

// // If user leaves dragged File from DropArea
// dropArea.addEventListener("dragleave", () => {
//   dropArea.classList.remove("active");
//   dragText.textContent = "Drag & Drop to Upload File";
// });

// // If user drops File on DropArea
// dropArea.addEventListener("drop", (event) => {
//   event.preventDefault(); // preventing from default behavior
//   // getting user selected file and [0] this means if the user selects multiple files then we'll select only the first one
//   file = event.dataTransfer.files[0];
//   showFile(); // calling function
// });

// function showFile() {
//   let fileType = file.type; // getting selected file type
//   let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; // adding some valid image extensions in array
//   if (validExtensions.includes(fileType)) {
//     // if the user selected file is an image file
//     let fileReader = new FileReader(); // creating a new FileReader object
//     fileReader.onload = () => {
//       let fileURL = fileReader.result; // passing user file source in fileURL variable
//       let imgTag = `<img src="${fileURL}" alt="">`; // creating an img tag and passing user-selected file source inside src attribute
//       dropArea.innerHTML = imgTag; // adding that created img tag inside dropArea container
//       // Reset drop area after successfully uploading the first image
//       dropArea.classList.remove("active");
//       dragText.textContent = "Drag & Drop to Upload File";
//     };
//     fileReader.readAsDataURL(file);
//   } else {
//     alert("This is not an Image File!");
//     dropArea.classList.remove("active");
//     dragText.textContent = "Drag & Drop to Upload File";
//   }
// }




document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
	const dropZoneElement = inputElement.closest(".drop-zone");

	dropZoneElement.addEventListener("click", (e) => {
		inputElement.click();
	});

	inputElement.addEventListener("change", (e) => {
		if (inputElement.files.length) {
			updateThumbnail(dropZoneElement, inputElement.files[0]);
		}
	});

	dropZoneElement.addEventListener("dragover", (e) => {
		e.preventDefault();
		dropZoneElement.classList.add("drop-zone--over");
	});

	["dragleave", "dragend"].forEach((type) => {
		dropZoneElement.addEventListener(type, (e) => {
			dropZoneElement.classList.remove("drop-zone--over");
		});
	});

	dropZoneElement.addEventListener("drop", (e) => {
		e.preventDefault();

		if (e.dataTransfer.files.length) {
			inputElement.files = e.dataTransfer.files;
			updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
		}

		dropZoneElement.classList.remove("drop-zone--over");
	});
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
 function updateThumbnail(dropZoneElement, file) {
  let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

  // First time - remove the prompt
  if (dropZoneElement.querySelector(".drop-zone__prompt")) {
    dropZoneElement.querySelector(".drop-zone__prompt").remove();
  }

  // First time - there is no thumbnail element, so let's create it
  if (!thumbnailElement) {
    thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    dropZoneElement.appendChild(thumbnailElement);
  }

  thumbnailElement.dataset.label = file.name;

  // Show thumbnail for image files
  if (file.type.startsWith("image/")) {
    const reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = () => {
      thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
    };
  } else {
    alert("This is not an Image File!");
    // Clear the drop area
    dropZoneElement.innerHTML = '<div class="drop-zone__prompt">Drop file here or click to upload</div>';
  }
}

// document.getElementById('uploadForm').addEventListener('submit', function (event) {
// 	event.preventDefault(); // Prevent the default form submission behavior
// 	// Your code to handle the form submission or any other actions
//   });
  


function handleDrop(event) {
	event.preventDefault();
	const fileInput = document.getElementById("fileInput");
	const files = event.dataTransfer.files;

	if (files.length > 0) {
		fileInput.files = files;
	}
}

function handleDragOver(event) {
	event.preventDefault();
}

function triggerFileInput() {
	const fileInput = document.getElementById("fileInput");
	const dropPrompt = document.getElementById("dropPrompt");

	fileInput.click();

	// Show the drop zone after triggering the file input
	dropPrompt.style.display = "block";
}

function submitForm() {
	const form = document.getElementById("uploadForm");
	const formData = new FormData(form);

	// Perform AJAX submission
	fetch(form.action, {
		method: form.method,
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		// Handle the response data as needed
		console.log(data);
	})
	.catch(error => {
		console.error('Error:', error);
	});
}

function displaySelectedFile() {
    var fileInput = document.getElementById('fileInput');
    var dropPrompt = document.getElementById('dropPrompt');
    dropPrompt.textContent = fileInput.files[0].name;
}
function displaySelectedImage() {
    var fileInput = document.getElementById('{{ form.image.id_for_label }}');
    var dropPrompt = document.getElementById('dropPrompt');
    var imagePreview = document.getElementById('imagePreview');

    if (fileInput.files.length > 0) {
        var reader = new FileReader();

        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            dropPrompt.textContent = '';  // Clear the prompt when an image is selected
        };

        reader.readAsDataURL(fileInput.files[0]);
    } else {
        imagePreview.src = '';
        dropPrompt.textContent = 'Drop file here or click to upload';
    }
}

function triggerFileInput() {
	document.getElementById('{{ form.image.id_for_label }}').click();
}

function handleDrop(event) {
	event.preventDefault();
	var fileInput = document.getElementById('{{ form.image.id_for_label }}');
	fileInput.files = event.dataTransfer.files;
	displaySelectedImage();
}

function handleDragOver(event) {
	event.preventDefault();
}

function displaySelectedImage() {
	var fileInput = document.getElementById('{{ form.image.id_for_label }}');
	var dropPrompt = document.getElementById('dropPrompt');
	var imagePreview = document.getElementById('imagePreview');

	if (fileInput.files.length > 0) {
		var reader = new FileReader();

		reader.onload = function(e) {
			imagePreview.src = e.target.result;
			dropPrompt.textContent = '';  // Clear the prompt when an image is selected
		};

		reader.readAsDataURL(fileInput.files[0]);
	} else {
		imagePreview.src = '';
		dropPrompt.textContent = 'Drop file here or click to upload';
	}
}