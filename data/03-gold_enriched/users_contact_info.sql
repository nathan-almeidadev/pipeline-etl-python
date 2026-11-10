-- Query para informacoes de contato do usuario: 
SELECT 
    u.id, 
    u.nome, 
    u.email, 
    ci.ddd, 
    u.telefone, 
    u.data_nascimento, 
    ci.uf, 
    u.genero
FROM users as u
LEFT JOIN cep_info as ci   
    ON ci.cep = u.cep
ORDER BY u.id;