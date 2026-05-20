/**
 * 
 * @param {string} tipo "password_diferentes" ou "delete" 
 * @param {*} id 
 */
function openModal(tipo="delete",id=null,entidade=null) {
    const modal             = document.getElementById("janelaModal");
    const form              = document.getElementById("deleteForm");
    let p                   = document.getElementById("textoJanelaModal");
    let bt_modal_ok         = document.getElementById("bt-modal-ok");
    let bt_modal_cancelar   = document.getElementById("bt-modal-cancelar");

    switch(tipo){
        case "password_diferentes":
            form.action  = `/utilizadores/registar`;
            p.innerText  = "As passwords não são iguais."
            form.style.display = "none";
            bt_modal_cancelar.style.display = "none";
            break;
        case "delete":
            switch(entidade){
                case "anedota":
                    form.action = `/eliminar/${id}`;
                    break;
                case "categoria":
                    form.action = `/categorias/eliminar/${id}`;
                    break;
            }
            p.innerText = `Tem a certeza que deseja eliminar esta ${entidade}?`;
            bt_modal_ok.style.display = "none";

            break;
    }
    modal.style.display = "block";
}



function closeModal() {
    document.getElementById("janelaModal").style.display = "none";
}



function verifica_passwords_iguais(){
    const p1 = document.getElementById("pass1_id").value;
    const p2 = document.getElementById("pass2_id").value;
    if(p1 != p2){
        openModal("password_diferentes");
        return false;
    }else{
        return true;
    }
}



// fechar ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById("janelaModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}



window.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            /* console.log(btn);
            console.log("Aqui"); */
            openModal("delete",this.dataset.id,this.dataset.entidade);
        });
    });
});