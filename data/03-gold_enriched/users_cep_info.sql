-- Query para informacoes sobre o endereco do usuario:
SELECT 
    u.id, 
    u.nome, 
    u.data_nascimento, 
    u.genero, 
    u.cep, 
    ci.logradouro, 
    ci.complemento, 
    ci.bairro, 
    ci.localidade as cidade, 
    ci.uf, 
    ci.estado, 
    ci.regiao, 
    ci.ibge, 
    ci.gia, 
    ci.siafi
FROM users as u
LEFT JOIN cep_info as ci
    ON  u.cep = ci.cep
ORDER BY u.id;
