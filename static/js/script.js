const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");

const togglerElements = document.querySelectorAll("#accordionToggler");

// Add a click event listener to each 'accordionToggler' element
togglerElements.forEach((element) => {
	element.addEventListener("click", function () {
		// Find the parent 'chapter' div of the clicked element
		const parentChapter = element.closest(".chapter");

		// Toggle the 'active' class on the 'chapter-body' div within the parent chapter
		const chapterBody = parentChapter.querySelector(".chapter-body");
		chapterBody.classList.toggle("is-open");

		// Change the content inside the clicked element based on its current state
		if (element.textContent.trim() === "expand_more") {
			element.textContent = "expand_less";
		} else {
			element.textContent = "expand_more";
		}

		// Close other open accordions
		const allChapters = document.querySelectorAll(".chapter");
		allChapters.forEach((chapter) => {
			if (chapter !== parentChapter) {
				const otherChapterBody = chapter.querySelector(".chapter-body");
				const otherToggler = chapter.querySelector("#accordionToggler");

				// Close other chapter bodies and reset their toggler text
				otherChapterBody.classList.remove("is-open");
				otherToggler.textContent = "expand_more";
			}
		});
	});
});

// Show sidebar
menuBtn.addEventListener("click", () => {
	sideMenu.style.display = "block";
});

// Close sidebar
closeBtn.addEventListener("click", () => {
	sideMenu.style.display = "none";
});

// Title

let currentIndex = 0;
const titles = document.querySelectorAll(".title");
const previousButtons = document.querySelectorAll(".previous-button");
const nextButtons = document.querySelectorAll(".next-button");

function showTitle(direction) {
	titles[currentIndex].classList.remove("active");

	if (direction === "next") {
		currentIndex = (currentIndex + 1) % titles.length;
	} else if (direction === "previous") {
		currentIndex = (currentIndex - 1 + titles.length) % titles.length;
	}

	titles[currentIndex].classList.add("active");
	updateButtonState();
}

function updateButtonState() {
	previousButtons.forEach((button) => (button.disabled = currentIndex === 0));
	nextButtons.forEach((button) => (button.disabled = currentIndex === titles.length - 1));
}

// Initialize button state
updateButtonState();
