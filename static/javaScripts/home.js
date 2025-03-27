// Exemple de fonction de survol pour les boutons
document.querySelectorAll(".image-box").forEach((item) => {
  item.addEventListener("mouseover", () => {
    item.style.transform = "scale(1.05)";
  });
  item.addEventListener("mouseout", () => {
    item.style.transform = "scale(1)";
  });
});

// home.js

// Fonction pour gérer l'ouverture/fermeture des menus déroulants
document.addEventListener("DOMContentLoaded", function () {
  const dropdownButton = document.querySelector(".dropdown button");
  const dropdownContent = document.querySelector(".dropdown-content");

  dropdownButton?.addEventListener("click", function () {
    dropdownContent.style.display =
      dropdownContent?.style?.display === "block" ? "none" : "block";
  });

  // Cacher le menu lorsqu'on clique en dehors de celui-ci
  document.addEventListener("click", function (event) {
    if (
      !dropdownButton?.contains(event.target) &&
      !dropdownContent?.contains(event.target)
    ) {
      dropdownContent?.style.display = "none";
    }
  });
});
