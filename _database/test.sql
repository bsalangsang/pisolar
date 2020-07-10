-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 22, 2020 at 08:56 AM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.1.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `ldgr_shs`
--

CREATE TABLE `ldgr_shs` (
  `ctrlNo` int(11) NOT NULL,
  `ldgrNo` varchar(12) COLLATE latin1_general_ci NOT NULL,
  `ldgrDate` date NOT NULL,
  `ldgrTypeNo` int(2) NOT NULL,
  `refNo` varchar(12) COLLATE latin1_general_ci NOT NULL,
  `shsNo` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `shsCode` varchar(12) COLLATE latin1_general_ci NOT NULL,
  `amount` varchar(10) COLLATE latin1_general_ci NOT NULL,
  `balance` varchar(10) COLLATE latin1_general_ci NOT NULL,
  `remarks` varchar(200) COLLATE latin1_general_ci NOT NULL,
  `encodeDate` datetime NOT NULL,
  `encodeBy` varchar(5) COLLATE latin1_general_ci NOT NULL,
  `editDate` datetime DEFAULT NULL,
  `editBy` varchar(5) COLLATE latin1_general_ci DEFAULT NULL,
  `isActive` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'Y',
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Dumping data for table `ldgr_shs`
--

INSERT INTO `ldgr_shs` (`ctrlNo`, `ldgrNo`, `ldgrDate`, `ldgrTypeNo`, `refNo`, `shsNo`, `shsCode`, `amount`, `balance`, `remarks`, `encodeDate`, `encodeBy`, `editDate`, `editBy`, `isActive`, `status`) VALUES
(1, '1', '2020-06-15', 2, '0001', '1', '1', '20000', '20000', 'credit', '0000-00-00 00:00:00', '', NULL, NULL, 'Y', 0),
(2, '2', '2020-06-15', 1, '0001', '1', '1', '500', '19500', 'debit', '0000-00-00 00:00:00', '', NULL, NULL, 'Y', 0),
(3, '3', '2020-06-15', 1, '0001', '1', '1', '600', '18900', 'dEBIT', '0000-00-00 00:00:00', '', NULL, NULL, 'Y', 0),
(4, '4', '2020-06-15', 1, '0001', '1', '1', '700', '18200', '', '0000-00-00 00:00:00', '', NULL, NULL, 'Y', 0),
(5, '5', '2020-06-15', 1, '0001', '1', '1', '900', '17300', 'debit', '0000-00-00 00:00:00', '', NULL, NULL, 'Y', 0),
(6, '6', '2020-06-15', 1, '0001', '1', '1', '500', '16800', '', '0000-00-00 00:00:00', '', NULL, NULL, 'Y', 0);

-- --------------------------------------------------------

--
-- Table structure for table `man_customers`
--

CREATE TABLE `man_customers` (
  `customerNo` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `customerCode` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `vleNo` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `fName` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `mName` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `lName` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `contactPerson` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `address` varchar(250) COLLATE latin1_general_ci NOT NULL,
  `contact1` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `contact2` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `isActive` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'Y',
  `isVisible` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'Y'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Dumping data for table `man_customers`
--

INSERT INTO `man_customers` (`customerNo`, `customerCode`, `vleNo`, `fName`, `mName`, `lName`, `contactPerson`, `address`, `contact1`, `contact2`, `isActive`, `isVisible`) VALUES
('A1CUSA00001', '1', 'A1VLEA00002', 'Robert', 'John', 'Downey Jr.', 'Robert Downey Jr.', 'Toril, Davao City', '09555', '09333', 'Y', 'Y'),
('A1CUSA00002', '2', 'A1VLEA00001', 'Scarlett', 'D', 'Johansson', 'Scarlett Johansson', '', '', '', 'Y', 'Y'),
('A1CUSA00003', '3', 'A1VLEA00001', 'Samuel', 'Leroy', 'Jackson', 'Samuel Leroy Jackson', '', '', '', 'Y', 'Y');

-- --------------------------------------------------------

--
-- Table structure for table `man_shs`
--

CREATE TABLE `man_shs` (
  `shsNo` varchar(12) COLLATE latin1_general_ci NOT NULL,
  `shsCode` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `shsName` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `customerNo` varchar(12) COLLATE latin1_general_ci NOT NULL,
  `serialNo` varchar(30) COLLATE latin1_general_ci NOT NULL,
  `simNo` varchar(13) COLLATE latin1_general_ci NOT NULL,
  `firmwareVer` varchar(8) COLLATE latin1_general_ci NOT NULL,
  `softwareVer` varchar(8) COLLATE latin1_general_ci NOT NULL,
  `machStat` int(1) NOT NULL DEFAULT '0',
  `username` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `password` varchar(8) COLLATE latin1_general_ci NOT NULL,
  `isActive` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'N',
  `isVisible` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'Y'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Dumping data for table `man_shs`
--

INSERT INTO `man_shs` (`shsNo`, `shsCode`, `shsName`, `customerNo`, `serialNo`, `simNo`, `firmwareVer`, `softwareVer`, `machStat`, `username`, `password`, `isActive`, `isVisible`) VALUES
('A1SHSA00001', '1', 'SHS Tagum', '2', '290E-1650-9960-7012', '0922654987', 'v1.0', 'v1.2', 0, '', '', 'Y', 'Y'),
('A1SHSA00002', '2', 'SHS Mandug', '4', '290E-1650-9960-7011', '0946549879', 'v1.0', 'v1.2', 0, '', '', 'Y', 'Y'),
('A1SHSA00003', '3', 'SHS Sta Cruz', '1', '290E-1650-9960-701S', '', '', '', 0, '', '', 'Y', 'Y'),
('A1SHSA00004', '4', 'SHS Panabo', '2', '540E-1450-9960-7511', '', '', '', 0, '', '', 'Y', 'Y'),
('A1SHSA00005', '5', 'SHS Panacan', '3', '9960-1650-9960-7010', '', '', '', 0, '', '', 'Y', 'Y');

-- --------------------------------------------------------

--
-- Table structure for table `man_vle`
--

CREATE TABLE `man_vle` (
  `vleNo` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `vleCode` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `fName` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `mName` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `lName` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `contactPerson` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `address` varchar(250) COLLATE latin1_general_ci NOT NULL,
  `contact1` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `contact2` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `isActive` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'Y',
  `isVisible` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'Y'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Dumping data for table `man_vle`
--

INSERT INTO `man_vle` (`vleNo`, `vleCode`, `fName`, `mName`, `lName`, `contactPerson`, `address`, `contact1`, `contact2`, `isActive`, `isVisible`) VALUES
('A1VLEA00001', '1', 'Will', 'Carroll', 'Smith Jr.', 'Willard Carroll \"Will\" Smith, Jr.', 'Davao CIty', '09111', '09222', 'Y', 'Y');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ldgr_shs`
--
ALTER TABLE `ldgr_shs`
  ADD PRIMARY KEY (`ctrlNo`);

--
-- Indexes for table `man_customers`
--
ALTER TABLE `man_customers`
  ADD PRIMARY KEY (`customerNo`);

--
-- Indexes for table `man_shs`
--
ALTER TABLE `man_shs`
  ADD PRIMARY KEY (`shsNo`);

--
-- Indexes for table `man_vle`
--
ALTER TABLE `man_vle`
  ADD PRIMARY KEY (`vleNo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ldgr_shs`
--
ALTER TABLE `ldgr_shs`
  MODIFY `ctrlNo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
