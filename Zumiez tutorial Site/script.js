// script.js (partial)
// Tutorial data array: each tutorial has a title and steps (image + annotation text)
const tutorials = [
    {
      title: "How to build a board",
      steps: [
        { image: "assets/images/build_board_step1.jpg", text: "Step 1: Gather all necessary tools and materials." },
        { image: "assets/images/build_board_step2.jpg", text: "Step 2: Align the board components as shown." },
        { image: "assets/images/build_board_step3.jpg", text: "Step 3: Fasten the pieces together securely." }
      ]
    },
    {
      title: "How to print out tax forms",
      steps: [
        { image: "assets/images/print_tax_step1.jpg", text: "Step 1: Navigate to the tax form menu on the POS." },
        { image: "assets/images/print_tax_step2.jpg", text: "Step 2: Select the form needed and hit 'Print'." }
        // (additional steps can be added here)
      ]
    },
    {
      title: "How to change out the POS paper",
      steps: [
        { image: "assets/images/change_pos_paper1.jpg", text: "Step 1: Open the printer cover by pressing the latch." },
        { image: "assets/images/change_pos_paper2.jpg", text: "Step 2: Remove the empty paper roll and insert a new roll." }
      ]
    },
    {
      title: "How to do a basic refund",
      steps: [
        { image: "assets/images/basic_refund1.jpg", text: "Step 1: Press the 'Refund' button on the main screen." },
        { image: "assets/images/basic_refund2.jpg", text: "Step 2: Scan the item or enter the receipt number." }
      ]
    },
    {
      title: "How to do a refund with no receipt",
      steps: [
        { image: "assets/images/no_receipt_refund1.jpg", text: "Step 1: Select 'No Receipt' option on the refund screen." },
        { image: "assets/images/no_receipt_refund2.jpg", text: "Step 2: Manually search the transaction by date or item." }
      ]
    },
    {
      title: "How to change roll in markdown gun",
      steps: [
        { image: "assets/images/markdown_gun_roll1.jpg", text: "Step 1: Open the markdown gun by lifting the cover." },
        { image: "assets/images/markdown_gun_roll2.jpg", text: "Step 2: Remove the old label roll and insert a new one." }
      ]
    },
    {
      title: "How to change roll in a tape gun",
      steps: [
        { image: "assets/images/tape_gun_roll1.jpg", text: "Step 1: Slide out the tape holder and remove the empty roll." },
        { image: "assets/images/tape_gun_roll2.jpg", text: "Step 2: Place a new tape roll onto the holder and secure it." }
      ]
    },
    {
      title: "How to do a SOLG order",
      steps: [
        { image: "assets/images/solg_order1.jpg", text: "Step 1: On the register, go to the special orders menu." },
        { image: "assets/images/solg_order2.jpg", text: "Step 2: Enter the customer's information and order details." }
      ]
    }
  ];

  
  let currentStep = 0;

// Function to open a tutorial gallery
function openTutorial(tutorialIndex) {
  const gallerySection = document.getElementById('gallerySection');
  const tutorial = tutorials[tutorialIndex];
  if (!tutorial) return;
  
  // Build the gallery inner HTML
  let galleryHTML = "";
  // Title of the tutorial
  galleryHTML += `<h2 class="text-3xl font-bold mb-6 text-center">${tutorial.title}</h2>`;
  // Container for slides (relative positioning for overlap)
  galleryHTML += `<div class="relative overflow-hidden mb-4">`;
  tutorial.steps.forEach((step, idx) => {
    // Each step container is absolutely positioned to overlap, only the active one will be visible
    galleryHTML += `
      <div class="tutorial-step absolute inset-0 flex flex-col items-center justify-center 
                  transition-opacity duration-500 ${idx === 0 ? 'opacity-100' : 'opacity-0'}">
        <img src="${step.image}" alt="Step ${idx+1}" 
             class="max-h-96 mb-4 rounded shadow-2xl transform ${idx === 0 ? 'scale-100' : 'scale-95'}" />
        <div class="text-center text-lg bg-black bg-opacity-50 text-white px-4 py-2 rounded">
          ${step.text}
        </div>
      </div>`;
  });
  galleryHTML += `</div>`;
  // Navigation buttons
  galleryHTML += `
    <div class="flex items-center justify-between">
      <button onclick="prevStep()" class="px-4 py-2 bg-gray-700 text-white rounded 
                                     hover:bg-pink-600 transition">&#8592; Prev</button>
      <button onclick="nextStep()" class="px-4 py-2 bg-gray-700 text-white rounded 
                                     hover:bg-pink-600 transition">Next &#8594;</button>
    </div>`;
  // Back-to-home link
  galleryHTML += `
    <div class="mt-6 text-center">
      <a href="#" onclick="closeGallery()" class="text-pink-400 underline hover:text-pink-200">
        &larr; Back to tutorial list
      </a>
    </div>`;

  // Inject the HTML into the gallery section
  gallerySection.innerHTML = galleryHTML;
  // Show the gallery section
  gallerySection.classList.remove('hidden');
  // Optionally, hide the tutorial list (we can hide the UL or entire main, but we'll just hide the list here)
  document.querySelector('ul').classList.add('hidden');
  
  currentStep = 0;  // reset current step index for this tutorial
}

// Functions for navigation
function showStep(index) {
  const steps = document.querySelectorAll('.tutorial-step');
  if (!steps.length) return;
  // Wrap index for safety (cyclic rotation)
  if (index < 0) index = steps.length - 1;
  if (index >= steps.length) index = 0;
  currentStep = index;
  steps.forEach((stepElem, idx) => {
    if (idx === currentStep) {
      stepElem.classList.remove('opacity-0');
      stepElem.classList.add('opacity-100', 'scale-100');
    } else {
      stepElem.classList.remove('opacity-100', 'scale-100');
      stepElem.classList.add('opacity-0', 'scale-95');
    }
  });
}
function nextStep() {
  showStep(currentStep + 1);
}
function prevStep() {
  showStep(currentStep - 1);
}

// Function to close gallery and return to home list
function closeGallery() {
  document.getElementById('gallerySection').classList.add('hidden');
  document.querySelector('ul').classList.remove('hidden');
  // Optionally clear gallery content to free memory (not necessary here)
  // document.getElementById('gallerySection').innerHTML = "";
  return false; // prevent default link navigation
}