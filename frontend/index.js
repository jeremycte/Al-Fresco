const buttons = document.querySelectorAll(".card-buttons button");
const sections = document.querySelectorAll(".card-section");
const card = document.querySelector(".card");

const handleButtonClick = e => {
  const targetSection = e.target.getAttribute("data-section");
  const section = document.querySelector(targetSection);
  targetSection !== "#about" ?
  card.classList.add("is-active") :
  card.classList.remove("is-active");
  card.setAttribute("data-state", targetSection);
  sections.forEach(s => s.classList.remove("is-active"));
  buttons.forEach(b => b.classList.remove("is-active"));
  e.target.classList.add("is-active");
  section.classList.add("is-active");
};

buttons.forEach(btn => {
  btn.addEventListener("click", handleButtonClick);
});

var worktgtbtn = document.querySelector(".contact-me").addEventListener("click", handleContactBtn)
var learnmorebtn = document.querySelector(".learn-more").addEventListener("click", handleLearnMoreBtn)
var freshmankitbtn = document.querySelector(".freshman-kit").addEventListener("click", handleFreshmanKitBtn)
var emcccrewbtn = document.querySelector(".emcc-crew").addEventListener("click", handleEMCCCrewBtn)
var dscnusbtn = document.querySelector(".dsc-nus").addEventListener("click", handleDSCNUSBtn)

function handleContactBtn(){
    window.location.href = "https://t.me/abhishekjain";
};

function handleLearnMoreBtn(){
  window.location.href = "https://google.com";
}

function handleFreshmanKitBtn(){
  window.location.href = "https://nuscomputingfreshmankit.surge.sh";
}

function handleEMCCCrewBtn() {
  window.location.href = "https://github.com/jeremycte/hacknroll2021"
}

function handleDSCNUSBtn() {
  window.location.href = "https://t.me/abhishekjain"
}