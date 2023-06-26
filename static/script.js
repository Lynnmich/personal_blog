//Show and hide facts
function showFact(factIndex) {
    // Get the fact element and set its text based on the fact index
    var factText = document.getElementById('factText');
    factText.innerText = 'Fact ' + factIndex + ': This is a sample fact.';
  
    // Show the fact overlay
    var factOverlay = document.getElementById('factOverlay');
    factOverlay.style.display = 'block';
  }
  
  function hideFact() {
    // Hide the fact overlay
    var factOverlay = document.getElementById('factOverlay');
    factOverlay.style.display = 'none';
  }
  