-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-06-2026 a las 06:55:15
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `biosync`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones`
--

CREATE TABLE `sesiones` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `ruta_foto` varchar(255) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `sesiones`
--

INSERT INTO `sesiones` (`id`, `id_usuario`, `ruta_foto`, `fecha`) VALUES
(1, 1, 'fotos\\foto_1_20260607_115417.jpg', '2026-06-07 11:54:17'),
(2, 1, 'fotos\\foto_1_20260607_120329.jpg', '2026-06-07 12:03:29'),
(3, 1, 'fotos\\foto_1_20260607_121323.jpg', '2026-06-07 12:13:23'),
(4, 1, 'fotos\\foto_1_20260607_122916.jpg', '2026-06-07 12:29:16'),
(5, 1, 'fotos\\foto_1_20260607_123249.jpg', '2026-06-07 12:32:49'),
(6, 1, 'fotos\\foto_1_20260607_123254.jpg', '2026-06-07 12:32:54'),
(7, 1, 'fotos\\foto_1_20260607_123259.jpg', '2026-06-07 12:32:59'),
(8, 1, 'fotos\\foto_1_20260607_123548.jpg', '2026-06-07 12:35:48'),
(9, 1, 'fotos\\foto_1_20260607_124418.jpg', '2026-06-07 12:44:18'),
(10, 1, 'fotos\\foto_1_20260607_124756.jpg', '2026-06-07 12:47:56'),
(11, 1, 'fotos\\foto_1_20260607_125536.jpg', '2026-06-07 12:55:36'),
(12, 1, 'fotos\\foto_1_20260607_125656.jpg', '2026-06-07 12:56:56'),
(13, 1, 'fotos\\foto_1_20260607_130101.jpg', '2026-06-07 13:01:01'),
(14, 1, 'fotos\\foto_1_20260607_130340.jpg', '2026-06-07 13:03:40'),
(15, 1, 'fotos\\foto_1_20260607_133637.jpg', '2026-06-07 13:36:37'),
(16, 1, 'fotos\\foto_1_20260607_143934.jpg', '2026-06-07 14:39:34'),
(17, 1, 'fotos\\foto_1_20260607_144243.jpg', '2026-06-07 14:42:43'),
(18, 1, 'fotos\\foto_1_20260607_144247.jpg', '2026-06-07 14:42:47'),
(19, 1, 'fotos\\foto_1_20260607_150453.jpg', '2026-06-07 15:04:53'),
(20, 1, 'fotos\\foto_1_20260607_150805.jpg', '2026-06-07 15:08:05'),
(21, 1, 'fotos\\foto_1_20260607_150809.jpg', '2026-06-07 15:08:09'),
(22, 1, 'fotos\\foto_1_20260607_151613.jpg', '2026-06-07 15:16:13'),
(23, 1, 'fotos\\foto_1_20260607_151616.jpg', '2026-06-07 15:16:16'),
(24, 1, 'fotos\\foto_1_20260607_152129.jpg', '2026-06-07 15:21:29'),
(25, 1, 'fotos\\foto_1_20260607_152346.jpg', '2026-06-07 15:23:46'),
(26, 1, 'fotos\\foto_1_20260607_152650.jpg', '2026-06-07 15:26:50'),
(27, 1, 'fotos\\foto_1_20260607_153420.jpg', '2026-06-07 15:34:20'),
(28, 1, 'fotos\\foto_1_20260607_153426.jpg', '2026-06-07 15:34:26'),
(29, 1, 'fotos\\foto_1_20260607_161705.jpg', '2026-06-07 16:17:05'),
(30, 1, 'fotos\\foto_1_20260607_162802.jpg', '2026-06-07 16:28:02'),
(31, 1, 'fotos\\foto_1_20260607_165004.jpg', '2026-06-07 16:50:04'),
(32, 1, 'fotos\\foto_1_20260607_173658.jpg', '2026-06-07 17:36:58'),
(33, 1, 'fotos\\foto_1_20260607_174624.jpg', '2026-06-07 17:46:24'),
(34, 1, 'fotos\\foto_1_20260607_175359.jpg', '2026-06-07 17:53:59'),
(35, 1, 'fotos\\foto_1_20260607_175849.jpg', '2026-06-07 17:58:49'),
(36, 1, 'fotos\\foto_1_20260607_180117.jpg', '2026-06-07 18:01:17'),
(37, 1, 'fotos\\foto_1_20260607_214758.jpg', '2026-06-07 21:47:58'),
(38, 1, 'fotos\\foto_1_20260607_222836.jpg', '2026-06-07 22:28:36'),
(39, 1, 'fotos\\foto_1_20260607_224641.jpg', '2026-06-07 22:46:41'),
(40, 1, 'fotos\\foto_1_20260607_225109.jpg', '2026-06-07 22:51:09'),
(41, 1, 'fotos\\foto_1_20260607_230541.jpg', '2026-06-07 23:05:41'),
(42, 1, 'fotos\\foto_1_20260607_230546.jpg', '2026-06-07 23:05:46'),
(43, 1, 'fotos\\foto_1_20260607_231200.jpg', '2026-06-07 23:12:00'),
(44, 1, 'fotos\\foto_1_20260607_231204.jpg', '2026-06-07 23:12:04'),
(45, 1, 'fotos\\foto_1_20260607_231449.jpg', '2026-06-07 23:14:49'),
(46, 1, 'fotos\\foto_1_20260607_232232.jpg', '2026-06-07 23:22:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `usuario` varchar(50) DEFAULT NULL,
  `contrasena` varchar(100) DEFAULT NULL,
  `rol` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `usuario`, `contrasena`, `rol`) VALUES
(1, 'Administrador', 'admin', 'admin123', 'administrador'),
(2, 'Usuario Test', 'user', 'user123', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
