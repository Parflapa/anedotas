
function openModal(id) {
    const modal = document.getElementById("deleteModal");
    const form = document.getElementById("deleteForm");

    form.action = `/anedotas/eliminar/${id}`;

    modal.style.display = "block";
}



function closeModal() {
    document.getElementById("deleteModal").style.display = "none";
}



// fechar ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById("deleteModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

window.onload = function() {
    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            console.log(btn);
            console.log("Aqui");
            openModal(this.dataset.id);
        });
    });
}