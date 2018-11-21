var viewingHints = false;
var solutionIndex = 0;
var hintIndex = 0;

document.getElementById('hints-button').onclick = function() {
  showAllHints(true, 'rotateHint');
  document.getElementById('hint0').style.visibility = 'visible';
  hintIndex = 1;
};

document.getElementById('front-button').onclick = function() {
  hideChildren(document.getElementById('hints'), 'hint');
  showAllHints(false, 'rotateHint');
};

var showAllHints = function(show, rotate) {
  if (show) {
    document.getElementById('front-inner-content').style.display = 'none';
    document.getElementById('hints-button').style.display = 'none';
    document.getElementById('hints').style.display = 'inline';
    document.getElementById('front-button').style.display = 'inline';
  } else { // hide
    document.getElementById('front-inner-content').style.display = 'inline';
    document.getElementById('hints-button').style.display = 'inline';
    document.getElementById('hints').style.display = 'none';
    document.getElementById('front-button').style.display = 'none';
  }
  document.getElementById('flipper').classList.toggle(rotate);
  viewingHints = show;
};

var hideChildren = function(ele, id) {
    for (var index = 0; index < ele.childElementCount; index++) {
      document.getElementById(id + index).style.visibility = 'hidden';
    }
}

var showNextHint = function() {
    var hintsDiv = document.getElementById('hints');
    if (hintIndex < hintsDiv.childElementCount) {
      document.getElementById('hint' + hintIndex).style.visibility = 'visible';
      hintIndex += 1;
    }
}

var resetCard = function() {
    solutionIndex = 0;
    showAllHints(false, 'rotateBack');
    hideChildren(document.getElementById('back-inner-content'), 'solution');
    document.getElementById('ranking').style.visibility = 'hidden';
}

var revealBack = function() {
    document.getElementById('flipper').classList.toggle('rotateBack');
}

var updateSolution = function() {
    var solutionElementCount = document.getElementById('back-inner-content').childElementCount;
    if (solutionIndex == solutionElementCount) {
        resetCard();
        return;
    }

    if (solutionIndex == solutionElementCount - 1) { // show ranks on revealing last piece of solution
        document.getElementById('ranking').style.visibility = 'visible';
    }
    if (solutionIndex === 0) { // flip to back!
        revealBack();
    }

    // show the next piece of the solution
    document.getElementById('solution' + solutionIndex).style.visibility = 'visible';
    solutionIndex += 1;
}

var handleClick = function() {
    if (viewingHints) {
      showNextHint();
      return;
    }
    updateSolution();
}

// document.getElementById('front-content').onclick = handleClick;
// document.getElementById('back-content').onclick = handleClick;
