$(document).ready(function () {

  eel.init()();
  $(".text").textillate({
    loop: true,
    speed: 1500,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });

  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOutUp",
      sync: true,
    },
  });

  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 940,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    height: 200,
    autostart: true,
    waveColor: "#ff0000",
    waveOffset: 0,
    rippleEffect: true,
    rippleColor: "#ffffff",
  });

  $("#MicBtn").click(function () {
    eel.play_assistant_sound();
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);

    eel.takeAllCommands()
      .then((response) => {
        if (response && response.value) {
          console.log("Python response:", response.value);
          // handle response.value if needed
        } else {
          console.log("No response value received from Python");
        }
      })
      .catch((err) => {
        console.error("Error calling takeAllCommands:", err);
      });
  });

  function doc_keyUp(e) {
    if (e.key === "j" && e.metaKey) {
      eel.play_assistant_sound();
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.takeAllCommands()
        .then((response) => {
          if (response && response.value) {
            console.log("Python response:", response.value);
          } else {
            console.log("No response value received from Python");
          }
        })
        .catch((err) => {
          console.error("Error calling takeAllCommands:", err);
        });
    }
  }
  document.addEventListener("keyup", doc_keyUp, false);

  function PlayAssistant(message) {
    if (message != "") {
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.takeAllCommands(message)
        .then((response) => {
          if (response && response.value) {
            console.log("Python response:", response.value);
          } else {
            console.log("No response value received from Python");
          }
        })
        .catch((err) => {
          console.error("Error calling takeAllCommands:", err);
        });

      $("#chatbox").val("");
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    } else {
      console.log("Empty message, nothing sent."); // Log if the message is empty
    }
  }

  function ShowHideButton(message) {
    if (message.length == 0) {
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    } else {
      $("#MicBtn").attr("hidden", true);
      $("#SendBtn").attr("hidden", false);
    }
  }

  $("#chatbox").keyup(function () {
    let message = $("#chatbox").val();
    console.log("Current chatbox input: ", message); // Log input value for debugging
    ShowHideButton(message);
  });

  $("#SendBtn").click(function () {
    let message = $("#chatbox").val();
    PlayAssistant(message);
  });

  $("#chatbox").keypress(function (e) {
    let key = e.which;
    if (key == 13) {
      let message = $("#chatbox").val();
      PlayAssistant(message);
    }
  });
});
