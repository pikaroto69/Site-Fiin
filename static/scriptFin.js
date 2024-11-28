window.addEventListener('load', function() {
    const alertMensagem = document.querySelector('.alert');

    setTimeout(function() {
        alertMensagem.remove();
    }, 3900);
});


const novaTrans = document.getElementById('novaTransacaoBtn')
const modal = document.getElementById('modalNovaTransacao')
const closeBtn = document.getElementById('closeModal')

const modalEdit = document.getElementById('modalEditaTransacao')
const closeEdit = document.getElementById('closeModalEdita')

novaTrans.addEventListener('click', () => {
    modal.style.display = 'flex';
})
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
})

closeEdit.addEventListener('click', () => {
    modalEdit.style.display = 'none'  
})
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none'
})

document.getElementById('saidaBtn').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('transacaoForm').action = "/nova_transacao/saida";
    document.getElementById('transacaoForm').submit();
});

document.getElementById('entradaBtn').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('transacaoForm').action = "/nova_transacao/entrada";
    document.getElementById('transacaoForm').submit();
});

const formEditar = document.getElementById('form-editar');

document.getElementById('salvarEdicaoBtn').addEventListener('click', function(event) {
    event.preventDefault(); // Evita comportamento padrão do botão
    formEditar.action = "/editar_transacao"; // Define a ação do formulário
    formEditar.submit(); // Submete o formulário
}); // <-- Fecha o addEventListener corretamente

document.getElementById('excluirEdicaoBtn').addEventListener('click', function(event) {
    event.preventDefault(); // Evita comportamento padrão do botão
    formEditar.action = "/excluir_transacao"; // Define a ação do formulário
    formEditar.submit(); // Submete o formulário
});


function selectListaDespesa() {
    const listaReceita = document.getElementById('lista-receita');
    const listaDespesa = document.getElementById('lista-despesa');

    const divSelectReceita = document.getElementById('div-select-receita');
    const divSelectDespesa = document.getElementById('div-select-despesa');

    if (window.getComputedStyle(listaDespesa).display == 'none') {
        listaDespesa.style.display = 'block';
        listaReceita.style.display = 'none';
        divSelectReceita.style.backgroundColor = '#302F36'; // Cinza
        divSelectDespesa.style.backgroundColor = '#ff546b'; // Vermelho
    }
}

function selectListaReceita() {
    const listaReceita = document.getElementById('lista-receita');
    const listaDespesa = document.getElementById('lista-despesa');

    const divSelectReceita = document.getElementById('div-select-receita');
    const divSelectDespesa = document.getElementById('div-select-despesa');

    if (window.getComputedStyle(listaReceita).display == 'none') {
        listaDespesa.style.display = 'none';
        listaReceita.style.display = 'block';
        divSelectReceita.style.backgroundColor = '#00B27E';
        divSelectDespesa.style.backgroundColor = '#302F36';
    }
}

function abrirEditar(fonte, valor, data, id_transacao, tipo) {
    const modalEditar = document.getElementById('modalEditaTransacao');

    const inputFonte = document.getElementById('descricao_edit');
    const inputValor = document.getElementById('preco_edit');
    const inputData = document.getElementById('data_edit');
    const inputID = document.getElementById('id_edit');
    const inputTipo = document.getElementById('tipo_edit');

    inputFonte.value = fonte;
    inputValor.value = valor;
    inputData.value = data;
    inputID.value = id_transacao;
    inputTipo.value = tipo;

    modalEditar.style.display = 'flex';
}
