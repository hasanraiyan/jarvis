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

  // Face Setup Functions
  eel.expose(showFaceSetup);
  function showFaceSetup() {
    $("#Loader").attr("hidden", true);
    $("#FaceAuth").attr("hidden", true);
    $("#FaceSetup").attr("hidden", false);
  }

  eel.expose(hideFaceSetup);
  function hideFaceSetup() {
    $("#FaceSetup").attr("hidden", true);
  }

  eel.expose(showFaceAuth);
  function showFaceAuth() {
    $("#Loader").attr("hidden", true);
    $("#FaceSetup").attr("hidden", true);
    $("#FaceAuth").attr("hidden", false);
  }

  eel.expose(showFaceAuthSuccess);
  function showFaceAuthSuccess() {
    $("#FaceAuth").attr("hidden", true);
    $("#FaceAuthSuccess").attr("hidden", false);
  }

  eel.expose(showAuthRetryButtons);
  function showAuthRetryButtons() {
    $("#retryAuthBtn").attr("hidden", false);
    $("#resetAuthBtn").attr("hidden", false);
  }

  // Face Setup Event Handlers
  $("#startSetupBtn").click(function() {
    startFaceSetup();
  });

  $("#skipSetupBtn").click(function() {
    eel.skip_face_setup()().then(function(result) {
      console.log("Setup skipped:", result);
    });
  });

  $("#retryAuthBtn").click(function() {
    $("#retryAuthBtn").attr("hidden", true);
    $("#resetAuthBtn").attr("hidden", true);
    eel.authenticate_face()().then(function(result) {
      if (!result.success) {
        $("#retryAuthBtn").attr("hidden", false);
        $("#resetAuthBtn").attr("hidden", false);
      }
    });
  });

  $("#resetAuthBtn").click(function() {
    if (confirm("Are you sure you want to reset face authentication? You'll need to set it up again.")) {
      eel.reset_face_auth()().then(function(result) {
        if (result.success) {
          location.reload(); // Reload to start fresh
        } else {
          alert("Failed to reset: " + result.message);
        }
      });
    }
  });

  function startFaceSetup() {
    // Show video and progress
    $("#setupVideo").attr("hidden", false);
    $("#setupProgress").attr("hidden", false);
    $("#startSetupBtn").prop("disabled", true);
    
    // Get camera access
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        const video = document.getElementById('setupVideo');
        video.srcObject = stream;
        
        // Wait for video to be ready
        video.addEventListener('loadedmetadata', function() {
          // Create canvas for capturing frames
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          
          let sampleCount = 0;
          const totalSamples = 30;
          const capturedImages = [];
          
          const captureInterval = setInterval(function() {
            // Capture frame from video
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL('image/jpeg', 0.8);
            capturedImages.push(imageData);
            
            sampleCount++;
            const progress = (sampleCount / totalSamples) * 100;
            
            $("#setupProgressBar").css("width", progress + "%");
            $("#sampleCount").text(sampleCount);
            
            if (sampleCount >= totalSamples) {
              clearInterval(captureInterval);
              
              // Stop camera
              stream.getTracks().forEach(track => track.stop());
              $("#setupVideo").attr("hidden", true);
              
              // Show processing message
              $("#sampleCount").text("Processing images...");
              
              // Send captured images to backend
              eel.setup_face_auth_with_images(capturedImages)().then(function(result) {
                if (result.success) {
                  $("#sampleCount").text("Setup completed!");
                  setTimeout(function() {
                    $("#FaceSetup").attr("hidden", true);
                    $("#FaceAuth").attr("hidden", false);
                    
                    // Start authentication
                    eel.authenticate_face()();
                  }, 1500);
                } else {
                  alert("Setup failed: " + result.message);
                  $("#startSetupBtn").prop("disabled", false);
                  $("#setupProgress").attr("hidden", true);
                  $("#setupVideo").attr("hidden", true);
                  $("#setupProgressBar").css("width", "0%");
                  $("#sampleCount").text("0");
                }
              }).catch(function(error) {
                console.error("Setup error:", error);
                alert("An error occurred during setup. Please try again.");
                $("#startSetupBtn").prop("disabled", false);
                $("#setupProgress").attr("hidden", true);
                $("#setupVideo").attr("hidden", true);
                $("#setupProgressBar").css("width", "0%");
                $("#sampleCount").text("0");
              });
            }
          }, 200); // Capture every 200ms
        });
        
      })
      .catch(function(error) {
        console.error("Camera access denied:", error);
        alert("Camera access is required for face authentication setup.");
        $("#startSetupBtn").prop("disabled", false);
      });
  }
});