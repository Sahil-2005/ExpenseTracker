-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 02, 2026 at 03:48 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `expense_tracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `expense`
--

CREATE TABLE `expense` (
  `id` int(11) NOT NULL,
  `type` varchar(10) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `date` date DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expense`
--

INSERT INTO `expense` (`id`, `type`, `category`, `amount`, `date`, `description`, `user_id`) VALUES
(3, 'Income', 'Salary', 50000, '2025-07-01', 'Monthly salary', 1),
(4, 'Income', 'Freelancing', 15000, '2025-07-05', 'Web development project', 1),
(5, 'Expense', 'Food', 2500, '2025-07-02', 'Grocery shopping', 1),
(6, 'Expense', 'Transportation', 1200, '2025-07-03', 'Office commute', 1),
(7, 'Expense', 'Entertainment', 1800, '2025-07-04', 'Netflix subscription', 1),
(8, 'Expense', 'Utilities', 2200, '2025-07-06', 'Electricity bill', 1),
(9, 'Expense', 'Healthcare', 30000, '2025-07-07', 'Doctor visit', 1),
(10, 'Expense', 'Shopping', 4500, '2025-07-08', 'Clothes and accessories', 1),
(11, 'Income', 'Investment Returns', 8000, '2025-07-10', 'Stock dividends', 1),
(12, 'Expense', 'Education', 4000, '2025-07-12', 'Online course fee', 1),
(13, 'Expense', 'Food', 1800, '2025-07-13', 'Restaurant dine-in', 1),
(25, 'Recurring', 'Hairdryer Loan', 1000, '2025-08-05', 'Hairdryer Loan - installment auto-deducted', 1),
(27, 'Expense', 'Travel', 1200, '2025-08-07', 'Public transport', 1),
(28, 'Income', 'Freelance', 10000, '2025-08-11', 'Site creation', 1),
(29, 'Income', 'Salary', 50000, '2025-07-01', 'Monthly salary', 2),
(30, 'Income', 'Freelancing', 15000, '2025-07-05', 'Web development project', 2),
(31, 'Expense', 'Food', 2500, '2025-07-02', 'Grocery shopping', 2),
(32, 'Expense', 'Transportation', 1200, '2025-07-03', 'Office commute', 2),
(33, 'Expense', 'Entertainment', 1800, '2025-07-04', 'Netflix subscription', 2),
(34, 'Expense', 'Utilities', 2200, '2025-07-06', 'Electricity bill', 2),
(35, 'Expense', 'Healthcare', 3000, '2025-07-07', 'Doctor visit', 2),
(36, 'Expense', 'Shopping', 4500, '2025-07-08', 'Clothes and accessories', 2),
(37, 'Income', 'Investment Returns', 8000, '2025-07-10', 'Stock dividends', 2),
(38, 'Expense', 'Education', 4000, '2025-07-12', 'Online course fee', 2),
(39, 'Expense', 'Food', 1800, '2025-07-13', 'Restaurant dine-in', 2),
(40, 'Recurring', 'EMI', 2500, '2025-09-29', 'EMI - installment auto-deducted', 2),
(41, 'Recurring', 'EMI', 2500, '2025-10-28', 'EMI - installment auto-deducted', 2);

-- --------------------------------------------------------

--
-- Table structure for table `recurring_expense`
--

CREATE TABLE `recurring_expense` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `total_amount` float NOT NULL,
  `installment_amount` float NOT NULL,
  `frequency` varchar(10) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `installments_remaining` int(11) NOT NULL,
  `last_applied` date DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recurring_expense`
--

INSERT INTO `recurring_expense` (`id`, `name`, `total_amount`, `installment_amount`, `frequency`, `start_date`, `end_date`, `installments_remaining`, `last_applied`, `user_id`) VALUES
(2, 'Hairdryer Loan', 4000, 1000, 'weekly', '2025-07-30', '2025-08-20', 3, '2025-08-05', 1),
(4, 'EMI', 5000, 2500, 'monthly', '2025-09-27', '2025-10-27', 0, '2025-10-28', 2);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `income` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `income`) VALUES
(1, 'Sahil', 'sahil@mail.com', 'scrypt:32768:8:1$7w06hCWCY31V6URX$1be0bdcb56bf25ff2d9c74ea90d118088a99fc341aab7fdfa1f0f11934a66b1f50c2c2b988ec908dab65c978ad881149a66bdfbe7d6e9efecb2752d8998ed9d9', 0),
(2, 'elon', 'elon@mail.com', 'scrypt:32768:8:1$62t2dZmGGyGr0Eif$60352a59cc0ac61dbcec84a3da20af9e77b8872d641394d08069a6dc7cb3e5fc9a90f6c747c3e50876f8a6fecd073f22e4bd7f7dd90b50060f92a7eaa87cfeb1', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `expense`
--
ALTER TABLE `expense`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `recurring_expense`
--
ALTER TABLE `recurring_expense`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `expense`
--
ALTER TABLE `expense`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `recurring_expense`
--
ALTER TABLE `recurring_expense`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `expense`
--
ALTER TABLE `expense`
  ADD CONSTRAINT `expense_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `recurring_expense`
--
ALTER TABLE `recurring_expense`
  ADD CONSTRAINT `recurring_expense_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
