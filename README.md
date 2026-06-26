# Leak Simulation & Redaction Tool

A cybersecurity-focused web application that demonstrates how sensitive information can leak through improper redaction and hidden file metadata.

This project helps users understand why simply placing black boxes over text is not always secure and how metadata such as GPS location, device information, and timestamps can unintentionally expose private information.

## Problem Statement

Many data leaks happen not because of hacking, but because of poor document sanitization.

Examples:

* Blacked-out text that can still be copied
* Images revealing GPS coordinates through EXIF metadata
* Documents exposing author names or revision history

This tool simulates such scenarios and demonstrates secure alternatives.

## Features

### Secure Redaction

* Detects sensitive data using regex
* Supports detection of:

  * Emails
  * Phone numbers
  * IDs
* Removes underlying data instead of visually masking it

### Metadata Analysis

Extracts hidden metadata from files such as:

* GPS location
* Device information
* Timestamps
* Document properties

### Leak Simulation View

* Side-by-side comparison of original vs redacted output
* Highlights hidden leakage risks
* Displays warning messages for unsafe files

## Tech Stack

Frontend:

* HTML
* CSS
* JavaScript

Backend:

* Python
* Flask

Libraries / Concepts:

* Regex
* EXIF Metadata Analysis
* PDF Redaction

## Why I Built This

I built this project to explore practical cybersecurity and privacy engineering problems. The goal was to demonstrate that information leaks often happen due to improper handling of files rather than direct system compromise.

## Future Improvements

* OCR support for scanned PDFs
* Drag-and-drop uploads
* Cloud deployment
* Advanced leak detection using AI

## Author

Ishani Prajapati
