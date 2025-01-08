CREATE DATABASE projeto_ppc;
USE projeto_ppc;

CREATE TABLE pessoa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    papel ENUM('Coordenador', 'Colaborador', 'Avaliador') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE ppc (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    status ENUM('Em Criacao', 'Em Avaliacao', 'Aprovado') DEFAULT 'Em Criacao',
    motivo_rejeicao TEXT, -- Justificativa caso o PPC seja rejeitado
    coordenador_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (coordenador_id) REFERENCES pessoa(id)
);

CREATE TABLE ppc_colaboradores (
    ppc_id INT NOT NULL,
    colaborador_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ppc_id, colaborador_id),
    FOREIGN KEY (ppc_id) REFERENCES ppc(id) ON DELETE CASCADE,
    FOREIGN KEY (colaborador_id) REFERENCES pessoa(id) ON DELETE CASCADE
);

CREATE TABLE ppc_avaliadores (
    ppc_id INT NOT NULL,
    avaliador_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ppc_id, avaliador_id),
    FOREIGN KEY (ppc_id) REFERENCES ppc(id) ON DELETE CASCADE,
    FOREIGN KEY (avaliador_id) REFERENCES pessoa(id) ON DELETE CASCADE
);

CREATE TABLE relatorio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ppc_id INT NOT NULL,
    titulo_ppc VARCHAR(200),
    descricao_ppc TEXT,
    status_ppc ENUM('Em Criacao', 'Em Avaliacao', 'Aprovado'),
    motivo_rejeicao TEXT, -- Inclui justificativa se o PPC foi rejeitado
    coordenador_nome VARCHAR(100),
    coordenador_email VARCHAR(100),
    colaboradores TEXT, -- Lista de colaboradores (nome + e-mail)
    avaliadores TEXT, -- Lista de avaliadores (nome + e-mail)
    total_colaboradores INT,
    total_avaliadores INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ppc_id) REFERENCES ppc(id) ON DELETE CASCADE
);

CREATE TABLE estrategia_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome ENUM('Em Criacao', 'Em Avaliacao', 'Aprovado') NOT NULL,
    descricao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE PROCEDURE gerar_relatorio_por_ppc(ppc_id INT)
BEGIN
    INSERT INTO relatorio (
        ppc_id, 
        titulo_ppc, 
        descricao_ppc, 
        status_ppc, 
        motivo_rejeicao, 
        coordenador_nome, 
        coordenador_email, 
        colaboradores, 
        avaliadores, 
        total_colaboradores, 
        total_avaliadores
    )
    SELECT 
        p.id AS ppc_id,
        p.titulo AS titulo_ppc,
        p.descricao AS descricao_ppc,
        p.status AS status_ppc,
        p.motivo_rejeicao,
        coord.nome AS coordenador_nome,
        coord.email AS coordenador_email,
        GROUP_CONCAT(DISTINCT CONCAT(col.nome, ' (', col.email, ')') SEPARATOR ', ') AS colaboradores,
        GROUP_CONCAT(DISTINCT CONCAT(av.nome, ' (', av.email, ')') SEPARATOR ', ') AS avaliadores,
        COUNT(DISTINCT col.id) AS total_colaboradores,
        COUNT(DISTINCT av.id) AS total_avaliadores
    FROM ppc p
    LEFT JOIN pessoa coord ON p.coordenador_id = coord.id
    LEFT JOIN ppc_colaboradores pc ON p.id = pc.ppc_id
    LEFT JOIN pessoa col ON pc.colaborador_id = col.id
    LEFT JOIN ppc_avaliadores pa ON p.id = pa.ppc_id
    LEFT JOIN pessoa av ON pa.avaliador_id = av.id
    WHERE p.id = ppc_id
    GROUP BY p.id;
END$$

DELIMITER ;

