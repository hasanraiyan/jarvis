$(document).ready(function () {
  // Display Speak Message
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    // Only update UI if it's AI's response (not user's input)
    if (message && !message.startsWith("You said:")) {
      $(".siri-message li:first").text(message);
      $(".siri-message").textillate("start");
      
      // Clear previous captions
      $("#caption-container").empty();
      
      // Split message into words
      const words = message.split(' ');
      let currentIndex = 0;
      
      // Function to show words in groups of 2-3
      function showNextWords() {
        if (currentIndex >= words.length) {
          setTimeout(() => {
            $("#caption-container").empty();
          }, 1500);
          return;
        }
        
        // Clear previous words
        $("#caption-container").empty();
        
        // Show next 2-3 words
        for (let i = 0; i < 3 && currentIndex + i < words.length; i++) {
          const wordSpan = $('<span>')
            .addClass('word-container')
            .text(words[currentIndex + i]);
          
          $("#caption-container").append(wordSpan);
          
          // Trigger animation with slower fade-in
          setTimeout(() => {
            wordSpan.addClass('active');
          }, 100 * i);  // Increased from 50ms to 100ms
        }
        
        currentIndex += 3;
        
        // Schedule next group of words with slower transition
        setTimeout(showNextWords, 1200); // Increased from 800ms to 1200ms
      }
      
      // Start showing words
      showNextWords();
    }
  }

  eel.expose(ShowHood);
  function ShowHood() {
    $("#Oval").attr("hidden", false);
    $("#SiriWave").attr("hidden", true);
  }

  eel.expose(senderText);
  function senderText(message) {
    // This function is called when user sends a message
    // We don't need to display it in the main interface anymore
    // as it will be saved to history and shown in the modal
    console.log("User message:", message);
  }

  eel.expose(receiverText);
  function receiverText(message) {
    // This function is called when AI responds
    // We don't need to display it in the main interface anymore
    // as it will be saved to history and shown in the modal
    console.log("AI response:", message);
  }
  eel.expose(hideLoader);
  function hideLoader() {
    $("#Loader").attr("hidden", true);
    $("#FaceAuth").attr("hidden", false);
  }
  // Hide Face auth and display Face Auth success animation
  eel.expose(hideFaceAuth);
  function hideFaceAuth() {
    $("#FaceAuth").attr("hidden", true);
    $("#FaceAuthSuccess").attr("hidden", false);
  }
  // Hide success and display
  eel.expose(hideFaceAuthSuccess);
  function hideFaceAuthSuccess() {
    $("#FaceAuthSuccess").attr("hidden", true);
    $("#HelloGreet").attr("hidden", false);
  }

  // Hide Start Page and display blob
  eel.expose(hideStart);
  function hideStart() {
    $("#Start").attr("hidden", true);

    setTimeout(function () {
      $("#Oval").addClass("animate__animated animate__zoomIn");
    }, 1000);
    setTimeout(function () {
      $("#Oval").attr("hidden", false);
    }, 1000);
  }
});