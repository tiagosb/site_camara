function changeFont(op) {
    const body = document.querySelector('html');
    let size = parseInt(body.style.fontSize.replace("px",""));

    if(!size) {
        size = 16;
    }

    if(op == 'n') {
        body.style.fontSize = "16px";
    }
    else if(op == '+') {
        if(size<34){
            body.style.fontSize = size+1+"px";
        }
    } else {
        if(size>6){
            body.style.fontSize = size-1+"px";
        }
    }
}

function changeSchema() {
    const header = document.querySelector(".cabecalho");
    const btnMenu = document.querySelector(".btn-menu");
    const acessibilidadeTolls = document.querySelector(".acessibilidade-toll");
    const rodape = document.querySelector(".rodape");
    const html = document.querySelector("html");

    if(header.classList.contains("bg-color-acessibilidade")) {
        header.classList.remove("bg-color-acessibilidade");
        btnMenu.classList.remove("btn-menu-acessibilidade");
        acessibilidadeTolls.classList.remove("bg-color-acessibilidade");
        rodape.classList.remove("bg-color-acessibilidade");
        html.classList.remove("bg-color-acessibilidade");
        html.classList.remove("acessibilidade-contraste");
    } else {
        header.classList.add("bg-color-acessibilidade");
        btnMenu.classList.add("btn-menu-acessibilidade");
        acessibilidadeTolls.classList.add("bg-color-acessibilidade");
        rodape.classList.add("bg-color-acessibilidade");
        html.classList.add("bg-color-acessibilidade");
        html.classList.add("acessibilidade-contraste");
    }

    
}

document.addEventListener("DOMContentLoaded", function (){
    
    const $btnMenu = document.querySelector(".btn-menu");
    const $menu = document.querySelector(".menu");

    $btnMenu.addEventListener("click", function (){
        if($menu.classList.contains("aberto")) {
            $menu.classList.remove("aberto");
        } else {
            $menu.classList.add("aberto");
        }
    });
    
    // Comportamento dos inputs de estado
    document.querySelectorAll(".toggle-label").forEach(label => {
        if(label.control.checked) {
            label.classList.add('toggle-on');
        }
        label.addEventListener('click', function (event){
            const target = event.target;
            if(target.classList.contains('toggle-on')) {
                target.classList.remove('toggle-on');
            }else{
                target.classList.add('toggle-on');
            }
        }); 
    });
});

