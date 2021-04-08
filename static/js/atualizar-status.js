async function alterarStatus(event) {
    const postId = event.id;
    const status = event.checked ? 1 : 0;
    const rota = event.dataset['rota'];

    
    const req = await fetch(rota, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: postId})
    });

    if(!req.ok){
        console.error("Não foi possível alterar o status..");
        event.checked = !status;
    } else {
        console.log("Ok, status alterado.");
        console.log(await req.json())
    }
}