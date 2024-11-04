 
-- внутренее соединение Без условия 1 Показывает социальный статус в людей в разных городах 
SELECT filial.idcity, numclient.fio ,numclient.socialstatus
FROM filial
INNER JOIN numclient ON filial.idcity = numclient.idcity;

-- внутренее соединение без условия 2

Select agreement.amaunt, filial.name, filial.numofemploeers  
from agreement
INNER JOIN filial ON filial.id = agreement.filial

-- внутренее соединение без условия 3 

Select agreement.amaunt, agreement.typeofinsuranse, numclient.idcity
from agreement
INNER JOIN numclient ON numclient.id = agreement.client


-- ХЗ как его пока обосновать но в любом случае это внутрение сооединение с условием не по дате
Select agreement.amaunt, numclient.socialstatus ,numclient.id ,agreement.client
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE agreement.amaunt > 25000;


--лучеш наверное использовать это ну или нет посмотрим

SELECT n.*
FROM numclient n
LEFT JOIN agreement a ON n.id = a.client
WHERE a.client IS NULL;


-- Почти то же самое только показывает договоры из определенных городов тоже просто внутренее соединение с условием

Select agreement.amaunt, numclient.socialstatus ,numclient.id ,agreement.client ,numclient.idcity       
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE numclient.idcity = 'Москва'


-- ТО ЖЕ САМОЕ НО БЕЗ МУССОРА
Select agreement.amaunt, numclient.socialstatus  
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE numclient.idcity = 'Москва'


-- c условине на дату

Select agreement.amaunt, numclient.socialstatus  
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE agreement.dateofconclusion > '2015/05/07'


-- с условием на дату (а почему нееет ну почему неет)

Select agreement.amaunt, numclient.socialstatus  
from agreement
INNER JOIN numclient ON numclient.id = agreement.client
WHERE agreement.dateofconclusion < '2015/05/07'


-- левое соединение показывает всех клинетов

Select numclient.fio
from agreement
LEFT JOIN numclient ON numclient.id = agreement.client

-- праваое соединение показывает только тех с которыми уже есть договор

Select numclient.fio
from   agreement
Right JOIN numclient ON numclient.id = agreement.client;

-- запрос на запросе через левое соединение
SELECT n.id, n.fio, n.telephone, 
       COALESCE(a.filial, 0) AS branch,  -- Используем числовое значение по умолчанию
       COALESCE(a.typeofinsuranse, 'Not insured') AS insurance_type
FROM numclient n
LEFT JOIN (
    SELECT client, filial, typeofinsuranse
    FROM agreement
    GROUP BY client, filial, typeofinsuranse
) a ON n.id = a.client
WHERE a.client IS NULL;





SELECT SUM(numofemploeers)
FROM filial;

SELECT * FROM numclient;
