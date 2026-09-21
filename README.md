# AstroDB 🚀

[![GitHub Stars](https://img.shields.io/github/stars/ThreadCrash/AstroDB?style=social)](https://github.com/ThreadCrash/AstroDB)
[![License](https://img.shields.io/github/license/ThreadCrash/AstroDB?color=blue)](LICENSE)
[![C++20](https://img.shields.io/badge/C++-20-blue.svg)](https://en.cppreference.com/w/cpp/20)
[![Go](https://img.shields.io/badge/Go-1.22-00ADD8.svg)](https://golang.org)
[![Release](https://img.shields.io/github/v/release/ThreadCrash/AstroDB?color=orange)](https://github.com/ThreadCrash/AstroDB/releases)

> **AstroDB** is an ultra-fast, embedded columnar analytical database engine built from first principles with vector execution, SIMD filter scanning, and native GUI tools.

---

## 🌟 Key Features

* **Embedded Vector Engine:** Columnar chunk execution with zero-copy SIMD filtering.
* **Astro-SQL CLI:** Interactive terminal interface supporting analytical queries and fast bulk ingestion.
* **Native Desktop GUI:** Modern desktop manager for visual database inspection and query profiling.
* **ACID Transaction Log:** Write-ahead logging (WAL) with multi-version concurrency control (MVCC).

## 🚀 Quick Start

```sh
# Start interactive shell
astrodb example.astrodb

# Execute inline SQL query
astrodb example.astrodb -c "CREATE TABLE numbers AS SELECT * FROM range(1000000);"
astrodb example.astrodb -c "SELECT SUM(range) FROM numbers;"
```

---

⭐ **If you find AstroDB useful, please consider giving it a Star on GitHub to support development!**
