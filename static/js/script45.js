window.addEventListener('load',function(){

    const canvas = document.querySelector('#canvas')
    const context = canvas.getContext("2d")


    //Resizing
    canvas.height = 300
    canvas.width =  300



    // Variables
    let painting = false

    // Functions
    function startPosition(e){
        painting = true
        draw(e)
    }

    function endPosition(){
        painting = false
        context.beginPath()
    }

    function draw (e){
        if (!painting){
            return;
        }
        else {
            context.lineWidth = 10
            context.lineCap = 'round'

            context.lineTo(e.clientX-canvas.offsetLeft, e.clientY- canvas.offsetTop)
            context.stroke()
            context.beginPath()
            context.moveTo(e.clientX- canvas.offsetLeft, e.clientY- canvas.offsetTop)
        }

        
    }

    // Event Listener
    canvas.addEventListener('mousedown', startPosition)
    canvas.addEventListener('mouseup', endPosition)
    canvas.addEventListener('mousemove', draw)

    // ---------------------------------------------------------
    var ongoingTouches = [];

function handleStart(e) {
  e.preventDefault();
  console.log("touchstart.");
  var canvas = document.getElementById("canvas");
  var context = canvas.getContext("2d");
  var touches = e.changedTouches;
  context.lineWidth = 10;
  context.lineCap = 'round'

  for (var i = 0; i < touches.length; i++) {
    ongoingTouches.push(copyTouch(touches[i]));
    context.lineTo(touches[i].clientX-canvas.offsetLeft, touches[i].clientY-canvas.offsetTop)
    context.stroke()
    context.beginPath()
    context.moveTo(touches[i].clientX-canvas.offsetLeft, touches[i].clientY-canvas.offsetTop)
  }
}

function handleMove(e) {
  e.preventDefault();
  var canvas = document.getElementById("canvas");
  var context = canvas.getContext("2d");
  var touches = e.changedTouches;

  for (var i = 0; i < touches.length; i++) {
    var idx = ongoingTouchIndexById(touches[i].identifier);

    if (idx >= 0) {

      context.lineWidth = 10
      context.lineCap = 'round'
      context.lineTo(touches[i].clientX-canvas.offsetLeft, touches[i].clientY-canvas.offsetTop)
      context.stroke()
      context.beginPath()
      context.moveTo(touches[i].clientX-canvas.offsetLeft, touches[i].clientY-canvas.offsetTop)

      ongoingTouches.splice(idx, 1, copyTouch(touches[i]));  // swap in the new touch record
    } else {
      console.log("can't figure out which touch to continue");
    }
  }
}

function handleEnd(e) {
  e.preventDefault();
  var canvas = document.getElementById("canvas");
  var context = canvas.getContext("2d");
  var touches = e.changedTouches;

  for (var i = 0; i < touches.length; i++) {
    var idx = ongoingTouchIndexById(touches[i].identifier);

    if (idx >= 0) {
      context.beginPath()
      ongoingTouches.splice(idx, 1);
    } else {
      console.log("can't figure out which touch to end");
    }
  }
}

function handleCancel(e) {
  e.preventDefault();
  console.log("touchcancel.");
  var touches = e.changedTouches;

  for (var i = 0; i < touches.length; i++) {
    var idx = ongoingTouchIndexById(touches[i].identifier);
    ongoingTouches.splice(idx, 1); 
  }
}

function copyTouch({ identifier, clientX, clientY }) {
  return { identifier, clientX, clientY };
}

function ongoingTouchIndexById(idToFind) {
  for (var i = 0; i < ongoingTouches.length; i++) {
    var id = ongoingTouches[i].identifier;

    if (id == idToFind) {
      return i;
    }
  }
  return -1;  
}

  canvas.addEventListener("touchstart", handleStart, false);
  canvas.addEventListener("touchend", handleEnd, false);
  canvas.addEventListener("touchcancel", handleCancel, false);
  canvas.addEventListener("touchmove", handleMove, false);

    //---------------------------------------------------------


    //var savePredict = document.getElementById('save_predict')
    var predict  = document.getElementById('btn-predict')
    var clear = document.getElementById('btn-clear')

    clear.addEventListener('click', function(){
        var canvas = document.getElementById('canvas')
        const context = canvas.getContext("2d")
        context.clearRect(0, 0, canvas.width, canvas.height)

        var btn = document.getElementById('btn-predict')
        btn.style.display = 'block'

        var loader = document.querySelector('.loader')
        loader.style.display = 'none'

        var result = document.querySelector('#result')
        result.style.display = 'none'

        var outCanvas = document.getElementById("outCanvas");
        outCanvas.textContent = ''


    })

    predict.addEventListener('click',function(){

        var canvas = document.getElementById('canvas')
        var img = canvas.toDataURL()

        var btn = document.getElementById('btn-predict')
        btn.style.display = 'none'
        
        var loader = document.querySelector('.loader')
        loader.style.display = 'block'


        //Make prediction by calling api /predict
        async function predict(){
            try{
                const response = await fetch("/predict",{
                  method : "POST",
                  body: img
                })
                
                const data = await response.text()
                var loader = document.querySelector('.loader')
                loader.style.display = 'none'
                var result = document.querySelector('#result')
                result.style.display = 'block'
                fadeIn(result,600)
                result.textContent = 'Clear board to use again'
                var outCanvas = document.getElementById("outCanvas");
                fadeIn(outCanvas,600)
                outCanvas.textContent = data
                console.log('Success!... Result: '+data)
            }
            catch(e) {
                console.log(e)
                var loader = document.querySelector('.loader')
                loader.style.display = 'none'
                var result = document.querySelector('#result')
                fadeIn(result,600)
                result.textContent = 'Something Wrong!'
            }
        }
  
        predict()

    })



})



// ------------------------ Helper Function -------------------------------------------------------------------
function fadeIn(elem, ms) {
    elem.style.opacity = 0;
  
    if (ms) {
      let opacity = 0;
      const timer = setInterval(function() {
        opacity += 50 / ms;
        if (opacity >= 1) {
          clearInterval(timer);
          opacity = 1;
        }
        elem.style.opacity = opacity;
      }, 50);
    } else {
      elem.style.opacity = 1;
    }
  }

    
