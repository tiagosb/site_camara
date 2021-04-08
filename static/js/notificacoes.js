function closeAlert() {
    console.log("Fechar o alert.");
    
    document.querySelector('.js-alert').classList.add('hidden');
    setTimeout(function(){
        document.querySelector('.js-alert').classList.add('display-none');
    }, 400);
}