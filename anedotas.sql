-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 29-Jun-2026 às 16:02
-- Versão do servidor: 10.4.32-MariaDB
-- versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `anedotas`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `anedotas`
--

CREATE TABLE `anedotas` (
  `id_a` int(11) NOT NULL,
  `texto_a` text NOT NULL,
  `data_a` date NOT NULL,
  `utilizador_a` int(11) NOT NULL,
  `visualizacoes_a` int(11) NOT NULL,
  `votos_a` int(11) NOT NULL,
  `categoria_a` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `anedotas`
--

INSERT INTO `anedotas` (`id_a`, `texto_a`, `data_a`, `utilizador_a`, `visualizacoes_a`, `votos_a`, `categoria_a`) VALUES
(1, 'A mãe e a filha estão a dormir no corredor. Que horas são?\n– Falta um quarto para as duas\n', '2026-04-01', 1, 14, 12, 1),
(2, 'Como fazer com que um avião não caia?\r\n- Lavar o avião com shampoo anti-queda.\r\n', '2026-04-02', 2, 13, 8, 1),
(3, 'Onde vão as cobras para beber um copo no fim de um dia de trabalho?\r\n– Ao snake-bar.', '2026-04-03', 2, 12, 7, 1),
(4, 'O mito mais enganador sobre criaturas sobrenaturais é o que afirma que os vampiros penas bebem sangue. Eles também comem bolachas, mas não podem ser quaisquer umas. Só comem bolachas d’aveia.\r\n', '2026-04-29', 3, 31, 24, 1),
(5, 'Num certo dia, depois de vir da escola o filho pergunta à mãe: \n- É verdade que descendemos de macacos?\n- Não sei filho, o teu pai nunca me apresentou a família dele.\n', '2026-04-29', 1, 10, 18, 1),
(6, 'Por que é que os Alentejanos semeiam alhos nas bermas das estradas?\r\nPorque o alho faz bem à circulação.', '2026-04-15', 3, 3, 10, 6);

-- --------------------------------------------------------

--
-- Estrutura da tabela `categorias`
--

CREATE TABLE `categorias` (
  `id_c` int(11) NOT NULL,
  `nome_c` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `categorias`
--

INSERT INTO `categorias` (`id_c`, `nome_c`) VALUES
(1, 'Curtas'),
(2, 'Parvas'),
(3, 'Adultos'),
(4, 'Escola'),
(5, 'Tecnologia'),
(6, 'Regionalistas');

-- --------------------------------------------------------

--
-- Estrutura da tabela `paises`
--

CREATE TABLE `paises` (
  `id_p` int(11) NOT NULL,
  `nome_p` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `paises`
--

INSERT INTO `paises` (`id_p`, `nome_p`) VALUES
(1, 'Portugal'),
(2, 'Brasil');

-- --------------------------------------------------------

--
-- Estrutura da tabela `utilizadores`
--

CREATE TABLE `utilizadores` (
  `id_u` int(11) NOT NULL,
  `nick_u` varchar(15) NOT NULL,
  `nome_u` varchar(30) NOT NULL,
  `email_u` varchar(50) DEFAULT NULL,
  `password_u` varchar(255) NOT NULL,
  `pais_u` int(11) NOT NULL,
  `nivel_u` int(11) NOT NULL,
  `confirmado_u` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `utilizadores`
--

INSERT INTO `utilizadores` (`id_u`, `nick_u`, `nome_u`, `email_u`, `password_u`, `pais_u`, `nivel_u`, `confirmado_u`) VALUES
(1, 'Cocas', 'Carlos Costa', 'ccosta13@gmail.com', 'scrypt:32768:8:1$KTHc95eYv99BexJ1$01ca8bf61450ac4dac4188e7f05a1d36e0f4f1c50c5fa63cee65f9ed340f483172a65bae5a63d3d5fe8ccc71e3e000408c160227f6041013b26ca773a50b57f2', 1, 1, 1),
(2, 'Tia_Anica', 'Ana Sousa', 'anamf1987@sapo.pt', 'scrypt:32768:8:1$CTcNo2sE0oqZdmRx$ba733ce51e0907282822ae151a1548b2d964269fa66d6352710faed9dbf72986d5d25edc9f60f5581824f7f4741b83a5e7c00e12a74b5b493265e4d28025882f', 2, 1, 1),
(3, 'DevilOne', 'David Lemos', 'david.osr@iol.pt', 'scrypt:32768:8:1$dXuBBhEoiYKsqoUn$3fe0ac78227b68483c8bc8434fe9827383665ccafbb820819ba6877bc0cc9094ad1ac479fd4fa6abea4d16e8979ecd03eb94edcf938f8256cdde6946abb9c1e1', 1, 1, 1),
(7, 'Adremek', 'Pedro Lapa', 'lapa.pedro@gmail.com', 'scrypt:32768:8:1$db1ZI3R7H4i3nxq5$5490b4db2a26f849f95b3b45e23569ef10ac2c48687b2ba784f467490dc037419a6f3c4104ece8e39c449f5c558ef0d3dc6ecb96a20b6863708aa80e5b8ff27e', 1, 2, 1);

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `anedotas`
--
ALTER TABLE `anedotas`
  ADD PRIMARY KEY (`id_a`),
  ADD KEY `autor_a` (`utilizador_a`),
  ADD KEY `categoria_a` (`categoria_a`);

--
-- Índices para tabela `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_c`);

--
-- Índices para tabela `paises`
--
ALTER TABLE `paises`
  ADD PRIMARY KEY (`id_p`);

--
-- Índices para tabela `utilizadores`
--
ALTER TABLE `utilizadores`
  ADD PRIMARY KEY (`id_u`),
  ADD UNIQUE KEY `nick_u` (`nick_u`),
  ADD UNIQUE KEY `email_u` (`email_u`),
  ADD KEY `pais_au` (`pais_u`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `anedotas`
--
ALTER TABLE `anedotas`
  MODIFY `id_a` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de tabela `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_c` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `paises`
--
ALTER TABLE `paises`
  MODIFY `id_p` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `utilizadores`
--
ALTER TABLE `utilizadores`
  MODIFY `id_u` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `anedotas`
--
ALTER TABLE `anedotas`
  ADD CONSTRAINT `anedotas_ibfk_1` FOREIGN KEY (`utilizador_a`) REFERENCES `utilizadores` (`id_u`),
  ADD CONSTRAINT `anedotas_ibfk_2` FOREIGN KEY (`categoria_a`) REFERENCES `categorias` (`id_c`);

--
-- Limitadores para a tabela `utilizadores`
--
ALTER TABLE `utilizadores`
  ADD CONSTRAINT `utilizadores_ibfk_1` FOREIGN KEY (`pais_u`) REFERENCES `paises` (`id_p`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
