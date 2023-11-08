-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: db:3306
-- Tiempo de generación: 08-11-2023 a las 02:31:34
-- Versión del servidor: 8.1.0
-- Versión de PHP: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `advicegpt_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mood_tracker`
--

CREATE TABLE `mood_tracker` (
  `num` int NOT NULL,
  `user_id` int NOT NULL,
  `date` date NOT NULL,
  `emotions` varchar(255) DEFAULT NULL,
  `well_being_level` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `mood_tracker`
--

INSERT INTO `mood_tracker` (`num`, `user_id`, `date`, `emotions`, `well_being_level`) VALUES
(4, 1, '2023-10-31', '[sad, angry]', 2),
(5, 1, '2023-10-31', '[sad, grief, loss]', 2),
(6, 1, '2023-10-31', '[sad, grief, heartbroken]', 2),
(7, 1, '2023-10-31', '[thrilled]', 8),
(8, 1, '2023-10-31', '[sad, rejected]', 4),
(9, 1, '2023-10-31', '[frustration, despair]', 3),
(10, 1, '2023-10-31', '[tired]', 5),
(11, 1, '2023-10-31', '[fear, anxiety]', 4),
(12, 1, '2023-10-31', '[fear, anxiety]', 4),
(13, 1, '2023-10-31', '[fear, anxiety]', 3),
(14, 4, '2023-11-01', '[tired, confused]', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `Id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` char(102) NOT NULL,
  `used_tokens` int DEFAULT '0',
  `email` varchar(255) NOT NULL,
  `age` int DEFAULT NULL,
  `fullname` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`Id`, `username`, `password`, `used_tokens`, `email`, `age`, `fullname`) VALUES
(1, 'ramontalvo', 'pbkdf2:sha256:260000$l55YSvv2r8atgQv1$95780a13f8f3a5885a302c50f5937c2b8c0d3e95f0ff1009c094216126e28376', 2570, 'richi_email@live.com', 23, 'Richard Montalvo'),
(2, '1600602708', 'pbkdf2:sha256:260000$uJVd2XGHHPP8wCVc$6a4f549e375326beb9f059aa0c3c47db99cf9b3abeed3ccdb62ff996fcef22fe', 0, 'richardmontalvo074@gmail.com', 0, 'Richard Alexander Montalvo'),
(3, 'ydrgsdf', 'pbkdf2:sha256:260000$d7VsP0QhSTP2LIF9$8116b87d154c0418c2a70e242b6976cd9fb416328fb34baf775167f0103f3e81', 0, 'venger10@live.com', 17, 'Alex Montalvo'),
(4, 'danaguirre', 'pbkdf2:sha256:260000$EtiNn3BiuIenFb4o$eea30a6d49fbdeac72df6bc9e5a9e106d724b31fb26e5097015f6841cc3b8696', 399, 'dhanny_aguirre@hotmail.com', 26, 'Danny Fernando Aguirre Espin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `mood_tracker`
--
ALTER TABLE `mood_tracker`
  ADD PRIMARY KEY (`num`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `mood_tracker`
--
ALTER TABLE `mood_tracker`
  MODIFY `num` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `mood_tracker`
--
ALTER TABLE `mood_tracker`
  ADD CONSTRAINT `mood_tracker_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`Id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
